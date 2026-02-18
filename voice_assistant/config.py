from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv() -> None:
        return None


load_dotenv()


def _to_bool(value: str, default: bool = True) -> bool:
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    return default


@dataclass(frozen=True)
class Settings:
    assistant_name: str = os.getenv("ASSISTANT_NAME", "Nova")
    voice_rate: int = int(os.getenv("VOICE_RATE", "180"))
    tts_enabled: bool = _to_bool(os.getenv("TTS_ENABLED", "true"))
    listen_timeout: float = float(os.getenv("LISTEN_TIMEOUT", "2.0"))
    phrase_time_limit: float = float(os.getenv("PHRASE_TIME_LIMIT", "5.0"))
    ambient_duration: float = float(os.getenv("AMBIENT_DURATION", "0.15"))
    notes_file: str = os.getenv("NOTES_FILE", "notes.txt")
    reminders_file: str = os.getenv("REMINDERS_FILE", "reminders.json")
    tasks_file: str = os.getenv("TASKS_FILE", "tasks.json")
    profile_file: str = os.getenv("PROFILE_FILE", "profile.json")
    expenses_file: str = os.getenv("EXPENSES_FILE", "expenses.json")
    habits_file: str = os.getenv("HABITS_FILE", "habits.json")
    history_file: str = os.getenv("HISTORY_FILE", "history.jsonl")
    llm_enabled: bool = _to_bool(os.getenv("LLM_ENABLED", "false"))
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1/chat/completions")
    llm_timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "8.0"))
    translation_api_url: str = os.getenv("TRANSLATION_API_URL", "")
    use_sqlite_storage: bool = _to_bool(os.getenv("USE_SQLITE_STORAGE", "true"))
    sqlite_db_file: str = os.getenv("SQLITE_DB_FILE", ".data/assistant_state.db")
    log_file: str = os.getenv("LOG_FILE", ".data/assistant.log")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    phone_adb_enabled: bool = _to_bool(os.getenv("PHONE_ADB_ENABLED", "false"))
    phone_adb_path: str = os.getenv("PHONE_ADB_PATH", "adb")
    contacts_file: str = os.getenv("CONTACTS_FILE", "contacts.json")
    events_file: str = os.getenv("EVENTS_FILE", "events.json")
    google_sync_enabled: bool = _to_bool(os.getenv("GOOGLE_SYNC_ENABLED", "false"))
    google_credentials_file: str = os.getenv("GOOGLE_CREDENTIALS_FILE", ".data/google_credentials.json")
    google_token_file: str = os.getenv("GOOGLE_TOKEN_FILE", ".data/google_token.json")
    google_calendar_id: str = os.getenv("GOOGLE_CALENDAR_ID", "primary")
    google_auto_sync_minutes: int = int(os.getenv("GOOGLE_AUTO_SYNC_MINUTES", "0"))
    wake_word_enabled: bool = _to_bool(os.getenv("WAKE_WORD_ENABLED", "false"))
    wake_word: str = os.getenv("WAKE_WORD", "nova")
