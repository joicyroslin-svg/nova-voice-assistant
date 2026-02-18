from voice_assistant.skills.reminders import clear_reminders, delete_reminder


def test_delete_reminder() -> None:
    reminders = ["a", "b"]
    assert delete_reminder(reminders, 2) == "Removed reminder: b"
    assert reminders == ["a"]


def test_clear_reminders() -> None:
    reminders = ["a"]
    assert clear_reminders(reminders) == "All reminders cleared."
    assert reminders == []
