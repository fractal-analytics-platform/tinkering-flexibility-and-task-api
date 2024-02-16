from copy import copy
from typing import Any

from env import MAX_PARALLELIZATION_LIST_SIZE
from images import find_image_by_path
from models import SingleImage
from models import Task
from task_output import TaskOutput
from task_output import ParallelTaskOutput
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
        
        task_output = task.function(**function_kwargs) or {}

        if task_output.get("new_images") is not None:
            new_old_image_mapping.update(
                {
                    new_image["path"]: function_kwargs["path"]
                    for new_image in task_output["new_images"]
                }
            )

        ParallelTaskOutput(**task_output)
        task_outputs.append(copy(task_output))

    task_output = merge_outputs(
        task_outputs,
        new_old_image_mapping,
        old_dataset_images,
    )

    return task_output



def merge_outputs(
        task_outputs: list[ParallelTaskOutput],
        new_old_image_mapping: dict[str, str],
        old_dataset_images: list[SingleImage],
    ):
    
    final_new_images = []
    final_edited_images = []
    final_new_filters = None
    
    for task_output in task_outputs:
        
        for new_image in task_output.get("new_images", []):
            old_image = find_image_by_path(
                images=old_dataset_images,
                path=new_old_image_mapping[new_image["path"]],
            )
            final_new_images.append(
                # Propagate old-image attributes to new-image
                old_image | new_image
            )
        
        for edited_image in task_output.get("edited_images", []):
            final_edited_images.append(edited_image)

        if new_filters := task_output.get("new_filters"):
            if final_new_filters is None:
                final_new_filters = new_filters
            else:
                if final_new_filters != new_filters:
                    raise ValueError(
                        f"{new_filters=} but {final_new_filters=}"
                    )

    final_output = dict()
    if final_new_images:
        final_output["new_images"] = final_new_images
    if final_edited_images:
        final_output["edited_images"] = final_edited_images
    if final_new_filters:
        final_output["new_filters"] = final_new_filters
    ParallelTaskOutput(**final_output)
    
    print(f"Merged task output:\n{pjson(final_output)}")

    return final_output