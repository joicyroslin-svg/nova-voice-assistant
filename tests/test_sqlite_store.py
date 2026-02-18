from pathlib import Path

from voice_assistant.storage.sqlite_store import MigrationSources, SQLiteStore


def _sources(tmp_path: Path) -> MigrationSources:
    return MigrationSources(
        reminders_file=str(tmp_path / "reminders.json"),
        tasks_file=str(tmp_path / "tasks.json"),
        profile_file=str(tmp_path / "profile.json"),
        expenses_file=str(tmp_path / "expenses.json"),
        habits_file=str(tmp_path / "habits.json"),
        history_file=str(tmp_path / "history.jsonl"),
        contacts_file=str(tmp_path / "contacts.json"),
        events_file=str(tmp_path / "events.json"),
    )


def test_sqlite_store_roundtrip(tmp_path: Path) -> None:
    db_file = tmp_path / "state.db"
    store = SQLiteStore(str(db_file), _sources(tmp_path))

    store.save_profile({"name": "Sunil"})
    store.save_reminders(["drink water"])
    store.save_tasks([{"text": "finish resume", "done": False}])
    store.save_expenses([{"amount": 100.0, "category": "food", "date": "2026-02-18"}])
    store.save_habits({"reading": 2})
    store.append_history("user", "hello")

    assert store.load_profile().get("name") == "Sunil"
    assert store.load_reminders() == ["drink water"]
    assert store.load_tasks()[0]["text"] == "finish resume"
    assert store.load_expenses()[0]["category"] == "food"
    assert store.load_habits()["reading"] == 2
    assert "user: hello" in store.history_text()
