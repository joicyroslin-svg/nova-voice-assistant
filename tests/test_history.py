from pathlib import Path

from voice_assistant.skills.history import append_history, clear_history, history_text


def test_history_append_and_clear(tmp_path: Path) -> None:
    path = tmp_path / "history.jsonl"
    append_history(str(path), "user", "hello")
    text = history_text(str(path))
    assert "user: hello" in text
    assert clear_history(str(path)) == "Conversation history cleared."
