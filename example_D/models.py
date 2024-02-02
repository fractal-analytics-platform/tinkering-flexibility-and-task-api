from typing import Any
from typing import Callable
from typing import Literal
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

    task_type: Literal["standard", "parallel", "combine_images"] = "standard"

    @property
    def name(self) -> str:
        return self.function.__name__


class WorkflowTask(BaseModel):
    id: int
    task_id: int
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    task: Task


class Workflow(BaseModel):
    id: int
    task_list: list[WorkflowTask] = Field(default_factory=list)
