from models import Dataset
from models import Task
from models import Workflow
from models import WorkflowTask
from runner import apply_workflow

from tests.tasks_for_tests import copy_and_edit_image
from tests.tasks_for_tests import create_images_from_scratch
from tests.tasks_for_tests import edit_images
from tests.tasks_for_tests import print_path


dataset = Dataset(id=1, root_dir="/invalid")
wf = Workflow(
    id=1,
    task_list=[
        WorkflowTask(
            id=1,
            task_id=1,
            task=Task(
                id=1,
                task_type="non_parallel",
                function=create_images_from_scratch,
            ),
        ),
        # a, b, c
        WorkflowTask(
            id=2,
            task_id=2,
            task=Task(id=2, task_type="parallel", function=edit_images, new_filters=dict(key="value")),
        ),
        # a, b, c all with key=value
        # dataset.filters key=value
        WorkflowTask(
            id=4,
            task_id=4,
            task=Task(
                id=4,
                task_type="parallel",
                function=copy_and_edit_image,
            ),
        ),
        # a, b, c all with key=value
        # d, e, f
        # dataset.filters key=value
        WorkflowTask(
            id=3,
            task_id=3,
            task=Task(
                id=3,
                task_type="parallel",
                function=print_path,
            ),
        ),
    ],
)


def test_apply_workflow():
    apply_workflow(wf_task_list=wf.task_list, dataset=dataset)
