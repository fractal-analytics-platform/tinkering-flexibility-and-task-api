import os
import shutil
import sys

from models import Dataset
from runner import apply_workflow
from workflows import WF0
from workflows import WF1
from workflows import WF2
from workflows import WF3


if __name__ == "__main__":
    workflows = [WF0, WF1, WF2, WF3]
    if len(sys.argv) == 2:
        WF_ind = int(sys.argv[1])
        workflows = [workflows[WF_ind]]

    for WF in workflows:
        # Define single dataset, and reset its root_dir
        dataset = Dataset(id=123, root_dir="/tmp/somewhere/")
        if os.path.isdir(dataset.root_dir):
            shutil.rmtree(dataset.root_dir)

        apply_workflow(wf_task_list=WF.task_list, dataset=dataset)
