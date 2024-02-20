from typing import Any
from typing import Optional

from images import find_image_by_path
from images import ScalarDict
from images import SingleImage
from pydantic import BaseModel
from utils import pjson


class TaskOutput(BaseModel):
    new_images: list[SingleImage] = []
    """List of new images added by a given task instance."""

    edited_images: list[SingleImage] = []
    """List of images edited by a given task instance."""

    new_filters: ScalarDict = {}
    """
    *Global* filters (common to all images) added by this task.

    Note: the right place for these filters would be in the task manifest,
    but this attribute is useful for the ones which determined at runtime
    (e.g. the plate name).
    """

    buffer: Optional[dict[str, Any]] = None
    """
    Metadata used for communication between an init task and its (parallel)
    companion task.
    """

    parallelization_list: Optional[list[ScalarDict]] = None
    """
    Used in the output of an init task, to expose customizable parallelization
    of the companion task.
    """

    class Config:
        extra = "forbid"


class ParallelTaskOutput(BaseModel):
    class Config:
        extra = "allow"

    new_images: list[SingleImage] = []
    edited_images: list[SingleImage] = []
    new_filters: ScalarDict = {}


def merge_outputs(
    task_outputs: list[ParallelTaskOutput],
    new_old_image_mapping: dict[str, str],
    old_dataset_images: list[SingleImage],
) -> TaskOutput:

    final_new_images = []
    final_edited_images = []
    final_new_filters = {}

    for task_output in task_outputs:

        for new_image in task_output.new_images:
            old_image = find_image_by_path(
                images=old_dataset_images,
                path=new_old_image_mapping[new_image.path],
            )

            # Propagate old-image attributes to new-image
            new_image.attributes = old_image.attributes | new_image.attributes

            final_new_images.append(new_image)

        for edited_image in task_output.edited_images:
            final_edited_images.append(edited_image)

        new_filters = task_output.new_filters
        if new_filters:
            if final_new_filters:
                final_new_filters = new_filters
            else:
                if final_new_filters != new_filters:
                    raise ValueError(f"{new_filters=} but {final_new_filters=}")

    final_output = TaskOutput(
        new_images=final_new_images,
        edited_images=final_edited_images,
        new_filters=final_new_filters,
    )

    print(f"Merged task output:\n{pjson(final_output.dict())}")

    return final_output
