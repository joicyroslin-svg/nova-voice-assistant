from __future__ import annotations

from pathlib import Path
from voice_assistant.audio import Listener, Speaker
from voice_assistant.config import Settings
from voice_assistant.intents import IntentType, parse_intent
from voice_assistant.logging_setup import setup_logging
from voice_assistant.skills.expenses import (
    add_expense,
    load_expenses,
    monthly_expense_report_text,
    save_expenses,
    show_expenses_text,
)
from voice_assistant.skills.calendar_tools import add_event, show_schedule_text, sync_tasks_to_calendar
from voice_assistant.skills.contacts import add_contact, list_contacts_text, resolve_contact_number
from voice_assistant.skills.contact_store import load_contacts, save_contacts
from voice_assistant.skills.event_store import load_events, save_events
from voice_assistant.skills.habits import (
    add_habit,
    done_habit,
    load_habits,
    save_habits,
    show_habits_text,
)
from voice_assistant.skills.history import append_history, clear_history, history_text
from voice_assistant.skills.llm import generate_llm_reply
from voice_assistant.skills.math_tools import calculate_expression
from voice_assistant.skills.notes import save_note
from voice_assistant.skills.phone import make_call, open_phone_app, send_sms, send_whatsapp_message
from voice_assistant.skills.profile import load_profile, save_profile
from voice_assistant.skills.reminders import (
    clear_reminders,
    delete_reminder,
    load_reminders,
    save_reminders,
)
from voice_assistant.skills.system import (
    get_affirmation_text,
    get_breathing_text,
    get_check_in_text,
    get_daily_chores_text,
    get_date_text,
    get_fitness_tip_text,
    get_friend_reply_text,
    get_greeting_text,
    get_help_text,
    get_how_are_you_text,
    get_joke_text,
    get_money_tip_text,
    get_motivation_text,
    get_sleep_tip_text,
    get_study_tip_text,
    get_thanks_reply_text,
    get_time_text,
)
from voice_assistant.skills.study import build_study_plan, explain_topic, quiz_topic
from voice_assistant.skills.tasks import (
    add_task,
    clear_tasks,
    complete_task,
    delete_task,
    list_tasks_text,
    load_tasks,
    save_tasks,
)
from voice_assistant.skills.translate import supported_languages_text, translate_text
from voice_assistant.skills.web import open_site, search_web
from voice_assistant.storage.sqlite_store import MigrationSources, SQLiteStore
try:
    from voice_assistant.skills.google_sync import (
        google_login,
        sync_google_calendar_pull,
        sync_google_calendar_push,
        sync_google_contacts,
    )
    GOOGLE_LIBS_AVAILABLE = True
except ModuleNotFoundError:
    GOOGLE_LIBS_AVAILABLE = False
import threading
import time


