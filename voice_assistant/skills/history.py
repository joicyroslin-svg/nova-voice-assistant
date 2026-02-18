from __future__ import annotations

import json
from pathlib import Path


def append_history(path: str, role: str, text: str) -> None:
    line = json.dumps({"role": role, "text": text}, ensure_ascii=False)
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def read_history(path: str, limit: int = 10) -> list[dict[str, str]]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries: list[dict[str, str]] = []
    for line in lines[-limit:]:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict) and isinstance(item.get("role"), str) and isinstance(item.get("text"), str):
            entries.append({"role": item["role"], "text": item["text"]})
    return entries


def clear_history(path: str) -> str:
    try:
        Path(path).write_text("", encoding="utf-8")
        return "Conversation history cleared."
    except OSError:
        return "Could not clear history."


def history_text(path: str, limit: int = 8) -> str:
    entries = read_history(path, limit=limit)
    if not entries:
        return "No conversation history yet."
    lines = [f"{item['role']}: {item['text']}" for item in entries]
    return "Recent conversation: " + " | ".join(lines)
