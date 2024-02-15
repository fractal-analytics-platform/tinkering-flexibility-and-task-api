from typing import Any
from task_function import task_function_legacy


def init_task(
    images: list[dict[str, Any]],
    filters: dict[str, Any],
) -> list[str]:
    image_paths = []
    for image in images:
        skip = False
        for key, value in filters.items():
            if image.get(key, False) != value:
                skip = True
                break
        if skip:
            continue
        image_paths.append(image["path"])
    return image_paths


def run_parallel_task_in_fractal_server():
    # (1) Mock database objects for a single parallel task
    IMAGES = [
        dict(path="plate.zarr/A/01/0"),
        dict(path="plate.zarr/A/02/0"),
        dict(path="plate.zarr/A/01/0_corr", illum_corr=True),
        dict(path="plate.zarr/A/02/0_corr", illum_corr=True),
    ]
    task = dict(
        function=task_function_legacy,  # mock of `task.command`
        parallelization_level="image",
    )
    input_dataset = dict(
        paths=["/somewhere"],
        images=IMAGES,
        metadata=dict(),
    )
    output_dataset = dict(paths=["/somewhere_else"])

    # (2) Construct parallelization list
    component_list = init_task(
        images=input_dataset["images"], filters=dict(illum_corr=True)
    )

    # (3) Run task
    for component in component_list:
        task["function"](
            input_paths=input_dataset["paths"],
            output_path=output_dataset["paths"][0],
            metadata=input_dataset["metadata"],
            component=component,
        )

    # (4) Update output_dataset["metadata"]
    # Skipping for now..


if __name__ == "__main__":
    run_parallel_task_in_fractal_server()
