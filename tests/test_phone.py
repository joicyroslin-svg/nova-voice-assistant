from voice_assistant.skills.phone import make_call, open_phone_app, send_sms, send_whatsapp_message


def test_phone_actions_when_adb_disabled() -> None:
    assert "Enable ADB phone control" in make_call("9876543210", adb_enabled=False, adb_path="adb")
    assert "Enable ADB phone control" in open_phone_app("whatsapp", adb_enabled=False, adb_path="adb")
    assert "Enable ADB phone control" in send_sms(
        "9876543210",
        "hello",
        adb_enabled=False,
        adb_path="adb",
    )
    assert "Enable ADB phone control" in send_whatsapp_message(
        "9876543210",
        "hello",
        adb_enabled=False,
        adb_path="adb",
    )
