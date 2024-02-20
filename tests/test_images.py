import pytest
from images import find_image_by_path
from images import SingleImage
from images import ScalarDict

def test_find_image_by_path():
    images = [
        SingleImage(path="a", attributes=ScalarDict(name="a")),
        SingleImage(path="b")
    ]

    image = find_image_by_path(path="a", images=images)
    assert image.attributes["name"] == "a"

    with pytest.raises(ValueError):
        find_image_by_path(path="invalid", images=images)
