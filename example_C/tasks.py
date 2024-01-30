from pathlib import Path
from typing import Any
from typing import Optional


def create_ome_zarr(
    *,
    root_dir: str,
    image_dir: str,
) -> dict:
    """
    TBD

    Args:
        root_dir: Absolute path to parent folder for plate-level Zarr.
        image_dir: Absolute path to images folder.
    """
    # Based on images in image_folder, create plate OME-Zarr
    Path(root_dir).mkdir(parents=True)
    plate_zarr_name = "my_plate.zarr"
    zarr_path = (Path(root_dir) / plate_zarr_name).as_posix()
    with open(zarr_path, "w") as f:
        f.write("This is an OME-Zarr container.\n")

    print("[create_ome_zarr] START")
    print(f"[create_ome_zarr] {image_dir=}")
    print(f"[create_ome_zarr] {root_dir=}")
    print(f"[create_ome_zarr] {zarr_path=}")

    out = dict(
        images=[
            dict(path=f"{plate_zarr_name}/A/01/0"),
            dict(path=f"{plate_zarr_name}/A/02/0"),
        ],
        buffer=dict(
            image_raw_paths={
                f"{plate_zarr_name}/A/01/0": f"{image_dir}/figure_A01.tif",
                f"{plate_zarr_name}/A/02/0": f"{image_dir}/figure_A02.tif",
            },
        ),
    )
    print("[create_ome_zarr] END")
    return out


def yokogawa_to_zarr(
    *,
    root_dir: str,
    component: str,
    buffer: dict[str, Any],
) -> dict:
    """
    TBD

    Args:
        root_dir: Absolute path to parent folder for plate-level Zarr.
        component:
        Relative image path within `root_dir`, e.g.`"plate.zarr/A/01/0"".
    """

    print("[yokogawa_to_zarr] START")
    print(f"[yokogawa_to_zarr] {root_dir=}")
    print(f"[yokogawa_to_zarr] {component=}")
    print(f"[yokogawa_to_zarr] {buffer.keys()=}")
    print(f"[yokogawa_to_zarr] {buffer['image_raw_paths']=}")
    print("[yokogawa_to_zarr] END")
    return {}


def illumination_correction(
    *,
    root_dir: str,
    component: str,
    buffer: dict[str, Any],
    output_path: Optional[str] = None,
) -> dict:
    print("[yokogawa_to_zarr] START")
    print(f"[yokogawa_to_zarr] {root_dir=}")
    print(f"[yokogawa_to_zarr] {component=}")
    print("[yokogawa_to_zarr] END")
    return {}
    # print("Now running task with:\n" f"
    # {zarr_path=}\n" f"  {output_path=}\n")


def copy_ome_zarr(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print("Now running task with:")
    print(f"{zarr_path=}\n" f"  {output_path=}\n")


def maximum_intensity_projection(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print("Now running task with:\n" f"  {zarr_path=}\n" f"  {output_path=}\n")


def cellpose_segmentation(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print("Now running task with:\n" f"  {zarr_path=}\n" f"  {output_path=}\n")
