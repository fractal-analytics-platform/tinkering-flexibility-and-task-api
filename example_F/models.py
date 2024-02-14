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
from tasks import create_ome_zarr_multiplex
from tasks import illumination_correction
from tasks import init_channel_parallelization
from tasks import init_registration
from tasks import maximum_intensity_projection
from tasks import new_ome_zarr
from tasks import yokogawa_to_zarr

KwargsType = dict[str, Any]
ImageAttribute = Union[str, bool, int, None]  # a scalar JSON object
FilterSet = dict[str, ImageAttribute]
SingleImage = dict[str, ImageAttribute]

# Example image
# image = {"path": "/tmp/asasd", "dimensions": 3}
# Example filters
# filters = {"dimensions": 2, "illumination_corrected": False}


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
    id: int
    function: Callable  # mock of task.command
    meta: dict[str, Any] = Field(default_factory=dict)
    new_filters: FilterSet = Field(default_factory=dict)
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
        new_filters=dict(illumination_correction=True),
    ),
    Task(id=4, function=cellpose_segmentation, task_type="parallel"),
    Task(id=5, function=new_ome_zarr, task_type="non_parallel"),
    Task(id=6, function=copy_data, task_type="parallel"),
    Task(
        id=7,
        function=maximum_intensity_projection,
        task_type="parallel",
        new_filters=dict(data_dimensionality=2),
    ),
    Task(id=8, function=init_channel_parallelization, task_type="non_parallel"),
    Task(id=9, function=init_registration, task_type="non_parallel"),
    Task(id=10, function=create_ome_zarr_multiplex, task_type="non_parallel"),
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