from __future__ import annotations

import json
from pathlib import Path


def load_reminders(path: str) -> list[str]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if isinstance(data, list):
        return [str(item) for item in data if isinstance(item, str)]
    return []


def save_reminders(path: str, reminders: list[str]) -> None:
    file_path = Path(path)
    file_path.write_text(json.dumps(reminders, indent=2), encoding="utf-8")


def delete_reminder(reminders: list[str], index: int) -> str:
    if index < 1 or index > len(reminders):
        return "Reminder number is out of range."
    removed = reminders.pop(index - 1)
    return f"Removed reminder: {removed}"


def clear_reminders(reminders: list[str]) -> str:
    if not reminders:
        return "You do not have any reminders to clear."
    reminders.clear()
    return "All reminders cleared."
