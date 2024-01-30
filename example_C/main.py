import os
import shutil
from copy import copy
from copy import deepcopy
from typing import Any

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
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    filtered_images = []
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

        debug(task_function)

        # Parallel task
        if tasks[wftask["task_id"]].get("meta", {}).get("parallel", False):
            # FIXME: filtering
            outs = []
            for image in _filter_image_list(
                tmp_dataset["images"],
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
                tmp_dataset["images"].append(image)
            tmp_dataset["buffer"] = out["buffer"]
        tmp_dataset.history.append(str(task_function))
        debug(tmp_dataset)


if __name__ == "__main__":

    # Define tasks
    tasks = {
        1: dict(
            name="Create OME-Zarr",
            function=create_ome_zarr,
        ),
        2: dict(
            name="Yokogawa-to-Zarr",
            function=yokogawa_to_zarr,
            meta=dict(parallel=True),
        ),
        3: dict(
            name="Illumination correction",
            function=illumination_correction,
        ),
        4: dict(
            name="Copy OME-Zarr",
            function=copy_ome_zarr,
        ),
        5: dict(
            name="MIP",
            function=maximum_intensity_projection,
        ),
        6: dict(
            name="Cellpose",
            function=cellpose_segmentation,
        ),
    }

    # Define single dataset
    dataset = Dataset(id=123, root_dir="/tmp/somewhere/")

    # Define workflow
    wf_task_list = [
        dict(task_id=1, args=dict(image_folder="/tmp/input_images")),
        dict(task_id=2, args={}),
    ]

    # Clear root directory of dataset 7
    if os.path.isdir(dataset["root_dir"]):
        shutil.rmtree(dataset["root_dir"])

    apply_workflow(wf_task_list=wf_task_list, tasks=tasks, dataset=dataset)


"""


    # (1) Mock database objects for a single parallel task
    IMAGES = [
        dict(path="plate.zarr/A/01/0"),
        dict(path="plate.zarr/A/02/0"),
        dict(path="plate.zarr/A/01/0_corr", illum_corr=True),
        dict(path="plate.zarr/A/02/0_corr", illum_corr=True),
    ]
    task = dict(
        function=task_function_new,  # mock of `task.command`
    )
    input_dataset = dict(
        paths=["/somewhere"],
        images=IMAGES,
        metadata=dict(),
    )

    # (2) Construct parallelization list
    list_arguments = init_task(
        images=input_dataset["images"],
        filters=dict(illum_corr=True),
    )

    # (3) Run task
    for kwargs in list_arguments:
        task["function"](**kwargs, metadata={})

    # (4) Update output_dataset["metadata"]
    # Skipping for now..


if __name__ == "__main__":
    run_parallel_task_in_fractal_server()
"""
