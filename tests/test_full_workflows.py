from pathlib import Path

import pytest
from devtools import debug
from models import Dataset
from models import Workflow
from models import WorkflowTask
from runner import apply_workflow
from tasks import TASK_LIST


def test_workflow_1(tmp_path: Path):
    root_dir = (tmp_path / "root_dir").as_posix()
    dataset_in = Dataset(id=1, root_dir=root_dir)
    dataset_out = apply_workflow(
        wf_task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["illumination_correction"],
            ),
            WorkflowTask(
                task=TASK_LIST["cellpose_segmentation"],
            ),
            WorkflowTask(
                task=TASK_LIST["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                task=TASK_LIST["maximum_intensity_projection"],
            ),
        ],
        dataset=dataset_in,
    )
    debug(dataset_out.images)
    assert set(dataset_out.image_paths) == {
        "my_plate.zarr/A/01/0",
        "my_plate.zarr/A/01/0_corr",
        "my_plate_mip.zarr/A/01/0",  # FIXME: why not corr??
        "my_plate.zarr/A/02/0",
        "my_plate.zarr/A/02/0_corr",
        "my_plate_mip.zarr/A/02/0",  # FIXME: why not corr??
    }


WORKFLOWS = [
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["illumination_correction"],
                args={},
            ),
            WorkflowTask(
                task=TASK_LIST["cellpose_segmentation"],
                args={},
            ),
            WorkflowTask(
                task=TASK_LIST["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["illumination_correction"],
                args=dict(overwrite_input=True),
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["illumination_correction"],
                args=dict(overwrite_input=True),
                filters=dict(well="A_01"),
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["new_ome_zarr"],
                args={"suffix": "new"},
            ),
            WorkflowTask(
                task=TASK_LIST["copy_data"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                task=TASK_LIST["maximum_intensity_projection"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"]),
            WorkflowTask(task=TASK_LIST["init_channel_parallelization"]),
            WorkflowTask(
                task=TASK_LIST["illumination_correction"],
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr_multiplex"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["init_registration"],
                args={"ref_cycle_name": "0"},
            ),
        ],
    ),
    Workflow(
        task_list=[
            WorkflowTask(
                task=TASK_LIST["create_ome_zarr"],
                args=dict(image_dir="/tmp/input_images"),
            ),
            WorkflowTask(task=TASK_LIST["yokogawa_to_zarr"], args={}),
            WorkflowTask(
                task=TASK_LIST["new_ome_zarr"],
                args={"suffix": "mip"},
            ),
            WorkflowTask(
                task=TASK_LIST["maximum_intensity_projection"],
            ),
            WorkflowTask(
                task=TASK_LIST["cellpose_segmentation"],
            ),
            WorkflowTask(
                task=TASK_LIST["cellpose_segmentation"],
                filters=dict(data_dimensionality="3", plate=None),
            ),
        ],
    ),
]


@pytest.mark.parametrize("workflow", WORKFLOWS)
def test_full_workflows(workflow: Workflow, tmp_path: Path):
    root_dir = (tmp_path / "root_dir").as_posix()
    dataset = Dataset(id=1, root_dir=root_dir)
    apply_workflow(wf_task_list=workflow.task_list, dataset=dataset)
