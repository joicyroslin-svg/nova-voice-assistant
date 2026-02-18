from __future__ import annotations

import json
from pathlib import Path


def load_tasks(path: str) -> list[dict[str, object]]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    tasks: list[dict[str, object]] = []
    for item in data:
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            tasks.append({"text": item["text"], "done": bool(item.get("done", False))})
    return tasks


def save_tasks(path: str, tasks: list[dict[str, object]]) -> None:
    file_path = Path(path)
    file_path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(tasks: list[dict[str, object]], text: str) -> str:
    tasks.append({"text": text, "done": False})
    return f"Task added: {text}"


def list_tasks_text(tasks: list[dict[str, object]]) -> str:
    if not tasks:
        return "You do not have any tasks yet."
    lines = []
    for idx, task in enumerate(tasks, start=1):
        status = "done" if bool(task.get("done")) else "pending"
        lines.append(f"{idx}. {task.get('text')} ({status})")
    return "Your tasks are: " + "; ".join(lines)


def complete_task(tasks: list[dict[str, object]], index: int) -> str:
    if index < 1 or index > len(tasks):
        return "Task number is out of range."
    tasks[index - 1]["done"] = True
    return f"Task marked done: {tasks[index - 1]['text']}"


def delete_task(tasks: list[dict[str, object]], index: int) -> str:
    if index < 1 or index > len(tasks):
        return "Task number is out of range."
    removed = tasks.pop(index - 1)
    return f"Deleted task: {removed['text']}"


def clear_tasks(tasks: list[dict[str, object]]) -> str:
    if not tasks:
        return "You do not have any tasks to clear."
    tasks.clear()
    return "All tasks cleared."
