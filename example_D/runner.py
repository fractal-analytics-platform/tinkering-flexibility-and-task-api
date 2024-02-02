import json
from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from models import Dataset
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
    filters: Optional[dict[str, Any]] = None,
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

    parallel_task_outs = []
    for image in current_image_list:
        tmp_image = deepcopy(image)
        image_path = tmp_image.pop("path")
        function_args.update(
            dict(
                path=image_path,
                buffer=_dataset.buffer,
                image_meta=tmp_image,
            )
        )
        task_output = task.function(**function_args)
        parallel_task_outs.append(task_output)
    # Reset buffer after using it
    _dataset.buffer = None

    # TODO: clean-up parallel metadata merge
    _new_images = []
    _new_filters = None
    for _out in parallel_task_outs:
        for new_image in _out.get("new_images", []):
            _new_images.append(new_image)

        current_filters = _out.get("new_filters", None)
        if current_filters is None:
            pass
        else:
            if _new_filters is None:
                _new_filters = current_filters
            else:
                if _new_filters != current_filters:
                    raise ValueError(f"{current_filters=} but {_new_filters=}")

    task_output = {}
    if _new_images:
        task_output["new_images"] = _new_images
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
    components = []
    image_metas = []
    for image in current_image_list:
        tmp_image = deepcopy(image)
        components.append(tmp_image.pop("path"))
        image_metas.append(tmp_image)

    function_args.update(
        dict(
            paths=components,
            buffer=_dataset.buffer,
            image_metas=image_metas,
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
        else:
            # TODO: include wftask-specific filters
            current_image_list = _filter_image_list(
                tmp_dataset.images,
                filters=tmp_dataset.default_filters,
            )
            print(f"Current filters:     {pjson(tmp_dataset.default_filters)}")
            print(f"Filtered image list: {pjson(current_image_list)}")

            if task.task_type == "combine_images":
                task_output = _run_combined_task(
                    task=task,
                    current_image_list=current_image_list,
                    function_args=function_args,
                    _dataset=tmp_dataset,
                )
            elif task.task_type == "parallel":
                task_output = _run_parallel_task(
                    task=task,
                    current_image_list=current_image_list,
                    function_args=function_args,
                    _dataset=tmp_dataset,
                )
            else:
                raise ValueError(f"Invalid {task.task_type=}.")

        # Process new_images, if any
        new_images = task_output.get("new_images", [])
        for ind, image in enumerate(new_images):
            new_image = deepcopy(image)
            for key, value in task.new_default_filters.items():
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

        # Update dataset metadata / buffer
        if task_output.get("buffer", None) is not None:
            tmp_dataset.buffer = task_output["buffer"]

        # Update dataset metadata / default filters
        new_filters = tmp_dataset.default_filters
        new_filters.update(task.new_default_filters)
        new_filters.update(task_output.get("new_filters", {}))
        tmp_dataset.default_filters = new_filters

        # Update dataset metadata / history
        tmp_dataset.history.append(task_function.__name__)

        print(f"AFTER RUNNING {task_function.__name__}:")
        print(pjson(tmp_dataset.dict()))
        print("\n" + "-" * 88 + "\n")
