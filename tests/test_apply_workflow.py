from devtools import debug
from models import Dataset
from models import Task
from models import WorkflowTask
from runner import apply_workflow

from tests.tasks_for_tests import create_images_from_scratch
from tests.tasks_for_tests import print_path

"""
from models import Workflow
from tests.tasks_for_tests import copy_and_edit_image
from tests.tasks_for_tests import edit_image
from tests.tasks_for_tests import print_path


dataset = Dataset(id=1, root_dir="/invalid")

        WorkflowTask(
            task=Task(task_type="parallel", function=edit_image, new_filters=dict(key="value")),
        ),
        # a, b, c all with key=value
        # dataset.filters key=value
        WorkflowTask(
            task=Task(
                task_type="parallel",
                function=copy_and_edit_image,
            ),
        ),
        # a, b, c all with key=value
        # d, e, f
        # dataset.filters key=value
        WorkflowTask(
            task=Task(
                task_type="parallel",
                function=print_path,
            ),
        ),
    ],
)
"""


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
