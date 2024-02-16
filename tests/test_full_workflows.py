from pathlib import Path

import pytest
from models import Dataset
from models import Workflow
from runner import apply_workflow
from workflows import WORKFLOWS


@pytest.mark.parametrize("workflow", WORKFLOWS)
def test_full_workflows(workflow: Workflow, tmp_path: Path):
    root_dir = (tmp_path / "root_dir").as_posix()
    dataset = Dataset(id=1, root_dir=root_dir)
    apply_workflow(wf_task_list=workflow.task_list, dataset=dataset)
