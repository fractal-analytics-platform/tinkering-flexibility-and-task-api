from task_function import task_function_legacy


def init_task(
    parallelization_level: str,
    components: dict[str, list[str]],
) -> list[str]:
    return components[parallelization_level]


def run_parallel_task_in_fractal_server():
    # (1) Mock database objects for a single parallel task
    task = dict(
        function=task_function_legacy,  # mock of `task.command`
        parallelization_level="image",
    )
    input_dataset = dict(
        paths=["/somewhere"],
        components=dict(
            plate=["plate.zarr"],
            well=["plate.zarr/A/01", "plate.zarr/A/02"],
            image=["plate.zarr/A/01/0", "plate.zarr/A/02/0"],
        ),
        metadata=dict(),
    )
    output_dataset = dict(paths=["/somewhere_else"])

    # (2) Construct parallelization list
    component_list = init_task(
        parallelization_level=task["parallelization_level"],
        components=input_dataset["components"],
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
