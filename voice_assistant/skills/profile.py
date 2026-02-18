from __future__ import annotations

import json
from pathlib import Path


def load_profile(path: str) -> dict[str, str]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    profile: dict[str, str] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, str):
            profile[key] = value
    return profile


def save_profile(path: str, profile: dict[str, str]) -> None:
    Path(path).write_text(json.dumps(profile, indent=2), encoding="utf-8")
