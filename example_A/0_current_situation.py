from task_function import task_function


def run_parallel_task_in_fractal_server():

    # (1) Mock database objects for a single parallel task
    task = dict(
        function=task_function,  # mock of `task.command`
        parallelization_level="image",
        )
    input_dataset = dict(
        paths=["/somewhere"],
        metadata=dict(
            components=dict(
                plate=["plate.zarr"],
                well=["plate.zarr/A/01", "plate.zarr/A/02"],
                image=["plate.zarr/A/01/0", "plate.zarr/A/02/0"],
            )
        ),
    )
    output_dataset = dict(paths=["/somewhere_else"])

    # (2) Construct parallelization list
    input_dataset_components = input_dataset["metadata"]["components"]
    component_list = input_dataset_components[task["parallelization_level"]]

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
