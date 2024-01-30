from typing import Any
from typing import Optional

from pydantic import BaseModel


class Dataset(BaseModel):
    id: Optional[int] = None
    root_dir: str
    images: list[dict[str, Any]] = []
    default_filters: Optional[dict[str, bool]] = None
    buffer: Optional[dict[str, Any]] = None
    history: list[dict[str, Any]] = []

    def filtered_images(self, wftask_filters: dict):

        filters = self.default_filters
        filters.update(wftask_filters)

        _filtered_images = []
        for image in self.images:
            if 0.5 < 0.5:
                _filtered_images.append(image)
        return _filtered_images


if __name__ == "__main__":

    # After create-ome-zarr
    ds = Dataset(
        root_dir="/tmp",
        images=[
            dict(path="plate.zarr/A/01/0"),
            dict(path="plate.zarr/A/02/0"),
        ],
        default_filters={},
        buffer=dict(
            raw_images_sources={
                "plate.zarr/A/01/0": "/tmp/input_images/figure_A01.tif",
                "plate.zarr/A/02/0": "/tmp/input_images/figure_A01.tif",
            }
        ),
        history=["create-ome-zarr"],
    )

    # After yokogawa-to-zarr
    ds = Dataset(
        root_dir="/tmp",
        images=[
            dict(path="/tmp/plate.zarr/A/01/0"),
            dict(path="/tmp/plate.zarr/A/02/0"),
        ],
        default_filters={},
        buffer={},
        history=["create-ome-zarr", "yokogawa-to-zarr"],
    )

    # Afer illumination correction
    ds = Dataset(
        root_dir="/tmp",
        images=[
            dict(path="/tmp/plate.zarr/A/01/0"),
            dict(path="/tmp/plate.zarr/A/02/0"),
            dict(
                path="/tmp/plate.zarr/A/01/0_corr", illumination_corrected=True
            ),
            dict(
                path="/tmp/plate.zarr/A/02/0_corr", illumination_corrected=True
            ),
        ],
        default_filters=dict(illumination_corr=True),
        buffer={},
        history=[
            "create-ome-zarr",
            "yokogawa-to-zarr",
            "illumination-correction",
        ],
    )

    # Pre cellpose: what is the list of images??
    ds.filtered_images()
    # that is:
    # dict(path="/tmp/plate.zarr/A/01/0_corr", illumination_corrected=True),
    # dict(path="/tmp/plate.zarr/A/02/0_corr", illumination_corrected=True),

    # Afer cellpose
    ds = Dataset(
        root_dir="/tmp",
        images=[
            dict(path="/tmp/plate.zarr/A/01/0"),
            dict(path="/tmp/plate.zarr/A/02/0"),
            dict(
                path="/tmp/plate.zarr/A/01/0_corr", illumination_corrected=True
            ),
            dict(
                path="/tmp/plate.zarr/A/02/0_corr", illumination_corrected=True
            ),
        ],
        default_filters=dict(corr=True),
        buffer={},
        history=[
            "create-ome-zarr",
            "yokogawa-to-zarr",
            "illumination-correction",
            "cellpose",
        ],
    )

    print(ds.filtered_images())
    print(ds.filtered_images(wftask_filters=dict(mip=False)))
