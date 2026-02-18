from pathlib import Path

from voice_assistant.skills.profile import load_profile, save_profile


def test_profile_save_load_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    profile = {"name": "Sunil"}
    save_profile(str(path), profile)
    assert load_profile(str(path)) == profile