class VoiceAssistant:
    def __init__(self) -> None:
        self.settings = Settings()
        Path(".data").mkdir(exist_ok=True)
        self.logger = setup_logging(self.settings.log_file, self.settings.log_level)
        self.listener = Listener(
            ambient_duration=self.settings.ambient_duration,
            use_vad=True,
            wake_word=self.settings.wake_word if self.settings.wake_word_enabled else None,
        )
        self.speaker = Speaker(rate=self.settings.voice_rate, enabled=self.settings.tts_enabled)
        self.store: SQLiteStore | None = None

        if self.settings.use_sqlite_storage:
            self.store = SQLiteStore(
                self.settings.sqlite_db_file,
                sources=MigrationSources(
                    reminders_file=self.settings.reminders_file,
                    tasks_file=self.settings.tasks_file,
                    profile_file=self.settings.profile_file,
                    expenses_file=self.settings.expenses_file,
                    habits_file=self.settings.habits_file,
                    history_file=self.settings.history_file,
                    contacts_file=self.settings.contacts_file,
                    events_file=self.settings.events_file,
                ),
            )
            self.reminders = self.store.load_reminders()
            self.tasks = self.store.load_tasks()
            self.profile = self.store.load_profile()
            self.expenses = self.store.load_expenses()
            self.habits = self.store.load_habits()
            self.contacts = self.store.load_contacts()
            self.events = self.store.load_events()
        else:
            self.reminders = load_reminders(self.settings.reminders_file)
            self.tasks = load_tasks(self.settings.tasks_file)
            self.profile = load_profile(self.settings.profile_file)
            self.expenses = load_expenses(self.settings.expenses_file)
            self.habits = load_habits(self.settings.habits_file)
            self.contacts = load_contacts(self.settings.contacts_file)
            self.events = load_events(self.settings.events_file)
        self.google_enabled = self.settings.google_sync_enabled
        self.last_action: dict[str, object] | None = None
        self.wake_word_enabled = self.settings.wake_word_enabled
        self.wake_word = self.settings.wake_word.lower().strip()
        self._awake = not self.wake_word_enabled
        if self.google_enabled and GOOGLE_LIBS_AVAILABLE and self.settings.google_auto_sync_minutes > 0:
            threading.Thread(target=self._google_auto_sync_loop, daemon=True).start()

    def _append_history(self, role: str, text: str) -> None:
        try:
            if self.store:
                self.store.append_history(role, text)
            else:
                append_history(self.settings.history_file, role, text)
        except Exception:
            self.logger.exception("Failed to append history")

    def _google_auto_sync_loop(self) -> None:
        interval = max(1, self.settings.google_auto_sync_minutes) * 60
        while True:
            try:
                events = sync_google_calendar_pull(
                    self.settings.google_credentials_file,
                    self.settings.google_token_file,
                    self.settings.google_calendar_id,
                )
                self.events.extend(events)
                self._persist_events()
                imported = sync_google_contacts(
                    self.settings.google_credentials_file,
                    self.settings.google_token_file,
                )
                for name, number in imported:
                    add_contact(self.contacts, name, number)
                self._persist_contacts()
            except Exception:
                self.logger.exception("Auto Google sync failed")
            time.sleep(interval)

    def _history_text(self) -> str:
        if self.store:
            return self.store.history_text()
        return history_text(self.settings.history_file)

    def _clear_history(self) -> str:
        if self.store:
            return self.store.clear_history()
        return clear_history(self.settings.history_file)

    def _persist_profile(self) -> None:
        if self.store:
            self.store.save_profile(self.profile)
        else:
            save_profile(self.settings.profile_file, self.profile)

    def _persist_reminders(self) -> None:
        if self.store:
            self.store.save_reminders(self.reminders)
        else:
            save_reminders(self.settings.reminders_file, self.reminders)

    def _persist_tasks(self) -> None:
        if self.store:
            self.store.save_tasks(self.tasks)
        else:
            save_tasks(self.settings.tasks_file, self.tasks)

    def _persist_expenses(self) -> None:
        if self.store:
            self.store.save_expenses(self.expenses)
        else:
            save_expenses(self.settings.expenses_file, self.expenses)

    def _persist_habits(self) -> None:
        if self.store:
            self.store.save_habits(self.habits)
        else:
            save_habits(self.settings.habits_file, self.habits)

    def _persist_contacts(self) -> None:
        if self.store:
            self.store.save_contacts(self.contacts)
        else:
            save_contacts(self.settings.contacts_file, self.contacts)

    def _persist_events(self) -> None:
        if self.store:
            self.store.save_events(self.events)
        else:
            save_events(self.settings.events_file, self.events)

    def _say(self, text: str) -> None:
        try:
            self.speaker.say(text)
        except Exception:
            self.logger.exception("Failed to speak response")
        self._append_history("assistant", text)

    def _get_command(self) -> str:
        try:
            spoken = self.listener.listen(
                timeout=self.settings.listen_timeout,
                phrase_time_limit=self.settings.phrase_time_limit,
            )
        except Exception:
            self.logger.exception("Voice listen failed; using typed fallback")
            spoken = None
        if spoken:
            print(f"You said: {spoken}")
            if self.wake_word_enabled and not self._awake:
                if self.wake_word in spoken.lower():
                    self._awake = True
                    self._say("I'm listening.")
                return ""
            return spoken
        if self.wake_word_enabled and not self._awake:
            return ""
        return input("Type command (mic fallback): ").strip().lower()

    def _handle(self, command: str) -> bool:
        try:
            self._append_history("user", command)
            intent = parse_intent(command)

            if intent.intent_type == IntentType.EXIT:
                self._say("Goodbye.")
                return False
            if self.wake_word_enabled:
                self._awake = False

            if intent.intent_type == IntentType.GET_TIME:
                self._say(get_time_text())
                return True

            if intent.intent_type == IntentType.GET_DATE:
                self._say(get_date_text())
                return True

            if intent.intent_type == IntentType.GREETING:
                name = self.profile.get("name")
                self._say(f"Hi {name}. Nice to hear from you." if name else get_greeting_text())
                return True

            if intent.intent_type == IntentType.HOW_ARE_YOU:
                self._say(get_how_are_you_text())
                return True

            if intent.intent_type == IntentType.DAILY_CHORES:
                self._say(get_daily_chores_text())
                return True

            if intent.intent_type == IntentType.MOTIVATION:
                self._say(get_motivation_text())
                return True

            if intent.intent_type == IntentType.THANKS:
                self._say(get_thanks_reply_text())
                return True

            if intent.intent_type == IntentType.SET_NAME and intent.payload:
                formatted = intent.payload.strip().split()[0].capitalize()
                self.profile["name"] = formatted
                self._persist_profile()
                self._say(f"Nice to meet you, {formatted}. I will remember your name.")
                return True

            if intent.intent_type == IntentType.GET_NAME:
                name = self.profile.get("name")
                self._say(f"Your name is {name}." if name else "I do not know your name yet. You can say: my name is Sunil.")
                return True

            if intent.intent_type == IntentType.CHECK_IN:
                self._say(get_check_in_text(self.profile.get("name")))
                return True

            if intent.intent_type == IntentType.BREATHING:
                self._say(get_breathing_text())
                return True

            if intent.intent_type == IntentType.AFFIRMATION:
                self._say(get_affirmation_text())
                return True

            if intent.intent_type == IntentType.STUDY_TIP:
                self._say(get_study_tip_text())
                return True

            if intent.intent_type == IntentType.FITNESS_TIP:
                self._say(get_fitness_tip_text())
                return True

            if intent.intent_type == IntentType.MONEY_TIP:
                self._say(get_money_tip_text())
                return True

            if intent.intent_type == IntentType.SLEEP_TIP:
                self._say(get_sleep_tip_text())
                return True

            if intent.intent_type == IntentType.HELP:
                self._say(get_help_text())
                return True

            if intent.intent_type == IntentType.ADD_EXPENSE and intent.payload:
                amount_str, category = intent.payload.split("|", 1)
                reply = add_expense(self.expenses, float(amount_str), category)
                self._persist_expenses()
                self.last_action = {"kind": "expense_add", "amount": float(amount_str), "category": category}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.SHOW_EXPENSES:
                self._say(show_expenses_text(self.expenses))
                return True

            if intent.intent_type == IntentType.EXPENSE_REPORT:
                self._say(monthly_expense_report_text(self.expenses))
                return True

            if intent.intent_type == IntentType.ADD_HABIT and intent.payload:
                reply = add_habit(self.habits, intent.payload)
                self._persist_habits()
                self.last_action = {"kind": "habit_add", "name": intent.payload}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.DONE_HABIT and intent.payload:
                reply = done_habit(self.habits, intent.payload)
                self._persist_habits()
                self.last_action = {"kind": "habit_done", "name": intent.payload}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.SHOW_HABITS:
                self._say(show_habits_text(self.habits))
                return True

            if intent.intent_type == IntentType.DAY_SUMMARY:
                pending = sum(1 for task in self.tasks if not bool(task.get("done")))
                done = sum(1 for task in self.tasks if bool(task.get("done")))
                reminders = len(self.reminders)
                expense_reply = monthly_expense_report_text(self.expenses)
                self._say(
                    f"Day summary. Tasks pending: {pending}. Tasks done: {done}. "
                    f"Active reminders: {reminders}. {expense_reply}"
                )
                return True

            if intent.intent_type == IntentType.SHOW_HISTORY:
                self._say(self._history_text())
                return True

            if intent.intent_type == IntentType.CLEAR_HISTORY:
                self._say(self._clear_history())
                return True

            if intent.intent_type == IntentType.TRANSLATE and intent.payload:
                self._say(translate_text(intent.payload, api_url=self.settings.translation_api_url))
                return True

            if intent.intent_type == IntentType.SHOW_TRANSLATE_LANGS:
                self._say(supported_languages_text())
                return True

            if intent.intent_type == IntentType.ADD_REMINDER and intent.payload:
                self.reminders.append(intent.payload)
                self._persist_reminders()
                self.last_action = {"kind": "reminder_add", "text": intent.payload}
                self._say(f"Reminder added: {intent.payload}")
                return True

            if intent.intent_type == IntentType.LIST_REMINDERS:
                self._say("Your reminders are: " + "; ".join(self.reminders) if self.reminders else "You do not have any reminders yet.")
                return True

            if intent.intent_type == IntentType.DELETE_REMINDER and intent.payload:
                reply = delete_reminder(self.reminders, int(intent.payload))
                self._persist_reminders()
                self.last_action = {"kind": "reminder_delete"}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.CLEAR_REMINDERS:
                reply = clear_reminders(self.reminders)
                self._persist_reminders()
                self.last_action = {"kind": "reminder_clear"}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.ADD_TASK and intent.payload:
                reply = add_task(self.tasks, intent.payload)
                self._persist_tasks()
                self.last_action = {"kind": "task_add", "text": intent.payload}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.LIST_TASKS:
                self._say(list_tasks_text(self.tasks))
                return True

            if intent.intent_type == IntentType.COMPLETE_TASK and intent.payload:
                reply = complete_task(self.tasks, int(intent.payload))
                self._persist_tasks()
                self.last_action = {"kind": "task_complete", "index": int(intent.payload)}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.DELETE_TASK and intent.payload:
                reply = delete_task(self.tasks, int(intent.payload))
                self._persist_tasks()
                self.last_action = {"kind": "task_delete", "index": int(intent.payload)}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.CLEAR_TASKS:
                reply = clear_tasks(self.tasks)
                self._persist_tasks()
                self.last_action = {"kind": "task_clear"}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.ADD_CONTACT and intent.payload:
                name, number = intent.payload.split("|", 1)
                reply = add_contact(self.contacts, name, number)
                self._persist_contacts()
                self.last_action = {"kind": "contact_add", "name": name, "number": number}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.LIST_CONTACTS:
                self._say(list_contacts_text(self.contacts))
                return True

            if intent.intent_type == IntentType.CALL_CONTACT and intent.payload:
                number = resolve_contact_number(self.contacts, intent.payload)
                if not number:
                    self._say(f"I do not have contact {intent.payload}. Add it first.")
                else:
                    self._say(
                        make_call(
                            number,
                            adb_enabled=self.settings.phone_adb_enabled,
                            adb_path=self.settings.phone_adb_path,
                        )
                    )
                return True

            if intent.intent_type == IntentType.SMS_CONTACT and intent.payload:
                name, message = intent.payload.split("|", 1)
                number = resolve_contact_number(self.contacts, name)
                if not number:
                    self._say(f"I do not have contact {name}. Add it first.")
                else:
                    self._say(
                        send_sms(
                            number,
                            message,
                            adb_enabled=self.settings.phone_adb_enabled,
                            adb_path=self.settings.phone_adb_path,
                        )
                    )
                return True

            if intent.intent_type == IntentType.WHATSAPP_MESSAGE and intent.payload:
                target, message = intent.payload.split("|", 1)
                number = resolve_contact_number(self.contacts, target) or target
                self._say(
                    send_whatsapp_message(
                        number,
                        message,
                        adb_enabled=self.settings.phone_adb_enabled,
                        adb_path=self.settings.phone_adb_path,
                    )
                )
                return True

            if intent.intent_type == IntentType.ADD_EVENT and intent.payload:
                title, when = intent.payload.split("|", 1)
                reply = add_event(self.events, title, when)
                self._persist_events()
                self.last_action = {"kind": "event_add", "title": title, "when": when}
                self._say(reply)
                return True

            if intent.intent_type == IntentType.SHOW_SCHEDULE:
                self._say(show_schedule_text(self.events))
                return True

            if intent.intent_type == IntentType.SYNC_TASKS_CALENDAR:
                reply = sync_tasks_to_calendar(self.tasks, self.events)
                self._persist_events()
                self._say(reply)
                return True

            if intent.intent_type == IntentType.GOOGLE_LOGIN:
                if not self.google_enabled:
                    self._say("Google sync is disabled. Set GOOGLE_SYNC_ENABLED=true in .env and retry.")
                    return True
                if not GOOGLE_LIBS_AVAILABLE:
                    self._say("Google sync libraries are missing. Install google-auth, google-auth-oauthlib, google-api-python-client.")
                    return True
                self._say(
                    google_login(
                        self.settings.google_credentials_file,
                        self.settings.google_token_file,
                    )
                )
                return True

            if intent.intent_type == IntentType.GOOGLE_SYNC_CONTACTS:
                if not self.google_enabled:
                    self._say("Google sync is disabled. Set GOOGLE_SYNC_ENABLED=true in .env and retry.")
                    return True
                if not GOOGLE_LIBS_AVAILABLE:
                    self._say("Google sync libraries are missing. Install google-auth, google-auth-oauthlib, google-api-python-client.")
                    return True
                try:
                    imported = sync_google_contacts(
                        self.settings.google_credentials_file,
                        self.settings.google_token_file,
                    )
                    added = 0
                    for name, number in imported:
                        if add_contact(self.contacts, name, number).startswith("Saved"):
                            added += 1
                    if added:
                        self._persist_contacts()
                    self._say(f"Imported {added} Google contacts.")
                    self.last_action = {"kind": "contacts_sync", "added": added}
                except Exception as exc:
                    self._say(f"Google contacts sync failed: {exc}")
                return True

            if intent.intent_type == IntentType.GOOGLE_SYNC_CALENDAR:
                if not self.google_enabled:
                    self._say("Google sync is disabled. Set GOOGLE_SYNC_ENABLED=true in .env and retry.")
                    return True
                if not GOOGLE_LIBS_AVAILABLE:
                    self._say("Google sync libraries are missing. Install google-auth, google-auth-oauthlib, google-api-python-client.")
                    return True
                try:
                    events = sync_google_calendar_pull(
                        self.settings.google_credentials_file,
                        self.settings.google_token_file,
                        self.settings.google_calendar_id,
                    )
                    self.events.extend(events)
                    self._persist_events()
                    self._say(f"Imported {len(events)} events from Google Calendar.")
                    self.last_action = {"kind": "events_sync", "count": len(events)}
                except Exception as exc:
                    self._say(f"Google Calendar sync failed: {exc}")
                return True

            if intent.intent_type == IntentType.GOOGLE_PUSH_EVENTS:
                if not self.google_enabled:
                    self._say("Google sync is disabled. Set GOOGLE_SYNC_ENABLED=true in .env and retry.")
                    return True
                if not GOOGLE_LIBS_AVAILABLE:
                    self._say("Google sync libraries are missing. Install google-auth, google-auth-oauthlib, google-api-python-client.")
                    return True
                try:
                    reply = sync_google_calendar_push(
                        self.settings.google_credentials_file,
                        self.settings.google_token_file,
                        self.settings.google_calendar_id,
                        self.events,
                    )
                    self._say(reply)
                    self.last_action = {"kind": "events_push"}
                except Exception as exc:
                    self._say(f"Google Calendar push failed: {exc}")
                return True

            if intent.intent_type == IntentType.PHONE_CALL and intent.payload:
                self._say(
                    make_call(
                        intent.payload,
                        adb_enabled=self.settings.phone_adb_enabled,
                        adb_path=self.settings.phone_adb_path,
                    )
                )
                return True

            if intent.intent_type == IntentType.PHONE_SMS and intent.payload:
                number, message = intent.payload.split("|", 1)
                self._say(
                    send_sms(
                        number,
                        message,
                        adb_enabled=self.settings.phone_adb_enabled,
                        adb_path=self.settings.phone_adb_path,
                    )
                )
                return True

            if intent.intent_type == IntentType.PHONE_OPEN_APP and intent.payload:
                self._say(
                    open_phone_app(
                        intent.payload,
                        adb_enabled=self.settings.phone_adb_enabled,
                        adb_path=self.settings.phone_adb_path,
                    )
                )
                return True

            if intent.intent_type == IntentType.STUDY_PLAN and intent.payload:
                self._say(build_study_plan(intent.payload))
                return True

            if intent.intent_type == IntentType.STUDY_EXPLAIN and intent.payload:
                self._say(explain_topic(intent.payload))
                return True

            if intent.intent_type == IntentType.STUDY_QUIZ and intent.payload:
                self._say(quiz_topic(intent.payload))
                return True

            if intent.intent_type == IntentType.OPEN_SITE and intent.payload:
                self._say(open_site(intent.payload))
                return True

            if intent.intent_type == IntentType.SEARCH_WEB and intent.payload:
                self._say(search_web(intent.payload))
                return True

            if intent.intent_type == IntentType.SAVE_NOTE and intent.payload:
                self._say(save_note(intent.payload, self.settings.notes_file))
                return True

            if intent.intent_type == IntentType.CALCULATE and intent.payload:
                self._say(calculate_expression(intent.payload))
                return True

            if intent.intent_type == IntentType.JOKE:
                self._say(get_joke_text())
                return True

            if intent.intent_type == IntentType.UNDO:
                if not self.last_action:
                    self._say("Nothing to undo.")
                    return True
                la = self.last_action
                self.last_action = None
                kind = la.get("kind")
                if kind == "contact_add":
                    name = la.get("name", "")
                    self.contacts.pop(str(name).strip().lower(), None)
                    self._persist_contacts()
                    self._say(f"Undid contact add: {name}")
                    return True
                if kind == "reminder_add":
                    text = la.get("text")
                    if text in self.reminders:
                        self.reminders.remove(text)
                        self._persist_reminders()
                    self._say("Undid reminder add.")
                    return True
                if kind == "task_add":
                    text = la.get("text")
                    for idx, t in enumerate(self.tasks):
                        if t.get("text") == text:
                            self.tasks.pop(idx)
                            break
                    self._persist_tasks()
                    self._say("Undid task add.")
                    return True
                if kind == "task_complete":
                    idx = la.get("index")
                    if isinstance(idx, int) and 1 <= idx <= len(self.tasks):
                        self.tasks[idx - 1]["done"] = False
                        self._persist_tasks()
                    self._say("Undid task complete.")
                    return True
                if kind == "event_add":
                    title = la.get("title")
                    when = la.get("when")
                    self.events = [e for e in self.events if not (e.get("title") == title and e.get("when") == when)]
                    self._persist_events()
                    self._say("Undid event add.")
                    return True
                if kind == "expense_add":
                    amt = la.get("amount")
                    cat = la.get("category")
                    for idx, e in enumerate(reversed(self.expenses)):
                        if e.get("amount") == amt and e.get("category") == cat:
                            del self.expenses[len(self.expenses) - 1 - idx]
                            break
                    self._persist_expenses()
                    self._say("Undid expense add.")
                    return True
                if kind == "habit_add":
                    name = la.get("name")
                    if isinstance(name, str):
                        self.habits.pop(name.strip().lower(), None)
                        self._persist_habits()
                    self._say("Undid habit add.")
                    return True
                if kind == "habit_done":
                    name = la.get("name")
                    if isinstance(name, str) and name.strip().lower() in self.habits:
                        self.habits[name.strip().lower()] = max(0, self.habits[name.strip().lower()] - 1)
                        self._persist_habits()
                    self._say("Undid habit progress.")
                    return True
                self._say("Undo not available for that action yet.")
                return True

            if self.settings.llm_enabled:
                llm_reply = generate_llm_reply(
                    command,
                    history_file=self.settings.history_file,
                    api_key=self.settings.llm_api_key,
                    model=self.settings.llm_model,
                    base_url=self.settings.llm_base_url,
                    timeout_seconds=self.settings.llm_timeout_seconds,
                )
                if llm_reply:
                    self._say(llm_reply)
                    return True

            self._say(get_friend_reply_text(command))
            return True
        except Exception:
            self.logger.exception("Unhandled error while processing command")
            self._say("I hit an internal error. Please try again.")
            return True

    def run(self) -> None:
        name = self.profile.get("name")
        if name:
            self._say(f"Hello {name}, I am {self.settings.assistant_name}. How can I support you today?")
        else:
            self._say(f"Hello, I am {self.settings.assistant_name}. How can I help you today?")
        self._run_loop()

    def _run_loop(self) -> None:
        is_running = True
        while is_running:
            try:
                command = self._get_command()
                if not command:
                    continue
                is_running = self._handle(command)
            except (EOFError, KeyboardInterrupt):
                self._say("Goodbye.")
                break
