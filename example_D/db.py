from models import Task
from tasks import cellpose_segmentation
from tasks import copy_ome_zarr
from tasks import create_ome_zarr
from tasks import illumination_correction
from tasks import yokogawa_to_zarr


def get_task(id: int) -> Task:
    TASKS = [
        Task(id=1, function=create_ome_zarr),
        Task(id=2, function=yokogawa_to_zarr, meta=dict(parallel=True)),
        Task(id=3, function=illumination_correction, meta=dict(parallel=True)),
        Task(id=4, function=cellpose_segmentation, meta=dict(parallel=True)),
        Task(id=5, function=copy_ome_zarr, meta=dict(combine_components=True)),
    ]
    task = next(t for t in TASKS if t.id == id)
    return task
