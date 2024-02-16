from filters import FilterSet
from images import SingleImage
from models import KwargsType

from pydantic import BaseModel

from typing import Any
from typing import Optional


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


class ParallelTaskOutput(BaseModel):
    class Config:
        extra = "forbid"
    new_images: Optional[list[SingleImage]] = None
    edited_images: Optional[list[SingleImage]] = None
    new_filters: Optional[FilterSet] = None  # FIXME