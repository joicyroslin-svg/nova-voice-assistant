from __future__ import annotations

import json
from pathlib import Path


def load_events(path: str) -> list[dict[str, str]]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    result: list[dict[str, str]] = []
    for item in data:
        if (
            isinstance(item, dict)
            and isinstance(item.get("title"), str)
            and isinstance(item.get("when"), str)
        ):
            result.append({"title": item["title"], "when": item["when"], "source": str(item.get("source", "manual"))})
    return result


def save_events(path: str, events: list[dict[str, str]]) -> None:
    Path(path).write_text(json.dumps(events, indent=2), encoding="utf-8")
