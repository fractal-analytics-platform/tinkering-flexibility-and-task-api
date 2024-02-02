from typing import Any
from typing import Callable
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Dataset(BaseModel):
    id: Optional[int] = None
    root_dir: str
    images: list[dict[str, Any]] = []
    default_filters: Optional[dict[str, bool]] = None
    buffer: Optional[dict[str, Any]] = None
    history: list[dict[str, Any]] = []


class Task(BaseModel):
    id: Optional[int] = None
    function: Callable
    meta: dict[str, Any] = Field(default_factory=dict)

    @property
    def is_parallel(self):
        return self.meta.get("parallel", False)
