from typing import Any
from typing import Optional

from filters import FilterSet
from models import Dataset
from models import Task
from models import Workflow
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
    new_images = [dict(path=f"{path}_new", processed=True)]
    return dict(new_images=new_images)


def print_path(root_dir: str, path: str, buffer: dict[str, Any], custom_parameter: int = 1) -> dict[str, Any]:
    print(f"{path=}")
    return {}


dataset = Dataset(id=1, root_dir="/invalid")
wf = Workflow(
    id=1,
    task_list=[
        WorkflowTask(
            id=1,
            task_id=1,
            task=Task(
                id=1,
                task_type="non_parallel",
                function=create_images_from_scratch,
            ),
        ),
        # a, b, c
        WorkflowTask(
            id=2,
            task_id=2,
            task=Task(id=2, task_type="parallel", function=edit_images, new_filters=dict(key="value")),
        ),
        # a, b, c all with key=value
        # dataset.filters key=value
        WorkflowTask(
            id=4,
            task_id=4,
            task=Task(
                id=4,
                task_type="parallel",
                function=copy_and_edit_image,
            ),
        ),
        # a, b, c all with key=value
        # d, e, f
        # dataset.filters key=value
        WorkflowTask(
            id=3,
            task_id=3,
            task=Task(
                id=3,
                task_type="parallel",
                function=print_path,
            ),
        ),
    ],
)
apply_workflow(wf_task_list=wf.task_list, dataset=dataset)
