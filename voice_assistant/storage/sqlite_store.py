from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import sqlite3


@dataclass
class MigrationSources:
    reminders_file: str
    tasks_file: str
    profile_file: str
    expenses_file: str
    habits_file: str
    history_file: str
    contacts_file: str
    events_file: str


class SQLiteStore:
    def __init__(self, db_path: str, sources: MigrationSources) -> None:
        self.db_path = db_path
        self.sources = sources
        self._init_db()
        self._migrate_from_files_if_needed()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS profile (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS habits (
                    name TEXT PRIMARY KEY,
                    streak INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS contacts (
                    name TEXT PRIMARY KEY,
                    number TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    event_when TEXT NOT NULL,
                    source TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sync_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )

    def _get_meta(self, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else None

    def _set_meta(self, key: str, value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
                (key, value),
            )

    def _read_json_file(self, path: str) -> object | None:
        file_path = Path(path)
        if not file_path.exists():
            return None
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _migrate_from_files_if_needed(self) -> None:
        if self._get_meta("migration_v1_complete") == "1":
            return

        reminders = self._read_json_file(self.sources.reminders_file)
        if isinstance(reminders, list):
            clean = [item for item in reminders if isinstance(item, str)]
            self.save_reminders(clean)

        tasks = self._read_json_file(self.sources.tasks_file)
        if isinstance(tasks, list):
            clean_tasks: list[dict[str, object]] = []
            for item in tasks:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    clean_tasks.append(
                        {"text": item["text"], "done": bool(item.get("done", False))}
                    )
            self.save_tasks(clean_tasks)

        profile = self._read_json_file(self.sources.profile_file)
        if isinstance(profile, dict):
            clean_profile: dict[str, str] = {
                str(k): str(v) for k, v in profile.items() if isinstance(k, str) and isinstance(v, str)
            }
            self.save_profile(clean_profile)

        expenses = self._read_json_file(self.sources.expenses_file)
        if isinstance(expenses, list):
            clean_expenses: list[dict[str, object]] = []
            for item in expenses:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("amount"), (int, float))
                    and isinstance(item.get("category"), str)
                    and isinstance(item.get("date"), str)
                ):
                    clean_expenses.append(
                        {
                            "amount": float(item["amount"]),
                            "category": item["category"],
                            "date": item["date"],
                        }
                    )
            self.save_expenses(clean_expenses)

        habits = self._read_json_file(self.sources.habits_file)
        if isinstance(habits, dict):
            clean_habits = {str(k): int(v) for k, v in habits.items() if isinstance(k, str) and isinstance(v, int)}
            self.save_habits(clean_habits)

        history_path = Path(self.sources.history_file)
        if history_path.exists():
            try:
                for line in history_path.read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(item, dict) and isinstance(item.get("role"), str) and isinstance(item.get("text"), str):
                        self.append_history(item["role"], item["text"])
            except OSError:
                pass

        contacts = self._read_json_file(self.sources.contacts_file)
        if isinstance(contacts, dict):
            clean_contacts = {str(k): str(v) for k, v in contacts.items() if isinstance(k, str) and isinstance(v, str)}
            self.save_contacts(clean_contacts)

        events = self._read_json_file(self.sources.events_file)
        if isinstance(events, list):
            clean_events: list[dict[str, str]] = []
            for item in events:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("title"), str)
                    and isinstance(item.get("when"), str)
                ):
                    clean_events.append(
                        {
                            "title": item["title"],
                            "when": item["when"],
                            "source": str(item.get("source", "manual")),
                        }
                    )
            self.save_events(clean_events)

        self._set_meta("migration_v1_complete", "1")

    def load_profile(self) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT key, value FROM profile").fetchall()
        return {str(row["key"]): str(row["value"]) for row in rows}

    def save_profile(self, profile: dict[str, str]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM profile")
            conn.executemany(
                "INSERT INTO profile(key, value) VALUES(?, ?)",
                [(k, v) for k, v in profile.items()],
            )

    def load_reminders(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT text FROM reminders ORDER BY id").fetchall()
        return [str(row["text"]) for row in rows]

    def save_reminders(self, reminders: list[str]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM reminders")
            conn.executemany("INSERT INTO reminders(text) VALUES(?)", [(r,) for r in reminders])

    def load_tasks(self) -> list[dict[str, object]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT text, done FROM tasks ORDER BY id").fetchall()
        return [{"text": str(row["text"]), "done": bool(row["done"])} for row in rows]

    def save_tasks(self, tasks: list[dict[str, object]]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM tasks")
            conn.executemany(
                "INSERT INTO tasks(text, done) VALUES(?, ?)",
                [(str(task.get("text", "")), 1 if bool(task.get("done")) else 0) for task in tasks],
            )

    def load_expenses(self) -> list[dict[str, object]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT amount, category, date FROM expenses ORDER BY id").fetchall()
        return [
            {"amount": float(row["amount"]), "category": str(row["category"]), "date": str(row["date"])}
            for row in rows
        ]

    def save_expenses(self, expenses: list[dict[str, object]]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM expenses")
            conn.executemany(
                "INSERT INTO expenses(amount, category, date) VALUES(?, ?, ?)",
                [
                    (float(item.get("amount", 0.0)), str(item.get("category", "")), str(item.get("date", datetime.now().strftime("%Y-%m-%d"))))
                    for item in expenses
                ],
            )

    def load_habits(self) -> dict[str, int]:
        with self._connect() as conn:
            rows = conn.execute("SELECT name, streak FROM habits ORDER BY name").fetchall()
        return {str(row["name"]): int(row["streak"]) for row in rows}

    def save_habits(self, habits: dict[str, int]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM habits")
            conn.executemany(
                "INSERT INTO habits(name, streak) VALUES(?, ?)",
                [(name, int(streak)) for name, streak in habits.items()],
            )

    def append_history(self, role: str, text: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO history(role, text, created_at) VALUES(?, ?, ?)",
                (role, text, datetime.now().isoformat(timespec="seconds")),
            )

    def history_text(self, limit: int = 8) -> str:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, text FROM history ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        if not rows:
            return "No conversation history yet."
        rows = list(reversed(rows))
        lines = [f"{row['role']}: {row['text']}" for row in rows]
        return "Recent conversation: " + " | ".join(lines)

    def history_entries(self, limit: int = 12) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, text FROM history ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        rows = list(reversed(rows))
        return [{"role": str(row["role"]), "text": str(row["text"])} for row in rows]

    def clear_history(self) -> str:
        with self._connect() as conn:
            conn.execute("DELETE FROM history")
        return "Conversation history cleared."

    def load_contacts(self) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT name, number FROM contacts ORDER BY name").fetchall()
        return {str(row["name"]): str(row["number"]) for row in rows}

    def save_contacts(self, contacts: dict[str, str]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM contacts")
            conn.executemany(
                "INSERT INTO contacts(name, number) VALUES(?, ?)",
                [(name, number) for name, number in contacts.items()],
            )

    def load_events(self) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT title, event_when, source FROM events ORDER BY event_when").fetchall()
        return [
            {"title": str(row["title"]), "when": str(row["event_when"]), "source": str(row["source"])}
            for row in rows
        ]

    def save_events(self, events: list[dict[str, str]]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM events")
            conn.executemany(
                "INSERT INTO events(title, event_when, source) VALUES(?, ?, ?)",
                [
                    (str(item.get("title", "")), str(item.get("when", "")), str(item.get("source", "manual")))
                    for item in events
                ],
            )
