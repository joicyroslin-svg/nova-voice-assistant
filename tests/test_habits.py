from voice_assistant.skills.habits import add_habit, done_habit, show_habits_text


def test_habit_flow() -> None:
    habits: dict[str, int] = {}
    assert "Habit added" in add_habit(habits, "reading")
    assert "streak count is now 1" in done_habit(habits, "reading")
    assert "reading: 1" in show_habits_text(habits)
