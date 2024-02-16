from copy import copy
from typing import Any

from env import MAX_PARALLELIZATION_LIST_SIZE
from images import find_image_by_path
from models import SingleImage
from models import Task
from models import TaskOutput
from models import ParallelTaskOutput
from utils import pjson


def _run_non_parallel_task(
    task: Task,
    function_kwargs: dict[str, Any],
) -> dict[str, Any]:
    task_output = task.function(**function_kwargs)
    if task_output is None:
        task_output = {}
    print(f"Task output:\n{pjson(task_output)}")
    # Validate task output:
    TaskOutput(**task_output)
    return task_output


def _run_parallel_task(
    task: Task,
    list_function_kwargs: list[dict[str, Any]],
    old_dataset_images: list[SingleImage],
) -> dict[str, Any]:

    if len(list_function_kwargs) > MAX_PARALLELIZATION_LIST_SIZE:
        raise ValueError(
            "Too many parallelization items.\n"
            f"   {len(list_function_kwargs)=}\n"
            f"   {MAX_PARALLELIZATION_LIST_SIZE=}\n"
        )

    task_outputs = []
    new_old_image_mapping = {}
    for function_kwargs in list_function_kwargs:
        task_output = task.function(**function_kwargs)
        if task_output is None:
            task_output = {}
        if task_output.get("new_images") is not None:
            new_old_image_mapping.update(
                {
                    new_image["path"]: function_kwargs["path"]
                    for new_image in task_output["new_images"]
                }
            )
        ParallelTaskOutput(**task_output)
        task_outputs.append(copy(task_output))

    # Merge processed images # FIXME
    task_output = {}

    # TODO: clean-up parallel metadata merge
    # FIXME Yuri: represent current merge strategies in test_run_parallel_task

    # Merge new/edited images
    _new_images = []
    _edited_images = []
    for _out in task_outputs:
        for new_image in _out.get("new_images", []):
            # Propagate old-image attributes to new-image
            old_image = find_image_by_path(
                images=old_dataset_images,
                path=new_old_image_mapping[new_image["path"]],
            )
            actual_new_image = old_image
            actual_new_image.update(new_image)

            _new_images.append(actual_new_image)
        for _edited_image in _out.get("edited_images", []):
            _edited_images.append(_edited_image)
    if _new_images:
        task_output["new_images"] = _new_images
    if _edited_images:
        task_output["edited_images"] = _edited_images

    # Merge new filters
    _new_filters = None
    for _out in task_outputs:
        current_filters = _out.get("new_filters", None)
        if current_filters is None:
            pass
        else:
            if _new_filters is None:
                _new_filters = current_filters
            else:
                if _new_filters != current_filters:
                    raise ValueError(f"{current_filters=} but {_new_filters=}")
    if _new_filters:
        task_output["new_filters"] = _new_filters

    print(f"Merged task output:\n{pjson(task_output)}")
    return task_output
