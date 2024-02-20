from typing import Any
from typing import Callable
from typing import Literal
from typing import Optional

from images import ScalarDict
from images import SingleImage
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

KwargsType = dict[str, Any]


class Dataset(BaseModel):
    id: Optional[int] = None
    history: list[dict[str, Any]] = []
    # New in v2
    root_dir: str
    images: list[SingleImage] = Field(default_factory=list)
    filters: ScalarDict = Field(default_factory=dict)
    # Temporary state
    buffer: Optional[dict[str, Any]] = None
    parallelization_list: Optional[list[dict[str, Any]]] = None
    # Removed from V1
    # resource_list (relationship)

    @property
    def image_paths(self) -> list[str]:
        return [image.path for image in self.images]


class Task(BaseModel):
    function: Callable  # mock of task.command
    meta: dict[str, Any] = Field(default_factory=dict)
    new_filters: dict[str, Any] = Field(default_factory=dict)  # FIXME: this is not using ScalarDict any more!
    task_type: Literal["non_parallel", "parallel"] = "non_parallel"

    def callable(self, **kwargs):
        return self.function(**kwargs)

    @validator("new_filters")
    def scalar_filters(cls, v):
        """
        Check that values of new_filters are all JSON-scalar.

        Replacement for `new_filters: ScalarDict` attribute type, which
        does not work in Pydantic.
        """
        for value in v.values():
            if type(value) not in [int, str, bool] and value is not None:
                raise ValueError(f"{value=} in new_filters has invalid type {type(value)}")

        return v

    @property
    def name(self) -> str:
        return self.function.__name__


class WorkflowTask(BaseModel):
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    task: Optional[Task] = None
    filters: ScalarDict = Field(default_factory=dict)


class Workflow(BaseModel):
    task_list: list[WorkflowTask] = Field(default_factory=list)
