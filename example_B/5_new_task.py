from typing import Any
from task_function import task_function_new
import itertools


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

        # Parallelize over TCZ
        image_group_path = image["path"]  # noqa
        list_arguments.append(dict(zarr_path=image_group_path))

    return list_arguments


def run_parallel_task_in_fractal_server():
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
