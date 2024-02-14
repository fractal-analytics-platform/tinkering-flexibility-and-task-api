from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional

from termcolor import cprint


def print(x):
    return cprint(x, "cyan")


def create_ome_zarr(
    *,
    # Standard arguments
    paths: list[str],
    buffer: Optional[dict[str, Any]] = None,
    # Task-specific arguments
    zarr_dir: str,
    image_dir: str,
) -> dict:
    """
    TBD

    Args:
        image_dir: Absolute path to images folder.
        zarr_dir: Absolute path to parent folder for plate-level Zarr.
    """

    if len(paths) > 0:
        raise RuntimeError(f"Something wrong in create_ome_zarr. {paths=}")


    # Based on images in image_folder, create plate OME-Zarr
    zarr_dir = zarr_dir.rstrip("/")
    plate_zarr_name = "my_plate.zarr"
    Path(zarr_dir).mkdir(parents=True)
    zarr_path = (Path(zarr_dir) / plate_zarr_name).as_posix()

    print("[create_ome_zarr] START")
    print(f"[create_ome_zarr] {image_dir=}")
    print(f"[create_ome_zarr] {zarr_dir=}")
    print(f"[create_ome_zarr] {zarr_path=}")

    # Create (fake) OME-Zarr folder on disk
    Path(zarr_path).mkdir()

    # Create well/image OME-Zarr folders on disk
    image_relative_paths = ["A/01/0", "A/02/0"]
    for image_relative_path in image_relative_paths:
        (Path(zarr_path) / image_relative_path).mkdir(parents=True)

    # Prepare output metadata
    out = dict(
        new_images=[
            dict(
                path=f"{zarr_dir}/{plate_zarr_name}/{image_relative_path}",
                well="_".join(image_relative_path.split("/")[:2]),
            )
            for image_relative_path in image_relative_paths
        ],
        buffer=dict(
            image_raw_paths={
                f"{zarr_dir}/{plate_zarr_name}/A/01/0": f"{image_dir}/figure_A01.tif",
                f"{zarr_dir}/{plate_zarr_name}/A/02/0": f"{image_dir}/figure_A02.tif",
            },
        ),
        new_filters=dict(
            plate=plate_zarr_name,
        ),
    )
    print("[create_ome_zarr] END")
    return out


def yokogawa_to_zarr(
    *,
    # Standard arguments
    path: str,
    buffer: dict[str, Any],
) -> dict:
    """
    TBD

    Args:
        path: Absolute image path         
    """

    print("[yokogawa_to_zarr] START")
    print(f"[yokogawa_to_zarr] {path=}")

    source_data = buffer["image_raw_paths"][path]
    print(f"[yokogawa_to_zarr] {source_data=}")

    # Write fake image data into image Zarr group
    with (Path(path) / "data").open("w") as f:
        f.write(f"Source data: {source_data}\n")

    print("[yokogawa_to_zarr] END")
    return {}


def illumination_correction(
    *,
    # Standard arguments
    path: str,
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    subsets: Optional[dict[Literal["T_index", "C_index", "Z_index"], int]] = None,
    overwrite_input: bool = False,
) -> dict:
    print("[illumination_correction] START")
    print(f"[illumination_correction] {path=}")
    print(f"[illumination_correction] {overwrite_input=}")
    print(f"[illumination_correction] {subsets=}")

    if overwrite_input:
        out = dict(edited_images=[dict(path=path)])

    else:
        new_path = f"{path}_corr"
        print(f"[illumination_correction] {new_path=}")
        out = dict(new_images=[dict(path=new_path)])
    print(f"[illumination_correction] {out=}")
    print("[illumination_correction] END")
    return out


def cellpose_segmentation(
    *,
    # Standard arguments
    path: str,
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    default_diameter: int = 100,
) -> dict:
    print("[cellpose_segmentation] START")
    print(f"[cellpose_segmentation] {path=}")

    out = dict()
    print(f"[cellpose_segmentation] {out=}")
    print("[cellpose_segmentation] END")
    return out


