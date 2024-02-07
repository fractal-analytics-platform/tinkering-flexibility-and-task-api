from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from models import Dataset
from models import FilterSet
from models import Task
from models import WorkflowTask
from termcolor import cprint
from utils import ipjson
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


def _filter_image_list(
    images: list[dict[str, Any]],
    filters: Optional[FilterSet] = None,
    debug_mode: bool = False,
) -> list[dict[str, Any]]:
    def print(x):
        return cprint(x, "red")

    filtered_images = []
    if filters is None:
        return images
    for image in images:
        include_image = True
        for key, value in filters.items():
            if debug_mode:
                print(key, value, image.get(key))
            if image.get(key, False) != value:
                include_image = False
                break
        if debug_mode:
            print(image, include_image)
        if include_image:
            filtered_images.append(copy(image))
    return filtered_images


def apply_workflow(
    wf_task_list: list[WorkflowTask],
    dataset: Dataset,
):
    def print(x):
        return cprint(x, "magenta")

    # Run task 0
    tmp_dataset = deepcopy(dataset)

    for wftask in wf_task_list:
        task = wftask.task
        function_args = wftask.args

        print(f"NOW RUN {task.name} (task type: {task.task_type})")

        # Set global selection filters
        current_filters = copy(tmp_dataset.filters)
        current_filters.update(wftask.filters)
        print(f"Dataset filters:\n{ipjson(tmp_dataset.filters)}")
        print(f"WorkflowTask filters:\n{ipjson(wftask.filters)}")
        print(f"Current selection filters:\n{ipjson(current_filters)}")

        images_to_process = _filter_image_list(
            tmp_dataset.images,
            filters=current_filters,
        )
        print(f"Filtered image list:  {pjson(images_to_process)}")

        if task.task_type == "non_parallel":
            task_output = _run_non_parallel_task(
                task=task,
                current_image_list=images_to_process,
                function_args=function_args,
                _dataset=tmp_dataset,
            )
        elif task.task_type == "parallel":
            task_output = _run_parallel_task(
                task=task,
                current_image_list=images_to_process,
                function_args=function_args,
                _dataset=tmp_dataset,
            )
        else:
            raise ValueError(f"Invalid {task.task_type=}.")

        # Decorate new images with source-image attributes
        new_images = task_output.get("new_images", [])
        for ind, new_image in enumerate(new_images):
            pass
            # FIXME: missing
            # source_image[new_image["path"]] = ??
            # actual_new_image = copy(source_image)
            # actual_new_image.update(new_image)
            # new_images[ind] = actual_new_image

        # Add filters to processed images
        new_images = task_output.get("new_images", [])
        processed_images_paths = [image["path"] for image in new_images] + task_output.get("edited_paths", [])

        for ind, image in enumerate(tmp_dataset.images):
            if image["path"] in processed_images_paths:
                updated_image = deepcopy(image)
                for key, value in task.new_filters.items():
                    updated_image[key] = value
                tmp_dataset.images[ind] = updated_image

        # Update Dataset.filters
        new_filters = copy(tmp_dataset.filters)
        new_filters.update(task.new_filters)
        actual_task_new_filters = task_output.get("new_filters", {})
        new_filters.update(actual_task_new_filters)
        print(f"Dataset old filters:\n{ipjson(tmp_dataset.filters)}")
        print(f"Task.new_filters:\n{ipjson(task.new_filters)}")
        print(f"Actual new filters from task:\n{ipjson(actual_task_new_filters)}")
        print(f"Combined new filters:\n{ipjson(new_filters)}")
        tmp_dataset.filters = new_filters

        # Update Dataset.buffer with task output or None
        tmp_dataset.buffer = task_output.get("buffer", None)

        # Update Dataset.history
        tmp_dataset.history.append(task.name)

        # Process new_images, if any
        new_images = task_output.get("new_images", [])
        for ind, image in enumerate(new_images):
            new_image = deepcopy(image)
            for key, value in new_filters.items():
                new_image[key] = value
            new_images[ind] = new_image

        # Update dataset metadata / images
        for image in new_images:
            try:
                overlap = next(_image for _image in tmp_dataset.images if _image["path"] == image["path"])
                raise ValueError(f"Found {overlap=}")
            except StopIteration:
                pass
            print(f"Add {image} to list")
            tmp_dataset.images.append(image)

        # End-of-task logs
        print(f"AFTER RUNNING {task.name}, we have:")
        print(ipjson(tmp_dataset.dict()))
        print("\n" + "-" * 88 + "\n")
