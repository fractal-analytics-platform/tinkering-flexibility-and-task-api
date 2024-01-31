import json
import os
import shutil
from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from models import Dataset
from tasks import cellpose_segmentation
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import yokogawa_to_zarr
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


def apply_workflow(
    wf_task_list: list[dict],
    tasks: dict[str, dict],
    dataset: Dataset,
):
    def print(x):
        return cprint(x, "magenta")

    # Run task 0
    tmp_dataset = deepcopy(dataset)

    for wftask in wf_task_list:
        task_function = tasks[wftask["task_id"]]["function"]
        function_args = wftask["args"]
        function_args.update(dict(root_dir=tmp_dataset.root_dir))

        # Run task
        task = tasks[wftask["task_id"]]
        is_parallel = task.get("meta", {}).get("parallel", False)

        print(
            f"NOW RUN {task_function.__name__} (is it parallel? {is_parallel})"
        )

        if not is_parallel:
            task_output = task_function(**function_args)
            print(f"Task output:\n{pjson(task_output)}")
        else:
            parallel_task_outs = []
            # TODO: include wftask-specific filters
            current_image_list = _filter_image_list(
                tmp_dataset.images,
                filters=tmp_dataset.default_filters,
            )
            print(f"Current filters:     {pjson(tmp_dataset.default_filters)}")
            print(f"Filtered image list: {pjson(current_image_list)}")
            for image in current_image_list:
                tmp_image = deepcopy(image)
                image_path = tmp_image.pop("path")
                function_args.update(
                    dict(
                        component=image_path,
                        buffer=tmp_dataset.buffer,
                        image_meta=tmp_image,
                    )
                )
                task_output = task_function(**function_args)
                parallel_task_outs.append(task_output)
            # Reset buffer after using it
            tmp_dataset.buffer = None

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
                            raise ValueError(
                                f"{current_filters=} but {_new_filters=}"
                            )

            task_output = {}
            if _new_images:
                task_output["new_images"] = _new_images
            if _new_filters:
                task_output["new_filters"] = _new_filters

            print(f"Merged task output:\n{json.dumps(task_output, indent=2)}")

        # Update dataset metadata / images
        for image in task_output.get("new_images", []):
            try:
                overlap = next(
                    _image
                    for _image in tmp_dataset.images
                    if _image["path"] == image["path"]
                )
                raise ValueError(f"Found {overlap=}")
            except StopIteration:
                pass
            tmp_dataset.images.append(image)
        # Update dataset metadata / buffer
        if task_output.get("buffer", None) is not None:
            tmp_dataset.buffer = task_output["buffer"]
        # Update dataset metadata / default filters
        if task_output.get("new_filters", None) is not None:
            new_default_filters = deepcopy(tmp_dataset.default_filters)
            if new_default_filters is None:
                new_default_filters = {}
            for key, value in task_output["new_filters"].items():
                new_default_filters[key] = value
            tmp_dataset.default_filters = new_default_filters
        # Update dataset metadata / history
        tmp_dataset.history.append(task_function.__name__)

        print(f"AFTER RUNNING {task_function.__name__}:")
        print(pjson(tmp_dataset.dict()))
        print("\n" + "-" * 88 + "\n")


if __name__ == "__main__":
    # Define tasks
    tasks = {
        1: dict(
            function=create_ome_zarr,
        ),
        2: dict(
            function=yokogawa_to_zarr,
            meta=dict(parallel=True),
        ),
        3: dict(
            function=illumination_correction,
            meta=dict(parallel=True),
        ),
        4: dict(
            function=cellpose_segmentation,
            meta=dict(parallel=True),
        ),
    }

    # Define single dataset
    dataset = Dataset(id=123, root_dir="/tmp/somewhere/")

    # Define workflow
    wf_task_list = [
        dict(task_id=1, args=dict(image_dir="/tmp/input_images")),
        dict(task_id=2, args={}),
        dict(task_id=3, args={}),
        dict(task_id=4, args={}),
    ]

    # Clear root directory of dataset 7
    if os.path.isdir(dataset.root_dir):
        shutil.rmtree(dataset.root_dir)

    apply_workflow(wf_task_list=wf_task_list, tasks=tasks, dataset=dataset)
