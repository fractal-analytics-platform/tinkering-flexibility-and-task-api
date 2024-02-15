# from models import TASK_NAME_TO_TASK_ID
from models import Task
from models import Workflow
from models import WorkflowTask
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

TASKS = {
    "create_ome_zarr": Task(function=create_ome_zarr, task_type="non_parallel"),
    "yokogawa_to_zarr": Task(function=yokogawa_to_zarr, task_type="parallel"),
    "create_ome_zarr_multiplex": Task(function=create_ome_zarr_multiplex, task_type="non_parallel"),
    "cellpose_segmentation": Task(function=cellpose_segmentation, task_type="parallel"),
    "new_ome_zarr": Task(function=new_ome_zarr, task_type="non_parallel"),
    "copy_data": Task(function=copy_data, task_type="parallel"),
    "illumination_correction": Task(
        function=illumination_correction,
        task_type="parallel",
        new_filters=dict(illumination_correction=True),
    ),
    "maximum_intensity_projection": Task(
        function=maximum_intensity_projection,
        task_type="parallel",
        new_filters=dict(data_dimensionality="2"),
    ),
    "init_channel_parallelization": Task(function=init_channel_parallelization, task_type="non_parallel"),
    "init_registration": Task(function=init_registration, task_type="non_parallel"),
}


WORKFLOWS = [
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=Task(function=yokogawa_to_zarr), args={}),
            WorkflowTask(
                task=Task(
                    function=illumination_correction,
                    task_type="parallel",
                    new_filters=dict(illumination_correction=True),
                ),
                args={},
            ),
            WorkflowTask(
                task=TASKS["cellpose_segmentation"],
                args={},
            ),
            WorkflowTask(
                task=TASKS["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["illumination_correction"],
                args=dict(overwrite_input=True),
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["illumination_correction"],
                args=dict(overwrite_input=True),
                filters=dict(well="A_01"),
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["new_ome_zarr"],
                args={"suffix": "new"},
            ),
            WorkflowTask(
                task=TASKS["copy_data"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                task=TASKS["maximum_intensity_projection"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"]),
            WorkflowTask(task=TASKS["init_channel_parallelization"]),
            WorkflowTask(
                task=TASKS["illumination_correction"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr_multiplex"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["init_registration"],
                args={"ref_cycle_name": "0"},
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASKS["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASKS["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASKS["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                task=TASKS["maximum_intensity_projection"],
            ),
            WorkflowTask(
                task=TASKS["cellpose_segmentation"],
            ),
            WorkflowTask(
                task=TASKS["cellpose_segmentation"],
                filters=dict(data_dimensionality="3", plate=None),
            ),
        ],
    ),
]
