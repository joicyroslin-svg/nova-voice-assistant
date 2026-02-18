from __future__ import annotations

from datetime import datetime
from pathlib import Path


def save_note(text: str, notes_file: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}\n"
    Path(notes_file).open("a", encoding="utf-8").write(line)
    return "Your note has been saved."
