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
            dict(path=f"{plate_zarr_name}/{image_relative_path}")
            for image_relative_path in image_relative_paths
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

    source_data = buffer["image_raw_paths"][component]
    print(f"[yokogawa_to_zarr] {source_data=}")

    # Write fake image data into image Zarr group
    with (Path(root_dir) / component / "data").open("w") as f:
        f.write(f"Source data: {source_data}\n")

    print("[yokogawa_to_zarr] END")
    return {}


def illumination_correction(
    *,
    root_dir: str,
    component: str,
    buffer: Optional[dict[str, Any]] = None,
) -> dict:
    print("[illumination_correction] START")
    print(f"[illumination_correction] {root_dir=}")
    print(f"[illumination_correction] {component=}")

    new_component = f"{component}_corr"
    print(f"[illumination_correction] {new_component=}")

    out = dict(
        new_images=[
            dict(path=new_component, illumination_correction=True),
        ],
        new_filters=dict(illumination_correction=True),
    )
    print(f"[illumination_correction] {out=}")
    print("[illumination_correction] END")
    return out
