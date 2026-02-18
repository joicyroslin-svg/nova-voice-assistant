from voice_assistant.skills.calendar_tools import add_event, show_schedule_text, sync_tasks_to_calendar


def test_calendar_add_show_sync() -> None:
    events: list[dict[str, str]] = []
    tasks: list[dict[str, object]] = [{"text": "finish assignment", "done": False}]
    assert "Event added" in add_event(events, "study", "2026-02-20 18:00")
    assert "Upcoming schedule" in show_schedule_text(events)
    assert "Synced" in sync_tasks_to_calendar(tasks, events)
