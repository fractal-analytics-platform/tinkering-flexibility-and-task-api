"""
TASK API

Non-parallel task

1. This is typically an init task (the first half of a processing task), or a plate-level processing task.
2. It takes a (possibly empty) `paths` list, with paths to OME-NGFF images.
3. In general, it also outputs Fractal-specific metadata.
3/a. If it's an "init" tasks, it typically produce a parallelization list for the next task.
3/b. If it's a converter, it typcally produces metadata for the image list (e.g. well and plate attributes).

(embarassingly) parallel task

1. It is a processing task that is applied, which benefits from some form of parallelization.
2. It takes a single `path` argument, pointing to an OME-NGFF image.
3. It takes a single, optional, `buffer` argument - with additional metadata coming from the previous task.
4. It is run in parallel over a certain list:
4/a. If there was an "init" task before the current one, the parallelization list is already defined.
4/b. If not, then the default is to use filters to select a subset of images.
5. It may or may not produce relevant metadata to feed back to Fractal.


IMAGE LIST AND FILTERS

dataset.images
New attribute with metadata-rich list of OME-NGFF images.
There may exist multiple versions (e.g. raw/corrected) of the same image.

FILTERS

This is defined in the task manifest, or in the DB task entry.
These filters are typically for a whole homogeneous subset of the image list.
task.new_filters = {"illumination_correction": True}

This is mostly automated (from within tasks), but user can modify.
dataset.filters = {"plate": "plate.zarr", "illumination_correction": True}

Higher priority option, for more custom use cases:
wftask.filters = {"projection": False}
wftask.filters = {"well": "B03"}


Filters are used BEFORE the task, to prepare the image list for parallelization.
THEN task runs:
    A. In parallel, with `path` looping over list of images' paths;
    B. Not in parallel, with the whole list provided as `paths` argument.
Dataset.filters are updated AFTER the task.
"""
from typing import Any
from typing import Optional


# Type 1: non-parallel task
def non_parallel_task(
    *,
    # Standard arguments
    paths: list[str],  # can be empty, e.g. for the converter init
    buffer: dict[str, Any],  # Used??
    # Arbitrary task-specific parameter
    image_dir: str,  # Raw-image folder
    some_parameter: int = 1,
):
    pass


# Type 2: parallel task
def parallel_task(
    *,
    # Standard arguments
    path: str,  # Absolute path to NGFF image
    buffer: dict[str, Any],  # Used to receive information from an "init" task
    # Arbitrary task-specific parameter
    subsets: Optional[dict[str, Any]] = None,
    some_parameter: int = 1,
):
    pass


###############

# Converter "compound" task
non_parallel_task(
    paths=[],  # server-provided
    image_dir="/my-image-dir/",  # user-provided
    zarr_dir="/tmp/"
)
for path in [
    "/tmp/plate.zarr/A/01/0",
    "/tmp/plate.zarr/A/02/0",
]:  # list from dataset.images
    parallel_task(
        path=path,  # server-provided
        buffer=dict(original_image_paths={...}),
    )

# Illumination correction
for path in [
    "/tmp/plate.zarr/A/01/0",
    "/tmp/plate.zarr/A/02/0",
]:  # list from dataset.images
    parallel_task(
        path=path,  # server-provided
        background=100,  # user-provided
    )


# Illumination correction - with custom parallelization
non_parallel_task(
    paths=[
        "/tmp/my_plate.zarr/A/01/0",
        "/tmp/my_plate.zarr/A/02/0",
    ],  # list from dataset.images
)
parallelization_list = [
    dict(path="/tmp/my_plate.zarr/A/01/0", subsets=dict(C_index=0)),  # channel 0 of well A/01
    dict(path="/tmp/my_plate.zarr/A/02/0", subsets=dict(C_index=0)),  # channel 0 of well A/02
    dict(path="/tmp/my_plate.zarr/A/02/0", subsets=dict(C_index=1)),  # channel 1 of well A/02
]
for kwargs in parallelization_list:
    parallel_task(
        **kwargs,  # coming from the init task
        background=100,  # user-provided
    )


# Example (Cellpose segmentation)
# SERVER-SIDE
# Start with dataset.images (DB)
# Apply filters based on dataset.filters (+ optionally wftask.filters)
# End up with filtered list of images `filtered_image_list`

# After applying filters to dataset.images, I end up with
filtered_image_list = [
    dict(path="/tmp/plate.zarr/A/01/0"),
    dict(path="/tmp/plate.zarr/A/02/0"),
]
for kwargs in filtered_image_list:
    parallel_task(
        **kwargs,  # server-provided (parallelization)
        default_diameter=1,  # user-provided
    )

# Registration (some part of it): "compound" task acting at the well level
non_parallel_task(
    paths=[
        "/tmp/my_plate.zarr/A/01/0",
        "/tmp/my_plate.zarr/A/01/1",
        "/tmp/my_plate.zarr/A/01/2",
        "/tmp/my_plate.zarr/A/02/0",
        "/tmp/my_plate.zarr/A/02/1",
        "/tmp/my_plate.zarr/A/02/2",
    ],
)
parallelization_list = [
    dict(
        path="/tmp/my_plate.zarr/A/01/1",
        ref_cycle_path="/tmp/my_plate.zarr/A/01/0",
    ),
    dict(
        path="/tmp/my_plate.zarr/A/01/2",
        ref_cycle_path="/tmp/my_plate.zarr/A/01/0",
    ),
    dict(
        path="/tmp/my_plate.zarr/A/02/1",
        ref_cycle_path="/tmp/my_plate.zarr/A/02/0",
    ),
    dict(
        path="/tmp/my_plate.zarr/A/02/2",
        ref_cycle_path="/tmp/my_plate.zarr/A/02/0",
    ),
]
for kwargs in parallelization_list:
    parallel_task(
        **kwargs,  # coming from the init task
        registration_parameter=10,  # user-provided
    )
