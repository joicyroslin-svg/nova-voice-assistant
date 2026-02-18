from pathlib import Path

from voice_assistant.skills.reminders import load_reminders, save_reminders


def test_load_missing_file_returns_empty(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    assert load_reminders(str(missing)) == []


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "reminders.json"
    expected = ["call mom", "apply for jobs"]
    save_reminders(str(path), expected)
    assert load_reminders(str(path)) == expected


def test_load_invalid_json_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{invalid json", encoding="utf-8")
    assert load_reminders(str(path)) == []
