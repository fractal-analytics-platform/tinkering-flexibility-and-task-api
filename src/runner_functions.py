from copy import copy
from typing import Any

from env import MAX_PARALLELIZATION_LIST_SIZE
from images import find_image_by_path
from models import SingleImage
from models import Task
from task_output import merge_outputs
from task_output import ParallelTaskOutput
from task_output import TaskOutput
from utils import pjson


def _run_non_parallel_task(
    task: Task,
    function_kwargs: dict[str, Any],
    old_dataset_images: list[SingleImage],
) -> dict[str, Any]:

    task_output = task.function(**function_kwargs)
    if task_output is None:
        return TaskOutput()

    task_output = TaskOutput(**{k: v for k, v in task_output.items() if v is not None})

    # Process the output, to propagate some image attributes - if possible
    # FIXME: refactor this into a "process_task_output" function?
    if task_output.new_images is not None:
        old_image_paths = function_kwargs["paths"]
        new_image_paths = [new_image.path for new_image in task_output.new_images]
        if len(old_image_paths) == len(new_image_paths):
            new_old_image_mapping = {}
            for ind, new_image_path in enumerate(new_image_paths):
                new_old_image_mapping[new_image_path] = old_image_paths[ind]
            final_new_images = []
            for new_image in task_output.new_images:
                old_image = find_image_by_path(
                    images=old_dataset_images,
                    path=new_old_image_mapping[new_image.path],
                )
                new_image.attributes = old_image.attributes | new_image.attributes
                final_new_images.append(new_image)
            task_output.new_images = final_new_images

    print(f"Task output:\n{pjson(task_output.dict())}")
    # Validate task output:
    TaskOutput(**task_output.dict())

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
        if task_output is not None:
            task_output = ParallelTaskOutput(**{k: v for k, v in task_output.items() if v is not None})
            if task_output.new_images is not None:
                new_old_image_mapping.update(
                    {new_image.path: function_kwargs["path"] for new_image in task_output.new_images}
                )
            task_outputs.append(copy(task_output))
        else:
            task_outputs.append(ParallelTaskOutput())

    merged_output = merge_outputs(task_outputs, new_old_image_mapping, old_dataset_images)

    return merged_output
