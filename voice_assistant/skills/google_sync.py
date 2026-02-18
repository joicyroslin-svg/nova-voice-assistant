from __future__ import annotations

from pathlib import Path
from typing import Tuple, List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/calendar",
]


def _load_credentials(credentials_file: str, token_file: str) -> Credentials:
    creds: Credentials | None = None
    if Path(token_file).exists():
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh_request()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        Path(token_file).write_text(creds.to_json(), encoding="utf-8")
    return creds


def google_login(credentials_file: str, token_file: str) -> str:
    try:
        _load_credentials(credentials_file, token_file)
        return "Google login successful."
    except Exception as exc:
        return f"Google login failed: {exc}"


def sync_google_contacts(credentials_file: str, token_file: str) -> List[Tuple[str, str]]:
    creds = _load_credentials(credentials_file, token_file)
    service = build("people", "v1", credentials=creds)
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=200,
            personFields="names,phoneNumbers",
        )
        .execute()
    )
    connections = results.get("connections", [])
    contacts: list[Tuple[str, str]] = []
    for person in connections:
        names = person.get("names", [])
        numbers = person.get("phoneNumbers", [])
        if not names or not numbers:
            continue
        name = names[0].get("displayName")
        number = numbers[0].get("value")
        if name and number:
            contacts.append((name, number))
    return contacts


def sync_google_calendar_pull(credentials_file: str, token_file: str, calendar_id: str) -> list[dict[str, str]]:
    creds = _load_credentials(credentials_file, token_file)
    service = build("calendar", "v3", credentials=creds)
    events_result = (
        service.events()
        .list(calendarId=calendar_id, maxResults=20, singleEvents=True, orderBy="startTime")
        .execute()
    )
    events = []
    for item in events_result.get("items", []):
        title = item.get("summary", "Untitled")
        start = item.get("start", {}).get("dateTime") or item.get("start", {}).get("date")
        if start:
            events.append({"title": title, "when": start, "source": "google"})
    return events


def sync_google_calendar_push(credentials_file: str, token_file: str, calendar_id: str, events: list[dict[str, str]]) -> str:
    creds = _load_credentials(credentials_file, token_file)
    service = build("calendar", "v3", credentials=creds)
    created = 0
    for event in events:
        body = {
            "summary": event.get("title", "Untitled"),
            "start": {"dateTime": event.get("when")},
            "end": {"dateTime": event.get("when")},
        }
        try:
            service.events().insert(calendarId=calendar_id, body=body).execute()
            created += 1
        except Exception:
            continue
    if created == 0:
        return "No events pushed to Google Calendar."
    return f"Pushed {created} events to Google Calendar."
