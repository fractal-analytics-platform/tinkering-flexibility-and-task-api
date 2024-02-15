from typing import Any
from typing import Optional


# Type 1
def task_with_no_zarr_image_input(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    # Arbitrary task-specific parameter
    image_dir: str,  # Raw-image folder
):
    pass


# Example (e.g. converter init task)
task_with_no_zarr_image_input(
    root_dir="/my-zarr-dir/",
    image_dir="/my-image-dir/",
)


# Type 2
def parallel_processing_task(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    path: str,  # Relative path to NGFF image within root_dir
    buffer: dict[str, Any],  # Used to receive information from an "init" task
    subsets: Optional[dict[str, Any]] = None,
    # Arbitrary task-specific parameter
    some_parameter: int,
):
    pass


# Example (illumination correction)
for C_index in [
    0,
    1,
    2,
    3,
]:  # <-- this list would be prepared in a custom init task
    task_with_no_zarr_image_input(
        root_dir="/my-zarr-dir/",
        path="my_plate.zarr/A/01/0",
        subsets={"C_index": C_index},
        background=100,
    )

# Example (Cellpose segmentation)
for T_index in [
    0,
    1,
    2,
    3,
]:  # <-- this list would be prepared in a custom init task
    task_with_no_zarr_image_input(
        root_dir="/my-zarr-dir/",
        path="my_plate.zarr/A/01/0",
        subsets={"T_index": T_index},
        default_diameter=1,
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


# Example (a path acting at the well leve)
multi_image_input_task(
    root_dir="/my-zarr-dir/",
    paths=[
        "my_plate.zarr/A/01/0",
        "my_plate.zarr/A/01/1",
        "my_plate.zarr/A/01/2",
        "my_plate.zarr/A/01/3",
    ],
    buffer={"some": "important information"},
    some_parameter=1,
)
