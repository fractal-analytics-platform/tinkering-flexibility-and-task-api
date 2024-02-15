from typing import Any


def dummy_task(*args, **kwargs):
    """
    This task does nothing, and it is both valid as a parallel or non_parallel task.
    """
    return {}


# Non-parallel tasks


def create_images_from_scratch(
    root_dir: str,
    paths: list[str],
    buffer: dict[str, Any],
) -> dict[str, Any]:
    new_images = [
        dict(path="a"),
        dict(path="b"),
        dict(path="c"),
    ]
    return dict(new_images=new_images)


# Parallel tasks


def print_path(root_dir: str, path: str, buffer: dict[str, Any]) -> dict[str, Any]:
    print(f"Running `print_path` task, with {path=}")
    return {}


def edit_image(root_dir: str, path: str, buffer: dict[str, Any], custom_parameter: int = 1) -> dict[str, Any]:
    edited_images = [dict(path=path)]
    return dict(edited_images=edited_images)


def copy_and_edit_image(
    root_dir: str,
    path: str,
    buffer: dict[str, Any],
) -> dict[str, Any]:
    new_images = [dict(path=f"{path}_new", processed=True)]
    return dict(new_images=new_images)
