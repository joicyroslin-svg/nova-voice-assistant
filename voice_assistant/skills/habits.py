from __future__ import annotations

import json
from pathlib import Path


def load_habits(path: str) -> dict[str, int]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    habits: dict[str, int] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, int):
            habits[key] = value
    return habits


def save_habits(path: str, habits: dict[str, int]) -> None:
    Path(path).write_text(json.dumps(habits, indent=2), encoding="utf-8")


def add_habit(habits: dict[str, int], name: str) -> str:
    key = name.strip().lower()
    if key in habits:
        return f"Habit already exists: {name.strip()}."
    habits[key] = 0
    return f"Habit added: {name.strip()}."


def done_habit(habits: dict[str, int], name: str) -> str:
    key = name.strip().lower()
    if key not in habits:
        return f"Habit not found: {name.strip()}."
    habits[key] += 1
    return f"Great work. {name.strip()} streak count is now {habits[key]}."


def show_habits_text(habits: dict[str, int]) -> str:
    if not habits:
        return "You do not have any habits yet."
    lines = [f"{name}: {count}" for name, count in sorted(habits.items())]
    return "Your habits and streak counts: " + "; ".join(lines)
