from typing import Any
from typing import Optional

from devtools import debug
from models import Dataset
from models import FilterSet
from models import Task
from pydantic import BaseModel
from pydantic import Field
from runner import apply_workflow


class WorkflowTask(BaseModel):
    id: int
    task_id: int
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    task: Optional[Task] = None
    filters: FilterSet = Field(default_factory=dict)


def create_images_from_scratch(
    root_dir: str,
    paths: list[str],
    buffer: dict[str, Any],
) -> dict[str, Any]:
    new_images = [
        dict(path="a"),
        dict(path="b"),
        dict(path="c"),
    ]
    return dict(new_images=new_images)


def edit_images(root_dir: str, path: str, buffer: dict[str, Any], custom_parameter: int = 1) -> dict[str, Any]:
    edited_images = [dict(path=path)]
    return dict(edited_images=edited_images)


def copy_and_edit_image(
    root_dir: str,
    path: str,
    buffer: dict[str, Any],
) -> dict[str, Any]:
    new_images = [
        dict(
            path=f"{path}_new",
            processed=True,
        )
    ]
    return dict(new_images=new_images)


def test_image_attribute_propagation():
    images_pre = [
        dict(path="plate.zarr/A/01/0", plate="plate.zarr", well="A/01"),
        dict(path="plate.zarr/A/02/0", plate="plate.zarr", well="A/02"),
    ]
    dataset_pre = Dataset(
        id=1,
        root_dir="/tmp/invalid",
        images=images_pre,
    )
    wf_task_list = [
        WorkflowTask(
            id=1,
            task_id=1,
            task=Task(
                id=1,
                task_type="parallel",
                function=copy_and_edit_image,
            ),
        )
    ]
    dataset_post = apply_workflow(wf_task_list=wf_task_list, dataset=dataset_pre)
    images_post = dataset_post.images

    print()

    debug(images_pre)
    debug(images_post)

    for image in images_post:
        print(f"Now validate {image}")
        if image["path"] == "plate.zarr/A/01/0_new":
            assert image["processed"] is True
            assert image["plate"] == "plate.zarr"
            assert image["well"] == "A/01"
        elif image["path"] == "plate.zarr/A/02/0_new":
            assert image["processed"] is True
            assert image["plate"] == "plate.zarr"
            assert image["well"] == "A/02"
        else:
            assert image["plate"] == "plate.zarr"
            assert "processed" not in image.keys()
