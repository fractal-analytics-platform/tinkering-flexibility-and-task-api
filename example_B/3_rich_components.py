from typing import Any
from task_function import task_function_legacy


def init_task(
    images: list[dict[str, Any]],
) -> list[str]:
    return [image["path"] for image in images]


def run_parallel_task_in_fractal_server():
    # (1) Mock database objects for a single parallel task
    IMAGES = [
        dict(path="plate.zarr/A/01/0"),
        dict(path="plate.zarr/A/02/0"),
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
        images=input_dataset["images"],
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
