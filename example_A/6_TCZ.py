from typing import Any
from task_function import task_function_new
import itertools


def init_task(
    images: list[dict[str, Any]],
    filters: dict[str, Any],
    include_T: bool = False,
    include_C: bool = False,
    include_Z: bool = False,
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
        if not any([include_T, include_C, include_Z]):
            list_arguments.append(dict(zarr_path=image_group_path))
        else:
            # Extract array shape
            # array = da.from_zarr(f"{image_group_path}/0")  # Load high-res data
            # array_shape = array.shape
            array_shape = [
                2,
                2,
                2,
                1000,
                1000,
            ]  # mock version, not representing all cases

            # Extract array axes from NGFF metadata
            # image_meta = load_ngff_meta(image_group_path)
            # T_axis_index = image_meta.T_axis_index
            T_axis_index = 0  # mock version, not representing all cases
            # C_axis_index = image_meta.C_axis_index
            C_axis_index = 1  # mock version, not representing all cases
            # Z_axis_index = image_meta.Z_axis_index
            Z_axis_index = 2  # mock version, not representing all cases

            list_T = [None]
            if include_T:
                list_T = range(array_shape[T_axis_index])
                # Check whether image_array.chunks[T_axis_index] == 1, or do something
            list_C = [None]
            if include_C:
                list_C = range(array_shape[C_axis_index])
                # Check whether image_array.chunks[C_axis_index] == 1, or do something
            list_Z = [None]
            if include_Z:
                list_Z = range(array_shape[Z_axis_index])
                # Check whether image_array.chunks[Z_axis_index] == 1, or do something

            for T_index, C_index, Z_index in itertools.product(list_T, list_C, list_Z):
                kwargs = dict(zarr_path=image["path"])
                if T_index is not None:
                    kwargs["T_index"] = T_index
                if C_index is not None:
                    kwargs["C_index"] = C_index
                if Z_index is not None:
                    kwargs["Z_index"] = Z_index
                list_arguments.append(kwargs)

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

    # (2) Construct parallelization list (THIS MUST RUN WITHIN A TASK)
    list_arguments = init_task(
        images=input_dataset["images"],
        filters=dict(illum_corr=True),
        include_T=True,
    )

    # (3) Run task
    for kwargs in list_arguments:
        task["function"](**kwargs, metadata={})

    # (4) Update output_dataset["metadata"]
    # Skipping for now..


if __name__ == "__main__":
    run_parallel_task_in_fractal_server()
