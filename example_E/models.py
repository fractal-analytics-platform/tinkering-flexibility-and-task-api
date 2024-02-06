from typing import Any
from typing import Callable
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator
from tasks import cellpose_segmentation
from tasks import copy_data
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import maximum_intensity_projection
from tasks import new_ome_zarr
from tasks import yokogawa_to_zarr


SingleFilter = Union[str, bool, int, None]
FilterSet = dict[str, SingleFilter]


class Dataset(BaseModel):
    id: Optional[int] = None
    root_dir: str
    images: list[dict[str, Any]] = []
    filters: FilterSet = Field(default_factory=dict)
    buffer: Optional[dict[str, Any]] = None
    history: list[dict[str, Any]] = []


class Task(BaseModel):
    id: int
    function: Callable
    meta: dict[str, Any] = Field(default_factory=dict)
    new_default_filters: FilterSet = Field(default_factory=dict)

    task_type: Literal["non_parallel", "parallel"] = "non_parallel"

    @property
    def name(self) -> str:
        return self.function.__name__


DB_TASKS = [
    Task(id=1, function=create_ome_zarr, task_type="non_parallel"),
    Task(id=2, function=yokogawa_to_zarr, task_type="parallel"),
    Task(
        id=3,
        function=illumination_correction,
        task_type="parallel",
        new_default_filters=dict(illumination_correction=True),
    ),
    Task(id=4, function=cellpose_segmentation, task_type="parallel"),
    Task(id=5, function=new_ome_zarr, task_type="non_parallel"),
    Task(id=6, function=copy_data, task_type="parallel"),
    Task(id=7, function=maximum_intensity_projection, task_type="parallel"),
]


TASK_NAME_TO_TASK = {}
TASK_ID_TO_TASK = {}
TASK_NAME_TO_TASK_ID = {}
for _task in DB_TASKS:
    TASK_NAME_TO_TASK_ID[_task.name] = _task.id
    TASK_NAME_TO_TASK[_task.name] = _task
    TASK_ID_TO_TASK[_task.id] = _task


class WorkflowTask(BaseModel):
    id: int
    task_id: int
    args: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    task: Optional[Task] = None
    filters: FilterSet = Field(default_factory=dict)

    @root_validator()
    def set_task(cls, values):
        if values["task"] is None:
            values["task"] = TASK_ID_TO_TASK[values["task_id"]]
        return values


class Workflow(BaseModel):
    id: int
    task_list: list[WorkflowTask] = Field(default_factory=list)
