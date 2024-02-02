from typing import Any


def task_with_no_zarr_image_input(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    # Arbitrary task-specific parameter
    image_dir: str,  # Raw-image folder
):
    pass


task_with_no_zarr_image_input(
    root_dir="/my-output-dir/",
    image_dir="/my-image-dir/",
)


def parallel_processing_task(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    path: str,  # Relative path to NGFF image within root_dir
    buffer: dict[str, Any],  # Used to receive information from an "init" task
    # Arbitrary task-specific parameter
    some_parameter: int,
):
    pass


task_with_no_zarr_image_input(
    root_dir="/my-output-dir/",
    path="my_plate.zarr/A/01/0",
    buffer={"some": "important information"},
    some_parameter=1,
)


def multi_image_input_task(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    paths: list[str],  # Relative paths to NGFF images within root_dir
    buffer: dict[str, Any],  # Used to receive information from an "init" task
    # Arbitrary task-specific parameter
    some_parameter: int,
):
    pass


multi_image_input_task(
    root_dir="/my-output-dir/",
    paths=["my_plate.zarr/A/01/0", "my_plate.zarr/A/02/0"],
    buffer={"some": "important information"},
    some_parameter=1,
)