def new_ome_zarr(
    *,
    # Standard arguments
    paths: list[str],
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    suffix: str = "new",
    project_to_2D: bool = True,
) -> dict:

    shared_plates = []
    shared_root_dirs = []
    for path in paths:
        tmp = path.split(".zarr/")[0]
        shared_root_dirs.append("/".join(tmp.split("/")[:-1]))
        shared_plates.append(tmp.split("/")[-1] + ".zarr")
        
        
    if len(set(shared_plates)) > 1 or len(set(shared_root_dirs)) > 1:
        raise ValueError
    shared_plate = list(shared_plates)[0]
    shared_root_dir = list(shared_root_dirs)[0]

    print("[new_ome_zarr] START")
    print(f"[new_ome_zarr] Identified {shared_plate=}")
    print(f"[new_ome_zarr] Identified {shared_root_dir=}")

    assert shared_plate.endswith(".zarr")
    new_plate_zarr_name = shared_plate.strip(".zarr") + f"_{suffix}.zarr"
    print(f"[new_ome_zarr] {new_plate_zarr_name=}")

    # Based on images in image_folder, create plate OME-Zarr
    zarr_path = (Path(shared_root_dir) / new_plate_zarr_name).as_posix()

    print(f"[new_ome_zarr] {zarr_path=}")

    # Create (fake) OME-Zarr folder on disk
    Path(zarr_path).mkdir()

    # Create well/image OME-Zarr for the new copy
    image_relative_paths = ["A/01/0", "A/02/0"]
    for image_relative_path in image_relative_paths:
        (Path(zarr_path) / image_relative_path).mkdir(parents=True)

    # Prepare output metadata
    out = dict(
        new_images=[
            dict(path=f"{new_plate_zarr_name}/{image_relative_path}") for image_relative_path in image_relative_paths
        ],
        new_filters=dict(plate=new_plate_zarr_name),
        buffer=dict(
            new_ome_zarr=dict(
                old_plate=shared_plate,
                new_plate=new_plate_zarr_name,
            )
        ),
    )
    print("[new_ome_zarr] END")
    return out


def copy_data(
    *,
    # Standard arguments
    path: str,
    buffer: dict[str, Any],  # Used to receive information from an "init" task
) -> dict[str, Any]:

    old_plate = buffer["new_ome_zarr"]["old_plate"]
    new_plate = buffer["new_ome_zarr"]["new_plate"]
    old_path = path.replace(new_plate, old_plate)
    zarr_dir = Path(path).parent
    old_zarr_path = Path(zarr_dir) / old_path
    new_zarr_path = Path(zarr_dir) / path

    print("[copy_data] START")
    print(f"[copy_data] {old_zarr_path=}")
    print(f"[copy_data] {new_zarr_path=}")
    print("[copy_data] END")

    out = {}
    return out


def maximum_intensity_projection(
    *,
    # Standard arguments
    path: str,  # Absolute path to NGFF image
    buffer: dict[str, Any],  # Used to receive information from an "init" task
) -> dict[str, Any]:
    old_plate = buffer["new_ome_zarr"]["old_plate"]
    new_plate = buffer["new_ome_zarr"]["new_plate"]
    old_path = path.replace(new_plate, old_plate)
    zarr_dir = Path(path).parent
    old_zarr_path = Path(zarr_dir) / old_path
    new_zarr_path = Path(zarr_dir) / path

    print("[maximum_intensity_projection] START")
    print(f"[maximum_intensity_projection] {old_zarr_path=}")
    print(f"[maximum_intensity_projection] {new_zarr_path=}")
    print("[maximum_intensity_projection] END")

    out = dict(new_filters=dict(projected=True))
    return out


# This is a task that only serves as an init task
def init_channel_parallelization(
    *,
    # Standard arguments
    paths: list[str],
    buffer: Optional[dict[str, Any]] = None,
) -> dict:
    print("[init_channel_parallelization] START")
    print(f"[init_channel_parallelization] {paths=}")
    parallelization_list = []
    for path in paths:
        # Find out number of channels, from Zarr array shape or from NGFF metadata
        num_channels = 2  # mock
        for ind_channel in range(num_channels):
            parallelization_list.append(dict(path=path, subsets=dict(C_index=ind_channel)))
    print("[init_channel_parallelization] END")
    return dict(parallelization_list=parallelization_list)


