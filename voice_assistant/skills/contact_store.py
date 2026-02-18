from __future__ import annotations

import json
from pathlib import Path


def load_contacts(path: str) -> dict[str, str]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, str):
            result[k] = v
    return result


def save_contacts(path: str, contacts: dict[str, str]) -> None:
    Path(path).write_text(json.dumps(contacts, indent=2), encoding="utf-8")
