from copy import copy
from copy import deepcopy
from typing import Any

from models import Dataset
from models import Task
from utils import pjson


def _run_non_parallel_task(
    task: Task,
    current_image_list: list[dict[str, Any]],
    function_args: dict[str, Any],
    _dataset: Dataset,
) -> dict[str, Any]:
    tmp_function_args = deepcopy(function_args)
    tmp_function_args["root_dir"] = _dataset.root_dir
    tmp_function_args["paths"] = [image["path"] for image in current_image_list]
    tmp_buffer = deepcopy(_dataset.buffer)
    if tmp_buffer is not None and "parallelization_list" in tmp_buffer.keys():
        raise ValueError("parallelization_list provided to non-parallel task")
    tmp_function_args["buffer"] = tmp_buffer
    task_output = task.function(**tmp_function_args)
    print(f"Task output:\n{pjson(task_output)}")
    return task_output


def _run_parallel_task(
    task: Task,
    current_image_list: list[dict[str, Any]],
    function_args: dict[str, Any],
    _dataset: Dataset,
) -> dict[str, Any]:

    task_outputs = []
    for image in current_image_list:
        tmp_function_args = deepcopy(function_args)
        tmp_function_args["root_dir"] = _dataset.root_dir
        tmp_function_args["buffer"] = _dataset.buffer
        tmp_function_args["path"] = image["path"]
        task_output = task.function(**tmp_function_args)
        task_outputs.append(copy(task_output))

    # Reset buffer after using it
    _dataset.buffer = None

    # Merge processed images
    task_output = {}

    # TODO: clean-up parallel metadata merge

    # Merge new/edited images
    _new_images = []
    _edited_images = []
    for _out in task_outputs:
        for _new_image in _out.get("new_images", []):
            _new_images.append(_new_image)
        for _edited_path in _out.get("edited_paths", []):
            _edited_images.append(_edited_path)
    if _new_images:
        task_output["new_images"] = _new_images
    if _edited_images:
        task_output["edited_paths"] = _edited_images

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
