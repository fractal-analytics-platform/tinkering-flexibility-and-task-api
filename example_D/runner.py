import json
from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from models import Dataset
from models import FilterSet
from models import Task
from models import WorkflowTask
from termcolor import cprint


def pjson(x: dict) -> str:
    """
    Naive JSON pretty-print.
    """
    return json.dumps(x, indent=2)


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


def _run_standard_task(
    task: Task,
    function_args: dict[str, Any],
) -> dict[str, Any]:
    task_output = task.function(**function_args)
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
        function_args.update(
            dict(
                path=image["path"],
                buffer=_dataset.buffer,
            )
        )
        task_output = task.function(**function_args)
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

    print(f"Merged task output:\n{json.dumps(task_output, indent=2)}")
    return task_output


def _run_combined_task(
    task: Task,
    current_image_list: list[dict[str, Any]],
    function_args: dict[str, Any],
    _dataset: Dataset,
) -> dict[str, Any]:
    paths = [image["path"] for image in current_image_list]
    function_args.update(
        dict(
            paths=paths,
            buffer=_dataset.buffer,
        )
    )
    task_output = task.function(**function_args)
    print(f"Task output:\n{pjson(task_output)}")
    return task_output


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
        task_function = task.function
        function_args = wftask.args
        function_args.update(dict(root_dir=tmp_dataset.root_dir))

        # Run task
        print(f"NOW RUN {task.name}\n" f"    Task type: {task.task_type}\n")

        if task.task_type == "standard":
            task_output = _run_standard_task(task, function_args)
            images_to_process = []
        else:

            print(
                f"Default filters:      {pjson(tmp_dataset.default_filters)}"
            )
            print(f"WorkflowTask filters: {pjson(wftask.filters)}")

            current_filters = copy(tmp_dataset.default_filters)
            current_filters.update(wftask.filters)
            print(f"Current filters:      {pjson(current_filters)}")

            images_to_process = _filter_image_list(
                tmp_dataset.images,
                filters=current_filters,
            )
            print(f"Filtered image list:  {pjson(images_to_process)}")

            if task.task_type == "combine_images":
                task_output = _run_combined_task(
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

        # Add filters to processed images
        new_images = task_output.get("new_images", [])
        processed_images_paths = [
            image["path"] for image in new_images
        ] + task_output.get("edited_paths", [])

        for ind, image in enumerate(tmp_dataset.images):
            if image["path"] in processed_images_paths:
                updated_image = deepcopy(image)
                for key, value in task.new_default_filters.items():
                    updated_image[key] = value
                tmp_dataset.images[ind] = updated_image

        # Update dataset metadata / default filters
        new_filters = tmp_dataset.default_filters
        new_filters.update(task.new_default_filters)
        new_filters.update(task_output.get("new_filters", {}))

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
                overlap = next(
                    _image
                    for _image in tmp_dataset.images
                    if _image["path"] == image["path"]
                )
                raise ValueError(f"Found {overlap=}")
            except StopIteration:
                pass
            print(f"Add {image} to list")
            tmp_dataset.images.append(image)

        # Update dataset metadata / filters
        tmp_dataset.default_filters = new_filters

        # Update dataset metadata / buffer
        if task_output.get("buffer", None) is not None:
            tmp_dataset.buffer = task_output["buffer"]

        # Update dataset metadata / history
        tmp_dataset.history.append(task_function.__name__)

        print(f"AFTER RUNNING {task_function.__name__}:")
        print(pjson(tmp_dataset.dict()))
        print("\n" + "-" * 88 + "\n")
