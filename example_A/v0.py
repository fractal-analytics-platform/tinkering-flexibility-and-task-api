from typing import Optional
from typing import Any


def my_task(
        *,

        # Main arguments
        # The crucial one: where is the relevant Zarr store
        zarr_path: str,
        # A catch-all metadata argument - TBD
        metadata: dict[str, Any],
        # A generic overwrite flag
        overwrite: bool = False,
        # An argument for allowing data branching (behavior TBD, see below)
        output_zarr_path: Optional[str] = None,
        # Possibly needed to write history into OME-Zarrs
        history_item: Any,

        # TBD for regions-within-array arguments. Notes:
        #   1. Argument names may need a common prefix (naive example:
        #      `internal_`).
        #   2. Additional logic is required _within the task_ to check that
        #      chunking is appropriate. This cannot be enforced from the task
        #      API (although we can in principle offer a `safe` boolean
        #      argument, but that is still not strict).

        # Regions within array, option 1
        ROI: Optional[str] = None,             # is it string or int?
        T_slice: Optional[int] = None,         # example: 1
        Z_plane: Optional[int] = None,         # example: 10
        channel: Optional[int] = None,
        # How does `channel` work?
        #   * Channel OME-NGFF name (e.g. "0")?
        #   * Channel label from omero _transitional_ metadata? (e.g. "DAPI")?
        # Regions within array, option 2: lists rather than single elements
        ROI_list: Optional[list[str]] = None,
        T_slice_list: Optional[list[int]] = None,
        Z_plane_list: Optional[list[str]] = None,
        channel_list: Optional[list[str]] = None,
        ):
    pass

    # zarr_path
    # Full path to a local/s3 zarr group.
    #
    # 1. Valid examples:
    #  * /tmp/plate.zarr
    #  * /tmp/plate.zarr/B/03
    #  * /tmp/plate.zarr/B/03/0
    #  * s3://archive-bucket/plate.zarr
    #  * s3://archive-bucket/plate.zarr/B/03/
    #  * s3://archive-bucket/plate.zarr/B/03/0/
    #  * s3://archive-bucket/my_group.zarr
    # 2. Access to s3 zarr likely requires additional env variables - TBD
    # 3. Do we prefer to keep zarr_path split into something+component?
    #    I guess we don't - but this would limit flexibility of parallelizing
    #    on something which is not path-defined (e.g time sequences,
    #    sometime in the future).

    # output_zarr_path
    # Full path to an output zarr group.
    #
    # 1. Same valid examples as zarr_path.
    # 2. As usual, it requires overwrite checks.
    # 3. It is often None, as the same zarr group is used for I/O.
    # 4. When it is not None, there are a bunch of preliminary operations that
    #    need to be performed somewhere (e.g. creating the hierarchy, copying
    #    ROI tables and metadata, ...). TBD: where are these done? Is there
    #    always a copy-ome-zarr task before using output_zarr_path?
    # 5. When output_zarr_path is provided, it must be at the same hierarchy
    #    level as zarr_path, as in
    #    > zarr_path = /tmp/plate.zarr/B/03/0
    #    > zarr_path_output = /tmp/plate.zarr/B/03/0_registered
    #    This is a logical requirement, and not something that can be enforced.
    #    The reason is related to valid scenarios that would otherwise fail:
    #    > zarr_path = /tmp/plate.zarr/B/03/0
    #    > zarr_path_output = /tmp/plate.zarr/B/03/0/projections/2D/
    #    or
    #    > zarr_path = /tmp/plate.zarr/B/03/0
    #    > zarr_path_output = /tmp/testing_data/plate.zarr/B/03/0


def parallelize_over_images():

    # One well
    zarr_path_list = [
            "/tmp/plate.zarr/A/1/0"
            ]
    print(zarr_path_list)

    # Two wells
    zarr_path_list = [
            "/tmp/plate.zarr/A/1/0",
            "/tmp/plate.zarr/A/2/0",
            ]
    print(zarr_path_list)

    # How did we prepare those list?

    # One option: dataset has a parent directory, and top-level zarr name goes
    # into components
    dataset_root_folder = "/tmp"
    image_subset = [
            "plate.zarr/A/1/0",
            "plate.zarr/A/2/0",
            ]
    zarr_path_list = [
            f"{dataset_root_folder}/{image}"
            for image in image_subset
            ]

    # Another option -> this requires identifying a dataset with a single
    # top-level zarr (be it a plate, well, image, ...)
    dataset_zarr_path = "/tmp/plate.zarr"
    image_subset = [
            "A/1/0",
            "A/2/0",
            ]
    zarr_path_list = [
            f"{dataset_zarr_path}/{image}"
            for image in image_subset
            ]

    # How could we parallelize over anything else than paths?
