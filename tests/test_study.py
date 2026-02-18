from voice_assistant.skills.study import build_study_plan, explain_topic, quiz_topic


def test_study_helpers() -> None:
    assert "Study plan for python" in build_study_plan("python")
    assert "binary search" in explain_topic("binary search")
    assert "Quick quiz on os" in quiz_topic("os")
