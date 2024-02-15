from typing import Any
from typing import Callable
from typing import Literal
from typing import Optional

from filters import FilterSet
from images import SingleImage
from pydantic import BaseModel
from pydantic import Field


KwargsType = dict[str, Any]


class TaskOutput(BaseModel):
    new_images: Optional[list[SingleImage]] = None
    """List of new images added by a given task instance."""

    edited_images: Optional[list[SingleImage]] = None
    """List of images edited by a given task instance."""

    new_filters: Optional[FilterSet] = None
    """
    *Global* filters (common to all images) added by this task.

    Note: the right place for these filters would be in the task manifest,
    but this attribute is useful for the ones which determined at runtime
    (e.g. the plate name).
    """

    buffer: Optional[dict[str, Any]] = None
    """
    Metadata used for communication between an init task and its (parallel)
    companion task.
    """

    parallelization_list: Optional[list[KwargsType]] = None
    """
    Used in the output of an init task, to expose customizable parallelization
    of the companion task.
    """

    class Config:
        extra = "forbid"


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
