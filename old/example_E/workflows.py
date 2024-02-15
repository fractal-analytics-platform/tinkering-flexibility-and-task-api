from models import TASK_NAME_TO_TASK_ID
from models import Workflow
from models import WorkflowTask

WORKFLOWS = [
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=3,
                task_id=TASK_NAME_TO_TASK_ID["illumination_correction"],
                args={},
            ),
            WorkflowTask(
                id=4,
                task_id=TASK_NAME_TO_TASK_ID["cellpose_segmentation"],
                args={},
            ),
            WorkflowTask(
                id=5,
                task_id=TASK_NAME_TO_TASK_ID["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=3,
                task_id=TASK_NAME_TO_TASK_ID["illumination_correction"],
                args=dict(overwrite_input=True),
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=3,
                task_id=TASK_NAME_TO_TASK_ID["illumination_correction"],
                args=dict(overwrite_input=True),
                filters=dict(well="A_01"),
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=5,
                task_id=TASK_NAME_TO_TASK_ID["new_ome_zarr"],
                args={"suffix": "new"},
            ),
            WorkflowTask(
                id=6,
                task_id=TASK_NAME_TO_TASK_ID["copy_data"],
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=5,
                task_id=TASK_NAME_TO_TASK_ID["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                id=6,
                task_id=TASK_NAME_TO_TASK_ID["maximum_intensity_projection"],
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"]),
            WorkflowTask(id=3, task_id=TASK_NAME_TO_TASK_ID["init_channel_parallelization"]),
            WorkflowTask(
                id=4,
                task_id=TASK_NAME_TO_TASK_ID["illumination_correction"],
            ),
        ],
    ),
    Workflow(
        id=1,
        task_list=[
            WorkflowTask(
                id=1,
                task_id=TASK_NAME_TO_TASK_ID["create_ome_zarr_multiplex"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(id=2, task_id=TASK_NAME_TO_TASK_ID["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                id=3,
                task_id=TASK_NAME_TO_TASK_ID["init_registration"],
                args={"ref_cycle_name": "0"},
            ),
        ],
    ),
]

if __name__ == "__main__":
    from devtools import debug

    debug(WORKFLOWS[0])
