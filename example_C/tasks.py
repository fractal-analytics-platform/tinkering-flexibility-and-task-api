from typing import Any
from typing import Optional
from pathlib import Path


def create_ome_zarr(
    image_folder: str,
    root_dir: str,
) -> dict:
    
    # Based on images in image_folder, create plate OME-Zarr
    Path(root_dir).mkdir(parents=True)
    plate_zarr_name = "my_plate.zarr"
    zarr_path = (Path(root_dir) / plate_zarr_name).as_posix()
    with open(zarr_path, "w") as f:
        f.write("This is an OME-Zarr container.\n")

    print("[create_ome_zarr] START")
    print(f"[create_ome_zarr] {image_folder=}")
    print(f"[create_ome_zarr] {root_dir=}")
    print(f"[create_ome_zarr] {zarr_path=}")

    out = dict(
        images=[
            dict(path=f"{plate_zarr_name}/A/01/0"),
            dict(path=f"{plate_zarr_name}/A/02/0"),
        ],
        buffer=dict(
            image_raw_paths={
                f"{plate_zarr_name}/A/01/0": f"{image_folder}/figure_A01.tiff",
                f"{plate_zarr_name}/A/02/0": f"{image_folder}/figure_A02.tiff",
            },
        ),
    )
    print("[create_ome_zarr] END")
    return out

def yokogawa_to_zarr(
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


def illumination_correction(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print(
        "Now running task with:\n"
        f"  {zarr_path=}\n"
        f"  {output_path=}\n"
    )


def copy_ome_zarr(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print(
        "Now running task with:\n"
        f"  {zarr_path=}\n"
        f"  {output_path=}\n"
    )

def maximum_intensity_projection(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print(
        "Now running task with:\n"
        f"  {zarr_path=}\n"
        f"  {output_path=}\n"
    )

def cellpose_segmentation(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
):
    print(
        "Now running task with:\n"
        f"  {zarr_path=}\n"
        f"  {output_path=}\n"
    )
