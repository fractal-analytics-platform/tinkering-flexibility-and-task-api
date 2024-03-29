from typing import Any
from typing import Optional

import pytest
from devtools import debug
from env import MAX_PARALLELIZATION_LIST_SIZE
from models import Dataset
from models import Task
from models import WorkflowTask
from runner import execute_tasks_v2

from tests.tasks_for_tests import dummy_task


@pytest.mark.parametrize("N", [100, 1000])
def test_max_parallelization_list_size(N: int):
    parallelization_list = [
        dict(
            path=f"image-{i}",
            parameter=i,
        )
        for i in range(N)
    ]
    dataset = Dataset(
        id=1,
        root_dir="/tmp/invalid",
        images=[dict(path=x["path"]) for x in parallelization_list],
        parallelization_list=parallelization_list,
    )
    wf_task_list = [
        WorkflowTask(
            task=Task(
                task_type="parallel",
                function=dummy_task,
            ),
        )
    ]
    if N < MAX_PARALLELIZATION_LIST_SIZE:
        debug(N, "OK")
        execute_tasks_v2(wf_task_list=wf_task_list, dataset=dataset)
    else:
        with pytest.raises(ValueError) as e:
            execute_tasks_v2(wf_task_list=wf_task_list, dataset=dataset)
        debug(N, str(e.value))


def _copy_and_edit_image(
    root_dir: str,
    path: str,
    buffer: dict[str, Any],
) -> dict[str, Any]:
    new_images = [
        dict(
            path=f"{path}_new",
            processed=True,
        )
    ]
    return dict(new_images=new_images)


@pytest.mark.parametrize(
    "parallelization_list",
    [
        None,
        [
            dict(path="plate.zarr/A/01/0"),
            dict(path="plate.zarr/A/02/0"),
        ],
    ],
)
def test_image_attribute_propagation(
    parallelization_list: Optional[list[dict]],
):
    images_pre = [
        dict(path="plate.zarr/A/01/0", plate="plate.zarr", well="A/01"),
        dict(path="plate.zarr/A/02/0", plate="plate.zarr", well="A/02"),
    ]
    dataset_pre = Dataset(
        id=1,
        root_dir="/tmp/invalid",
        images=images_pre,
        parallelization_list=parallelization_list,
    )
    wf_task_list = [
        WorkflowTask(
            task=Task(
                task_type="parallel",
                function=_copy_and_edit_image,
            ),
        )
    ]
    dataset_post = execute_tasks_v2(wf_task_list=wf_task_list, dataset=dataset_pre)
    images_post = dataset_post.images

    debug(images_pre)
    debug(images_post)

    for image in images_post:
        print(f"Now validate {image}")
        if image["path"] == "plate.zarr/A/01/0_new":
            assert image["processed"] is True
            assert image["plate"] == "plate.zarr"
            assert image["well"] == "A/01"
        elif image["path"] == "plate.zarr/A/02/0_new":
            assert image["processed"] is True
            assert image["plate"] == "plate.zarr"
            assert image["well"] == "A/02"
        else:
            assert image["plate"] == "plate.zarr"
            assert "processed" not in image.keys()
