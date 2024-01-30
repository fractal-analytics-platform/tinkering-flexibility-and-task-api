import os
import shutil
from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from devtools import debug
from models import Dataset
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import yokogawa_to_zarr


def _filter_image_list(
    images: list[dict[str, Any]],
    filters: Optional[dict[str, Any]] = None,
) -> list[dict[str, Any]]:
    filtered_images = []
    if filters is None:
        return images
    debug(filters)
    for image in images:
        include_image = False
        for key, value in filters.items():
            if image.get(key, False) != value:
                include_image = False
                break
        if include_image:
            filtered_images.append(copy(image))
    return filtered_images


def apply_workflow(
    wf_task_list: list[dict],
    tasks: dict[str, dict],
    dataset: Dataset,
):
    # Run task 0
    tmp_dataset = deepcopy(dataset)

    for wftask in wf_task_list:
        task_function = tasks[wftask["task_id"]]["function"]
        function_args = wftask["args"]
        function_args.update(dict(root_dir=tmp_dataset.root_dir))

        debug(f"NOW RUN {task_function.__name__}")

        # Run task
        task = tasks[wftask["task_id"]]
        is_parallel = task.get("meta", {}).get("parallel", False)
        debug(is_parallel)
        if not is_parallel:
            out = task_function(**function_args)
        else:
            # FIXME: filtering
            outs = []
            for image in _filter_image_list(
                tmp_dataset.images,
                # tmp_dataset + wftask filters
            ):
                function_args.update(
                    dict(
                        component=image["path"],
                        buffer=tmp_dataset.buffer,
                    )
                )
                out = task_function(**function_args)
                outs.append(out)
            # Reset buffer after using it
            tmp_dataset.buffer = None

            # TODO: clean-up parallel metadata merge
            _new_images = []
            _new_filters = None
            debug(outs)
            for _out in outs:
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

            out = {}
            if _new_images:
                out["new_images"] = _new_images
            if _new_filters:
                out["new_filters"] = _new_filters

        # Update dataset metadata / images
        for image in out.get("new_images", []):
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
        if out.get("buffer", None) is not None:
            tmp_dataset.buffer = out["buffer"]
        # Update dataset metadata / default filters
        if out.get("new_filters", None) is not None:
            new_default_filters = deepcopy(tmp_dataset.default_filters)
            if new_default_filters is None:
                new_default_filters = {}
            for key, value in out["new_filters"].items():
                new_default_filters[key] = value
            tmp_dataset.default_filters = new_default_filters
        # Update dataset metadata / history
        tmp_dataset.history.append(task_function.__name__)

        debug(f"AFTER RUNNING {task_function.__name__}", tmp_dataset)


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
    }

    # Define single dataset
    dataset = Dataset(id=123, root_dir="/tmp/somewhere/")

    # Define workflow
    wf_task_list = [
        dict(task_id=1, args=dict(image_dir="/tmp/input_images")),
        dict(task_id=2, args={}),
        dict(task_id=3, args={}),
    ]

    # Clear root directory of dataset 7
    if os.path.isdir(dataset.root_dir):
        shutil.rmtree(dataset.root_dir)

    apply_workflow(wf_task_list=wf_task_list, tasks=tasks, dataset=dataset)
