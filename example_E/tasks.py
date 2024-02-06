from pathlib import Path
from typing import Any
from typing import Optional

from termcolor import cprint


def print(x):
    return cprint(x, "cyan")


def create_ome_zarr(
    *,
    # Standard arguments
    root_dir: str,
    paths: list[str],
    # Task-specific arguments
    image_dir: str,
) -> dict:
    """
    TBD

    Args:
        root_dir: Absolute path to parent folder for plate-level Zarr.
        image_dir: Absolute path to images folder.
    """

    if len(paths) > 0:
        raise RuntimeError(f"Something wrong in create_ome_zarr. {paths=}")

    # Based on images in image_folder, create plate OME-Zarr
    Path(root_dir).mkdir(parents=True)
    plate_zarr_name = "my_plate.zarr"
    zarr_path = (Path(root_dir) / plate_zarr_name).as_posix()

    print("[create_ome_zarr] START")
    print(f"[create_ome_zarr] {image_dir=}")
    print(f"[create_ome_zarr] {root_dir=}")
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
                path=f"{plate_zarr_name}/{image_relative_path}",
                well="_".join(image_relative_path.split("/")[:2]),
            )
            for image_relative_path in image_relative_paths
        ],
        buffer=dict(
            image_raw_paths={
                f"{plate_zarr_name}/A/01/0": f"{image_dir}/figure_A01.tif",
                f"{plate_zarr_name}/A/02/0": f"{image_dir}/figure_A02.tif",
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
    root_dir: str,
    path: str,
    buffer: dict[str, Any],
) -> dict:
    """
    TBD

    Args:
        root_dir: Absolute path to parent folder for plate-level Zarr.
        path:
            Relative image path within `root_dir`, e.g.`"plate.zarr/A/01/0"".
    """

    print("[yokogawa_to_zarr] START")
    print(f"[yokogawa_to_zarr] {root_dir=}")
    print(f"[yokogawa_to_zarr] {path=}")

    source_data = buffer["image_raw_paths"][path]
    print(f"[yokogawa_to_zarr] {source_data=}")

    # Write fake image data into image Zarr group
    with (Path(root_dir) / path / "data").open("w") as f:
        f.write(f"Source data: {source_data}\n")

    print("[yokogawa_to_zarr] END")
    return {}


def illumination_correction(
    *,
    # Standard arguments
    root_dir: str,
    path: str,
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    overwrite_input: bool = False,
) -> dict:
    print("[illumination_correction] START")
    print(f"[illumination_correction] {root_dir=}")
    print(f"[illumination_correction] {path=}")
    print(f"[illumination_correction] {overwrite_input=}")

    if overwrite_input:
        out = dict(edited_paths=[path])

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
    root_dir: str,
    path: str,
    buffer: Optional[dict[str, Any]] = None,
    # Non-standard arguments
    default_diameter: int = 100,
) -> dict:
    print("[cellpose_segmentation] START")
    print(f"[cellpose_segmentation] {root_dir=}")
    print(f"[cellpose_segmentation] {path=}")

    out = dict()
    print(f"[cellpose_segmentation] {out=}")
    print("[cellpose_segmentation] END")
    return out


def new_ome_zarr(
    *,
    # Standard arguments
    root_dir: str,
    paths: list[str],
    # Non-standard arguments
    suffix: str = "new",
    project_to_2D: bool = True,
) -> dict:

    shared_plate = set(path.split("/")[0] for path in paths)
    if len(shared_plate) > 1:
        raise ValueError
    shared_plate = list(shared_plate)[0]

    print("[new_ome_zarr] START")
    print(f"[new_ome_zarr] {root_dir=}")
    print(f"[new_ome_zarr] Identified {shared_plate=}")

    assert shared_plate.endswith(".zarr")
    new_plate_zarr_name = shared_plate.strip(".zarr") + f"_{suffix}.zarr"
    print(f"[new_ome_zarr] {new_plate_zarr_name=}")

    # Based on images in image_folder, create plate OME-Zarr
    zarr_path = (Path(root_dir) / new_plate_zarr_name).as_posix()

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
    )
    print("[new_ome_zarr] END")
    return out


def parallel_task(
    *,
    # Standard arguments
    root_dir: str,  # Parent folder of the main Zarr group (typically the plate one)
    path: str,  # Relative path to NGFF image within root_dir
    buffer: dict[str, Any],  # Used to receive information from an "init" task
    # Arbitrary task-specific parameter
    subsets: Optional[dict[str, Any]] = None,
    some_parameter: int = 1,
):
    pass
