from typing import Any

def task_function(
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