def create_ome_zarr_multiplex(
    *,
    # Standard arguments
    paths: list[str],
    buffer: Optional[dict[str, Any]] = None,
    # Task-specific arguments
    image_dir: str,
    zarr_dir: str,
) -> dict:
    if len(paths) > 0:
        raise RuntimeError(f"Something wrong in create_ome_zarr_multiplex. {paths=}")

    # Based on images in image_folder, create plate OME-Zarr
    zarr_dir = zarr_dir.rstrip("/")
    Path(zarr_dir).mkdir(parents=True)
    plate_zarr_name = "my_plate.zarr"
    zarr_path = (Path(zarr_dir) / plate_zarr_name).as_posix()

    print("[create_ome_zarr_multiplex] START")
    print(f"[create_ome_zarr_multiplex] {image_dir=}")
    print(f"[create_ome_zarr_multiplex] {zarr_dir=}")
    print(f"[create_ome_zarr_multiplex] {zarr_path=}")

    # Create (fake) OME-Zarr folder on disk
    Path(zarr_path).mkdir()

    # Create well/image OME-Zarr folders on disk
    image_relative_paths = [f"{well}/{cycle}" for well in ["A/01", "A/02"] for cycle in ["0", "1", "2"]]
    for image_relative_path in image_relative_paths:
        (Path(zarr_path) / image_relative_path).mkdir(parents=True)

    # Prepare output metadata
    out = dict(
        new_images=[
            dict(
                path=f"{zarr_path}/{image_relative_path}",
                well="_".join(image_relative_path.split("/")[:2]),
            )
            for image_relative_path in image_relative_paths
        ],
        buffer=dict(
            image_raw_paths={
                f"{zarr_path}/A/01/0": f"{image_dir}/figure_A01_0.tif",
                f"{zarr_path}/A/01/1": f"{image_dir}/figure_A01_1.tif",
                f"{zarr_path}/A/01/2": f"{image_dir}/figure_A01_2.tif",
                f"{zarr_path}/A/02/0": f"{image_dir}/figure_A02_0.tif",
                f"{zarr_path}/A/02/1": f"{image_dir}/figure_A02_1.tif",
                f"{zarr_path}/A/02/2": f"{image_dir}/figure_A02_2.tif",
            },
        ),
        new_filters=dict(
            plate=plate_zarr_name,
        ),
    )
    print("[create_ome_zarr] END")
    return out


# This is a task that only serves as an init task
def init_registration(
    *,
    # Standard arguments
    paths: list[str],
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    ref_cycle_name: str,
) -> dict:

    print("[init_registration] START")
    print(f"[init_registration] {paths=}")

    # Detect plate prefix
    shared_plates = []
    shared_root_dirs = []
    for path in paths:
        tmp = path.split(".zarr/")[0]
        shared_root_dirs.append("/".join(tmp.split("/")[:-1]))
        shared_plates.append(tmp.split("/")[-1] + ".zarr")
        
        
    if len(set(shared_plates)) > 1 or len(set(shared_root_dirs)) > 1:
        raise ValueError
    shared_plate = list(shared_plates)[0]
    shared_root_dir = list(shared_root_dirs)[0]
    
    print(f"[init_registration] Identified {shared_plate=}")
    print(f"[init_registration] Identified {shared_root_dir=}")

    ref_cycles_per_well = {}
    x_cycles_per_well = {}
    wells = []
    for path in paths:
        path_splits = path.lstrip(f"{shared_root_dir}/{shared_plate}").strip("/").split("/")
        well = "/".join(path_splits[0:2])
        wells.append(well)
        image = path_splits[2]
        if image == ref_cycle_name:
            assert well not in ref_cycles_per_well.keys()
            ref_cycles_per_well[well] = path
        else:
            cycles = x_cycles_per_well.get(well, [])
            cycles.append(path)
            x_cycles_per_well[well] = cycles

    parallelization_list = []
    for well in sorted(set(wells)):
        print(f"[init_registration] {well=}")
        ref_path = ref_cycles_per_well[well]
        for path in x_cycles_per_well[well]:
            parallelization_list.append(
                dict(
                    path=path,
                    ref_path=ref_path,
                )
            )

    print("[init_registration] END")
    return dict(parallelization_list=parallelization_list)
