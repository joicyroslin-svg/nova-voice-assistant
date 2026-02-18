from __future__ import annotations

from datetime import datetime


def add_event(events: list[dict[str, str]], title: str, when: str, source: str = "manual") -> str:
    clean_title = title.strip()
    clean_when = when.strip()
    if not clean_title or not clean_when:
        return "Could not add event. Use: add event <title> at YYYY-MM-DD HH:MM."
    events.append({"title": clean_title, "when": clean_when, "source": source})
    return f"Event added: {clean_title} at {clean_when}."


def show_schedule_text(events: list[dict[str, str]], limit: int = 8) -> str:
    if not events:
        return "No events in schedule."
    sorted_events = sorted(events, key=lambda e: e.get("when", ""))[:limit]
    lines = [f"{idx + 1}. {e['when']} - {e['title']} ({e.get('source', 'manual')})" for idx, e in enumerate(sorted_events)]
    return "Upcoming schedule: " + "; ".join(lines)


def sync_tasks_to_calendar(tasks: list[dict[str, object]], events: list[dict[str, str]]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    existing_titles = {e.get("title", "") for e in events if e.get("source") == "task_sync"}
    added = 0
    for task in tasks:
        if bool(task.get("done")):
            continue
        title = str(task.get("text", "")).strip()
        if not title or title in existing_titles:
            continue
        events.append({"title": title, "when": f"{today} 18:00", "source": "task_sync"})
        existing_titles.add(title)
        added += 1
    if added == 0:
        return "No new pending tasks to sync."
    return f"Synced {added} pending tasks to calendar."
