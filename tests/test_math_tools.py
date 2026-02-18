from voice_assistant.skills.math_tools import calculate_expression


def test_calculate_expression_success() -> None:
    assert calculate_expression("12 / 4 + 3") == "The result is 6"


def test_calculate_expression_invalid() -> None:
    reply = calculate_expression("import os")
    assert reply.startswith("I could not calculate that.")
