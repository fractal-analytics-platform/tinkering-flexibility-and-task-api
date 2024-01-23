from typing import Any
from typing import Optional


def task_function_legacy(
    *,
    input_paths: list[str],
    output_path: str,
    component: str,
    metadata: dict[str, Any],
):
    print(
        "Now running task with:\n"
        f"  {input_paths=}\n"
        f"  {output_path=}\n"
        f"  {component=}\n"
    )


def task_function_new(
    *,
    zarr_path: str,
    metadata: dict[str, Any],
    output_path: Optional[str] = None,
    T_index: Optional[int] = None,
    C_index: Optional[int] = None,
    Z_index: Optional[int] = None,
):
    print(
        "Now running task with:\n"
        f"  {zarr_path=}\n"
        f"  {output_path=}\n"
        f"  {T_index=}\n"
        f"  {C_index=}\n"
        f"  {Z_index=}\n"
    )
