from models import Dataset
from models import WorkflowTask
from workflows import get_task_from_db
from workflows import get_workflow_1


def get_default_filters_chain(dataset: Dataset, wftask_list: list[WorkflowTask]) -> list[dict]:

    current_default_filters = dataset.filters
    for ind, wftask in enumerate(wftask_list):
        task = get_task_from_db(wftask.task_id)
        print(ind)
        print(f"  {current_default_filters=}")
        print(f"  {task.new_default_filters=}")
        current_default_filters.update(task.new_default_filters)
        print(f"  {current_default_filters=}")
        print()


if __name__ == "__main__":
    ds = Dataset(id=123, root_dir="/tmp/somewhere/")
    wf = get_workflow_1()
    get_default_filters_chain(
        dataset=ds,
        wftask_list=wf.task_list,
    )
