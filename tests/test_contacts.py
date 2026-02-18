from voice_assistant.skills.contacts import add_contact, list_contacts_text, resolve_contact_number


def test_contacts_flow() -> None:
    contacts: dict[str, str] = {}
    assert "Saved contact" in add_contact(contacts, "Mom", "9876543210")
    assert resolve_contact_number(contacts, "mom") == "9876543210"
    assert "mom" in list_contacts_text(contacts)
