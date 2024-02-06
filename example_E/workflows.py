from models import TASK_NAME_TO_TASK_ID
from models import Workflow
from models import WorkflowTask

WF0 = Workflow(
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
)

WF1 = Workflow(
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
)


WF2 = Workflow(
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
)


WF3 = Workflow(
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
)


WF4 = Workflow(
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
)


if __name__ == "__main__":
    from devtools import debug

    debug(WF0)
