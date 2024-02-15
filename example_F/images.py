# Example image
# image = {"path": "/tmp/asasd", "dimensions": 3}
# Example filters
# filters = {"dimensions": 2, "illumination_corrected": False}
from typing import Union

ImageAttribute = Union[str, bool, int, None]  # a scalar JSON object
SingleImage = dict[str, ImageAttribute]


def find_image_by_path(
    *,
    images: list[SingleImage],
    path: str,
):
    try:
        return next(image for image in images if image["path"] == path)
    except StopIteration:
        raise ValueError(f"No image with {path=} found.")
