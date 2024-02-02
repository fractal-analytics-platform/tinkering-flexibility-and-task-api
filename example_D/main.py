import os
import shutil

from models import Dataset
from runner import apply_workflow
from workflows import WF1 as WF


if __name__ == "__main__":

    # Define single dataset, and reset its root_dir
    dataset = Dataset(id=123, root_dir="/tmp/somewhere/")
    if os.path.isdir(dataset.root_dir):
        shutil.rmtree(dataset.root_dir)

    apply_workflow(wf_task_list=WF.task_list, dataset=dataset)
