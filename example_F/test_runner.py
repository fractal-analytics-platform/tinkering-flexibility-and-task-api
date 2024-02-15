from typing import Any
from typing import Optional

import pytest
from devtools import debug
from env import MAX_PARALLELIZATION_LIST_SIZE
from models import Dataset
from models import FilterSet
from models import Task
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


def dummy_task(*args, **kwargs):
    return {}


@pytest.mark.parametrize("N", [100, 1000])
def test_max_parallelization_list_size(N: int):
    parallelization_list = [
        dict(
            path=f"image-{i}",
            parameter=i,
        )
        for i in range(N)
    ]
    dataset = Dataset(
        id=1,
        root_dir="/tmp/invalid",
        parallelization_list=parallelization_list,
    )
    wf_task_list = [
        WorkflowTask(
            id=1,
            task_id=1,
            task=Task(
                id=1,
                task_type="parallel",
                function=dummy_task,
            ),
        )
    ]
    if N < MAX_PARALLELIZATION_LIST_SIZE:
        debug(N, "OK")
        apply_workflow(wf_task_list=wf_task_list, dataset=dataset)
    else:
        with pytest.raises(ValueError) as e:
            apply_workflow(wf_task_list=wf_task_list, dataset=dataset)
        debug(N, str(e.value))
