from typing import Any
from typing import Optional
import itertools

IMAGE_LIST = [
    # Raw
    dict(path="/tmp/plate.zarr/A/01/0"),
    dict(path="/tmp/plate.zarr/A/01/1"),
    dict(path="/tmp/plate.zarr/A/01/2"),
    dict(path="/tmp/plate.zarr/A/02/0"),
    dict(path="/tmp/plate.zarr/A/02/1"),
    dict(path="/tmp/plate.zarr/A/02/2"),
    # Registered
    dict(path="/tmp/plate.zarr/A/01/0_reg", registered=True),
    dict(path="/tmp/plate.zarr/A/01/1_reg", registered=True),
    dict(path="/tmp/plate.zarr/A/01/2_reg", registered=True),
    dict(path="/tmp/plate.zarr/A/02/0_reg", registered=True),
    dict(path="/tmp/plate.zarr/A/02/1_reg", registered=True),
    dict(path="/tmp/plate.zarr/A/02/2_reg", registered=True),
    # MIP
    dict(path="/tmp/plate.zarr/A/01/0_reg/proj", registered=True, projected=True),
    dict(path="/tmp/plate.zarr/A/01/1_reg/proj", registered=True, projected=True),
    dict(path="/tmp/plate.zarr/A/01/2_reg/proj", registered=True, projected=True),
    dict(path="/tmp/plate.zarr/A/02/0_reg/proj", registered=True, projected=True),
    dict(path="/tmp/plate.zarr/A/02/1_reg/proj", registered=True, projected=True),
    dict(path="/tmp/plate.zarr/A/02/2_reg/proj", registered=True, projected=True),
]


def init(
    image_list_to_filter: list[dict],
    filters: dict[str, Any],
    include_T: bool = False,
    include_C: bool = False,
    include_Z: bool = False,
    ROIs: Optional[list[str]] = None,

) -> dict[str, Any]:
    args_list = []
    for image in image_list_to_filter:
        # Filter images based on flags like "registered" or "projected"
        skip = False
        for key, value in filters.items():
            if image.get(key, False) != value:
                skip = True
                break
        if skip:
            continue

        if any([include_T, include_C, include_Z, ROIs]):
            # image_group_path = path 
            # image_array_path = f"{path}/0"  # high-resolution level
            # image_meta = load_ngff_meta(image_group_path)
            # image_array = da.from_zarr(image_array_path)
            list_T = [None]
            if include_T:
                T_axis_index = 0   # This should come from image_meta
                len_T = 2          # This should come from image_array.shape
                list_T = range(len_T)
                # Check whether image_array.chunks[T_axis_index] == 1, or do something
            list_C = [None]
            if include_C:
                C_axis_index = 1   # This should come from image_meta
                len_C = 2          # This should come from image_array.shape
                list_C = range(len_C)
                # Check whether image_array.chunks[C_axis_index] == 1, or do something
            list_Z = [None]
            if include_Z:
                Z_axis_index = 1   # This should come from image_meta
                len_Z = 2          # This should come from image_array.shape
                list_Z = range(len_Z)
                # Check whether image_array.chunks[Z_axis_index] == 1, or do something
            list_ROI = [None]
            if ROIs is not None:
                list_ROI = ROIs
            for (T_index, C_index, Z_index, ROI_name) in itertools.product(list_T, list_C, list_Z, list_ROI):
                kwargs = dict(zarr_path=image["path"])
                if T_index is not None:
                    kwargs["T_index"] = T_index
                if C_index is not None:
                    kwargs["C_index"] = C_index
                if Z_index is not None:
                    kwargs["Z_index"] = Z_index
                if ROI_name is not None:
                    kwargs["ROI_name"] = ROI_name

                args_list.append(kwargs)
        else:
            args_list.append(dict(zarr_path=image["path"]))
    return dict(args_list=args_list)


def task(
    *,
    zarr_path: str,
    T_index: Optional[int] = None,
    C_index: Optional[int] = None,
    Z_index: Optional[int] = None,
    ROI_name: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
    # image_group_path = path 
    # image_array_path = f"{path}/0"  # high-resolution level
    # image_meta = load_ngff_meta(image_group_path)
    # image_array = da.from_zarr(image_array_path)
    # check axes are TCZYX
    # image_subarray = image_array
    # if T_index is not None:
    #     image_subarray = image_subarray[T_index:T_index+1]
    # if C_index is not None:
    #     image_subarray = image_subarray[:, C_index:C_index+1]
    # if Z_index is not None:
    #     image_subarray = image_subarray[:, :, Z_index:Z_index+1]
    # if ROI_name is not None:
    #     # load a ROI with name ROI_name from *some* table, and use it
    #     # to address a specific array region
    # .. and now process this TCZXY array
    pass


if __name__ == "__main__":
    # This is similar to code that would be run in fractal-server

    filters = dict(registered=True, projected=False)
    out = init(IMAGE_LIST, filters)
    components_args = out["args_list"]
    print("Filter images with {filters}")
    for single_component_args in components_args:
        print(single_component_args)
        task(**single_component_args)
    print()

    print("Same as above, but with TCZ slices")
    filters = dict(registered=True, projected=False)
    out = init(IMAGE_LIST, filters, include_T=True, include_C=True, include_Z=True)
    components_args = out["args_list"]
    for single_component_args in components_args:
        print(single_component_args)
        task(**single_component_args)
    print()

    print("Same as above, but with TCZ slices and ROIs")
    filters = dict(registered=True, projected=False)
    out = init(IMAGE_LIST, filters, include_T=True, include_C=True, include_Z=True, ROIs=["FOV_1", "FOV_2"])
    components_args = out["args_list"]
    for single_component_args in components_args:
        print(single_component_args)
        task(**single_component_args)
    print()