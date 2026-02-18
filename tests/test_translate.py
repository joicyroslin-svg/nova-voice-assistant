from voice_assistant.skills.translate import supported_languages_text, translate_text


def test_translate_known_phrase() -> None:
    reply = translate_text("telugu|hello")
    assert "నమస్తే" in reply


def test_translate_unknown_phrase() -> None:
    reply = translate_text("hindi|quantum mechanics")
    assert reply.startswith("I currently know common phrases offline.")


def test_translate_supported_languages() -> None:
    reply = supported_languages_text()
    assert "english" in reply and "telugu" in reply
