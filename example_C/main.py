from typing import Any
from tasks import create_ome_zarr
from tasks import yokogawa_to_zarr
from tasks import illumination_correction
from tasks import copy_ome_zarr
from tasks import maximum_intensity_projection
from tasks import cellpose_segmentation
import shutil
import os
from devtools import debug
from copy import deepcopy



def init_task(
    images: list[dict[str, Any]],
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    list_arguments = []
    for image in images:
        # Filter images
        skip = False
        for key, value in filters.items():
            if image.get(key, False) != value:
                skip = True
                break
        if skip:
            continue

        image_group_path = image["path"]  # noqa
        list_arguments.append(dict(zarr_path=image_group_path))

    return list_arguments


def apply_workflow(
        wf_task_list: list[dict],
        tasks:dict[str, dict],
        dataset: dict,
        ):

    # Run task 0
    tmp_dataset = deepcopy(dataset)
    for wftask in wf_task_list:

        task_function = tasks[wftask["task_id"]]["function"]
        function_args = wftask["args"]
        function_args.update(dict(root_dir=tmp_dataset["root_dir"]))

        debug(task_function)

        # Parallel task
        if tasks[wftask["task_id"]].get("meta", {}).get("parallel", False):
            # FIXME: filtering
            outs = []
            buffer = tmp_dataset.pop("buffer")
            for image in tmp_dataset["images"]:
                function_args.update(
                    dict(
                        component=image["path"],
                        buffer=buffer,
                        )
                    )
                out = task_function(**function_args)
                outs.append(out)
            # TODO: merge outs
        else:
            out = task_function(**function_args)
            for image in out["images"]:
                tmp_dataset["images"].append(image)
            tmp_dataset["buffer"] = out["buffer"]
        debug(tmp_dataset)

if __name__ == "__main__":

    # Define tasks
    tasks = {
        1: dict(function=create_ome_zarr),
        2: dict(function=yokogawa_to_zarr, meta=dict(parallel=True)),
        3: dict(function=illumination_correction),
        4: dict(function=copy_ome_zarr),
        5: dict(function=maximum_intensity_projection),
        6: dict(function=cellpose_segmentation),
    }

    # Define single dataset
    dataset = dict(
        id=7,
        root_dir="/tmp/dataset_7",
        images=[],
        )

    # Define workflow
    wf_task_list = [
        dict(task_id=1, args=dict(image_folder="/tmp/images")),
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