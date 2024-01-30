import os
import shutil
from copy import copy
from copy import deepcopy
from typing import Any
from typing import Optional

from devtools import debug
from models import Dataset
from tasks import cellpose_segmentation
from tasks import copy_ome_zarr
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import maximum_intensity_projection
from tasks import yokogawa_to_zarr


def _filter_image_list(
    images: list[dict[str, Any]],
    filters: Optional[dict[str, Any]] = None,
) -> list[dict[str, Any]]:
    filtered_images = []
    if filters is None:
        filters = {}
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

        # Parallel task
        if tasks[wftask["task_id"]].get("meta", {}).get("parallel", False):
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
            # TODO: merge outs
        else:
            out = task_function(**function_args)
            for image in out["images"]:
                tmp_dataset.images.append(image)
            tmp_dataset.buffer = out["buffer"]
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
        ),
        4: dict(
            function=copy_ome_zarr,
        ),
        5: dict(
            function=maximum_intensity_projection,
        ),
        6: dict(
            function=cellpose_segmentation,
        ),
    }

    # Define single dataset
    dataset = Dataset(id=123, root_dir="/tmp/somewhere/")

    # Define workflow
    wf_task_list = [
        dict(task_id=1, args=dict(image_dir="/tmp/input_images")),
        dict(task_id=2, args={}),
    ]

    # Clear root directory of dataset 7
    if os.path.isdir(dataset.root_dir):
        shutil.rmtree(dataset.root_dir)

    apply_workflow(wf_task_list=wf_task_list, tasks=tasks, dataset=dataset)
