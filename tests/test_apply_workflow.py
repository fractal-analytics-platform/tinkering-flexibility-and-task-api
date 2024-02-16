import pytest
from devtools import debug
from models import Dataset
from models import Task
from models import WorkflowTask
from runner import _validate_parallelization_list_valid
from runner import apply_workflow

from tests.tasks_for_tests import create_images_from_scratch
from tests.tasks_for_tests import print_path


def test_single_non_parallel_task():
    NEW_PATHS = ["A/01/0", "A/02/0", "A/03/0"]
    dataset_in = Dataset(id=1, root_dir="/invalid")
    task_list = [
        WorkflowTask(
            task=Task(
                task_type="non_parallel",
                function=create_images_from_scratch,
            ),
            args=dict(new_paths=NEW_PATHS),
        )
    ]
    dataset_out = apply_workflow(wf_task_list=task_list, dataset=dataset_in)
    debug(dataset_out.image_paths)
    assert set(dataset_out.image_paths) == set(NEW_PATHS)


def test_single_parallel_task_no_parallization_list():
    """This is currently not very useful"""
    IMAGES = [dict(path="A/01/0"), dict(path="A/02/0")]
    dataset_in = Dataset(id=1, root_dir="/invalid", images=IMAGES)
    task_list = [
        WorkflowTask(
            task=Task(
                task_type="parallel",
                function=print_path,
            )
        )
    ]
    dataset_out = apply_workflow(wf_task_list=task_list, dataset=dataset_in)
    debug(dataset_out.image_paths)


def test_unit_validate_parallelization_list():

    # Missing path
    PARALLELIZATION_LIST = [dict()]
    CURRENT_IMAGE_PATHS = []
    with pytest.raises(ValueError):
        _validate_parallelization_list_valid(
            parallelization_list=PARALLELIZATION_LIST,
            current_image_paths=CURRENT_IMAGE_PATHS,
        )

    # Path not in current image paths
    PARALLELIZATION_LIST = [dict(path="asd")]
    CURRENT_IMAGE_PATHS = []
    with pytest.raises(ValueError):
        _validate_parallelization_list_valid(
            parallelization_list=PARALLELIZATION_LIST,
            current_image_paths=CURRENT_IMAGE_PATHS,
        )

    # Invalid buffer attributes
    PARALLELIZATION_LIST = [dict(path="asd", buffer={})]
    CURRENT_IMAGE_PATHS = ["asd"]
    with pytest.raises(ValueError):
        _validate_parallelization_list_valid(
            parallelization_list=PARALLELIZATION_LIST,
            current_image_paths=CURRENT_IMAGE_PATHS,
        )

    # Invalid `buffer`` attribute
    PARALLELIZATION_LIST = [dict(path="asd", buffer={})]
    CURRENT_IMAGE_PATHS = ["asd"]
    with pytest.raises(ValueError):
        _validate_parallelization_list_valid(
            parallelization_list=PARALLELIZATION_LIST,
            current_image_paths=CURRENT_IMAGE_PATHS,
        )

    # Invalid `root_dir` attribute
    PARALLELIZATION_LIST = [dict(path="asd", root_dir="/something")]
    CURRENT_IMAGE_PATHS = ["asd"]
    with pytest.raises(ValueError):
        _validate_parallelization_list_valid(
            parallelization_list=PARALLELIZATION_LIST,
            current_image_paths=CURRENT_IMAGE_PATHS,
        )

    # Valid call
    PARALLELIZATION_LIST = [
        dict(path="asd", parameter=1),
        dict(path="asd", parameter=2),
        dict(path="asd", parameter=3),
    ]
    CURRENT_IMAGE_PATHS = ["asd"]
    _validate_parallelization_list_valid(
        parallelization_list=PARALLELIZATION_LIST,
        current_image_paths=CURRENT_IMAGE_PATHS,
    )
