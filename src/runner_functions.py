from copy import copy
from typing import Any

from env import MAX_PARALLELIZATION_LIST_SIZE
from models import SingleImage
from models import Task
from task_output import merge_outputs
from task_output import ParallelTaskOutput
from task_output import TaskOutput
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
                {new_image["path"]: function_kwargs["path"] for new_image in task_output["new_images"]}
            )

        ParallelTaskOutput(**task_output)
        task_outputs.append(copy(task_output))

    task_output = merge_outputs(
        task_outputs,
        new_old_image_mapping,
        old_dataset_images,
    )

    return task_output
