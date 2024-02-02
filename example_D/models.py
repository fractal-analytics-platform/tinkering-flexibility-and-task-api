from typing import Any
from typing import Callable
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class Dataset(BaseModel):
    id: Optional[int] = None
    root_dir: str
    images: list[dict[str, Any]] = []
    default_filters: dict[str, bool] = Field(default_factory=dict)
    buffer: Optional[dict[str, Any]] = None
    history: list[dict[str, Any]] = []


class Task(BaseModel):
    id: int
    function: Callable
    meta: dict[str, Any] = Field(default_factory=dict)
    new_default_filters: dict[str, Union[str, bool, int, float, None]] = Field(
        default_factory=dict
    )

    @property
    def is_parallel(self):
        return self.meta.get("parallel", False)


class WorkflowTask(BaseModel):
    id: int
    task_id: int
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)


class Workflow(BaseModel):
    id: int
    task_list: list[WorkflowTask] = Field(default_factory=list)
