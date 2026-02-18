from __future__ import annotations

import re


def normalize_phone(number: str) -> str:
    return re.sub(r"[^\d+]", "", number)


def add_contact(contacts: dict[str, str], name: str, number: str) -> str:
    key = name.strip().lower()
    normalized = normalize_phone(number)
    if not key or not normalized:
        return "Could not save contact. Please provide name and phone number."
    contacts[key] = normalized
    return f"Saved contact {name.strip()} with number {normalized}."


def resolve_contact_number(contacts: dict[str, str], name: str) -> str | None:
    return contacts.get(name.strip().lower())


def list_contacts_text(contacts: dict[str, str]) -> str:
    if not contacts:
        return "No contacts saved yet."
    lines = [f"{name}: {number}" for name, number in sorted(contacts.items())]
    return "Your contacts are: " + "; ".join(lines)
