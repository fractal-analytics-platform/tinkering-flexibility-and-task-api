from typing import Any
from typing import Callable
from typing import Literal
from typing import Optional

from filters import FilterSet
from images import SingleImage
from pydantic import BaseModel
from pydantic import Field


KwargsType = dict[str, Any]


class Dataset(BaseModel):
    id: Optional[int] = None
    history: list[dict[str, Any]] = []
    # New in v2
    root_dir: str
    images: list[SingleImage] = Field(default_factory=list)
    filters: FilterSet = Field(default_factory=dict)
    # Temporary state
    buffer: Optional[dict[str, Any]] = None
    parallelization_list: Optional[list[dict[str, Any]]] = None
    # Removed from V1
    # resource_list (relationship)

    @property
    def image_paths(self) -> list[str]:
        return [image["path"] for image in self.images]


class Task(BaseModel):
    function: Callable  # mock of task.command
    meta: dict[str, Any] = Field(default_factory=dict)
    new_filters: FilterSet = Field(default_factory=dict)
    task_type: Literal["non_parallel", "parallel"] = "non_parallel"

    @property
    def name(self) -> str:
        return self.function.__name__


class WorkflowTask(BaseModel):
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    task: Optional[Task] = None
    filters: FilterSet = Field(default_factory=dict)


class Workflow(BaseModel):
    task_list: list[WorkflowTask] = Field(default_factory=list)
