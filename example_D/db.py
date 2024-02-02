from models import Task
from models import Workflow
from models import WorkflowTask
from tasks import cellpose_segmentation
from tasks import copy_ome_zarr
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import yokogawa_to_zarr


def get_task(id: int) -> Task:
    TASKS = [
        Task(id=1, function=create_ome_zarr),
        Task(id=2, function=yokogawa_to_zarr, meta=dict(parallel=True)),
        Task(
            id=3,
            function=illumination_correction,
            meta=dict(parallel=True),
            new_default_filters=dict(illumination_correction=True),
        ),
        Task(id=4, function=cellpose_segmentation, meta=dict(parallel=True)),
        Task(
            id=5,
            function=copy_ome_zarr,
            meta=dict(combine_components=True),
        ),
    ]
    task = next(t for t in TASKS if t.id == id)
    return task


def get_workflow() -> Workflow:
    wf_task_list = [
        WorkflowTask(
            id=1, task_id=1, args=dict(image_dir="/tmp/input_images")
        ),
        WorkflowTask(id=2, task_id=2, args={}),
        WorkflowTask(id=3, task_id=3, args={}),
        WorkflowTask(id=4, task_id=4, args={}),
        WorkflowTask(id=5, task_id=5, args={"suffix": "mip"}),
    ]
    wf = Workflow(id=1, task_list=wf_task_list)
    return wf
