from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class IntentType(str, Enum):
    GET_TIME = "get_time"
    GET_DATE = "get_date"
    OPEN_SITE = "open_site"
    SEARCH_WEB = "search_web"
    SAVE_NOTE = "save_note"
    JOKE = "joke"
    GREETING = "greeting"
    HOW_ARE_YOU = "how_are_you"
    DAILY_CHORES = "daily_chores"
    MOTIVATION = "motivation"
    THANKS = "thanks"
    ADD_REMINDER = "add_reminder"
    LIST_REMINDERS = "list_reminders"
    DELETE_REMINDER = "delete_reminder"
    CLEAR_REMINDERS = "clear_reminders"
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    CLEAR_TASKS = "clear_tasks"
    CALCULATE = "calculate"
    SET_NAME = "set_name"
    GET_NAME = "get_name"
    CHECK_IN = "check_in"
    BREATHING = "breathing"
    AFFIRMATION = "affirmation"
    STUDY_TIP = "study_tip"
    FITNESS_TIP = "fitness_tip"
    MONEY_TIP = "money_tip"
    SLEEP_TIP = "sleep_tip"
    ADD_EXPENSE = "add_expense"
    SHOW_EXPENSES = "show_expenses"
    EXPENSE_REPORT = "expense_report"
    ADD_HABIT = "add_habit"
    DONE_HABIT = "done_habit"
    SHOW_HABITS = "show_habits"
    DAY_SUMMARY = "day_summary"
    SHOW_HISTORY = "show_history"
    CLEAR_HISTORY = "clear_history"
    TRANSLATE = "translate"
    SHOW_TRANSLATE_LANGS = "show_translate_langs"
    PHONE_CALL = "phone_call"
    PHONE_SMS = "phone_sms"
    PHONE_OPEN_APP = "phone_open_app"
    STUDY_PLAN = "study_plan"
    STUDY_EXPLAIN = "study_explain"
    STUDY_QUIZ = "study_quiz"
    ADD_CONTACT = "add_contact"
    LIST_CONTACTS = "list_contacts"
    CALL_CONTACT = "call_contact"
    SMS_CONTACT = "sms_contact"
    WHATSAPP_MESSAGE = "whatsapp_message"
    ADD_EVENT = "add_event"
    SHOW_SCHEDULE = "show_schedule"
    SYNC_TASKS_CALENDAR = "sync_tasks_calendar"
    GOOGLE_LOGIN = "google_login"
    GOOGLE_SYNC_CONTACTS = "google_sync_contacts"
    GOOGLE_SYNC_CALENDAR = "google_sync_calendar"
    GOOGLE_PUSH_EVENTS = "google_push_events"
    UNDO = "undo"
    HELP = "help"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Intent:
    intent_type: IntentType
    payload: str | None = None


def _extract_after_phrase(text: str, phrases: tuple[str, ...]) -> str | None:
    for phrase in phrases:
        if phrase in text:
            value = text.split(phrase, 1)[1].strip(" .!?")
            if value:
                return value
    return None


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(word in text for word in keywords)


def _normalize_text(text: str) -> str:
    cleaned = text.lower().strip()
    cleaned = re.sub(r"[\t\r\n]+", " ", cleaned)
    cleaned = re.sub(r"[!,?;\"()\[\]{}]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)

    regex_phrase_patterns: list[tuple[str, str]] = [
        (r"^నాకు గుర్తు చేయి\s+(.+)$", r"remind me to \1"),
        (r"^naaku gurtu cheyi\s+(.+)$", r"remind me to \1"),
        (r"^gurtu cheyi\s+(.+)$", r"remind me to \1"),
        (r"^मुझे याद दिलाओ\s+(.+)$", r"remind me to \1"),
        (r"^mujhe yaad dilao\s+(.+)$", r"remind me to \1"),
        (r"^recu[eé]rdame\s+(.+)$", r"remind me to \1"),
        (r"^గుర్తుచేయి\s+(.+)$", r"remind me to \1"),
        (r"^open cheyi\s+(.+)$", r"open \1"),
        (r"^తెరువు\s+(.+)$", r"open \1"),
        (r"^खोलो\s+(.+)$", r"open \1"),
        (r"^kholo\s+(.+)$", r"open \1"),
        (r"^abrir\s+(.+)$", r"open \1"),
        (r"^abre\s+(.+)$", r"open \1"),
        (r"^వెతుకు\s+(.+)$", r"search \1"),
        (r"^ढूंढो\s+(.+)$", r"search \1"),
        (r"^buscar\s+(.+)$", r"search \1"),
        (r"^nota\s+(.+)$", r"note \1"),
        (r"^గమనిక\s+(.+)$", r"note \1"),
        (r"^नोट\s+(.+)$", r"note \1"),
        (r"^చూపు రిమైండర్లు$", r"show reminders"),
        (r"^recordatorios$", r"show reminders"),
        (r"^reminders dikhao$", r"show reminders"),
        (r"^చూపు tasks$", r"show tasks"),
        (r"^tareas$", r"show tasks"),
        (r"^tasks dikhao$", r"show tasks"),
        (r"^add task\s+(.+)$", r"add task \1"),
        (r"^పని జోడించు\s+(.+)$", r"add task \1"),
        (r"^kaam jodo\s+(.+)$", r"add task \1"),
        (r"^tarea\s+(.+)$", r"add task \1"),
    ]
    for pattern, replacement in regex_phrase_patterns:
        cleaned = re.sub(pattern, replacement, cleaned)

    phrase_map = {
        "gud mrng": "good morning",
        "gd mrng": "good morning",
        "whats up": "what is up",
        "watsup": "what is up",
        "wru": "where are you",
        "hru": "how are you",
        "wyd": "what are you doing",
        "idk": "i do not know",
        "dont": "do not",
        "cant": "can not",
        "wanna": "want to",
        "gonna": "going to",
        "kinda": "kind of",
        "sorta": "sort of",
        "namaste": "hello",
        "hola": "hello",
        "bonjour": "hello",
        "nuvvu ela unnava": "how are you",
        "ela unnava": "how are you",
        "ela unnav": "how are you",
        "ela unav": "how are you",
        "ela unavu": "how are you",
        "bagunnava": "how are you",
        "bagunava": "how are you",
        "bagunnava?": "how are you",
        "mee peru enti": "what is my name",
        "samayam entha": "what is time",
        "samayam enta": "what is time",
        "thedi emiti": "what is date",
        "tarikh kya hai": "what is date",
        "que hora es": "what is time",
        "que fecha es": "what is date",
        "como estas": "how are you",
        "kya kar sakte ho": "what can you do",
        "ayuda": "help",
        "gracias": "thanks",
        "dhanyavad": "thanks",
        "shukriya": "thanks",
        "adios": "goodbye",
        "hasta luego": "goodbye",
        "buenos dias": "good morning",
        "buenas noches": "good night",
        "నమస్తే": "hello",
        "హలో": "hello",
        "హాయ్": "hello",
        "నువ్వు ఎలా ఉన్నావు": "how are you",
        "సమయం ఎంత": "what is time",
        "సమయం ఎంతా": "what is time",
        "తేదీ ఏమిటి": "what is date",
        "నా పేరు ఏమిటి": "what is my name",
        "నాకు సహాయం చేయి": "help",
        "ధన్యవాదాలు": "thanks",
        "వీడ్కోలు": "goodbye",
        "नमस्ते": "hello",
        "कैसे हो": "how are you",
        "समय क्या है": "what is time",
        "तारीख क्या है": "what is date",
        "मेरा नाम क्या है": "what is my name",
        "धन्यवाद": "thanks",
        "अलविदा": "goodbye",
    }
    for src, dst in phrase_map.items():
        cleaned = re.sub(rf"(?<!\S){re.escape(src)}(?!\S)", dst, cleaned)

    token_map = {
        "u": "you",
        "ur": "your",
        "r": "are",
        "pls": "please",
        "plz": "please",
        "thx": "thanks",
        "ty": "thank you",
        "im": "i am",
        "luv": "love",
        "bro": "friend",
        "sis": "friend",
        "gm": "good morning",
        "gn": "good night",
        "tmrw": "tomorrow",
        "2day": "today",
    }
    tokens = [token_map.get(token, token) for token in cleaned.split()]
    cleaned = " ".join(tokens)
    return re.sub(r"\s+", " ", cleaned).strip()


def _extract_site_name(text: str) -> str | None:
    patterns = (
        r"(?:open|launch|go to)\s+([a-z0-9\.-]+)",
        r"(?:can you|please)\s+(?:open|launch)\s+([a-z0-9\.-]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(" .!?")
    return None


def _extract_index(text: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def _extract_expense(text: str) -> str | None:
    patterns = (
        r"(?:spent|spend)\s+(\d+(?:\.\d+)?)\s+(?:on|for)\s+(.+)",
        r"add expense\s+(\d+(?:\.\d+)?)\s+(.+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            amount = match.group(1).strip()
            category = match.group(2).strip(" .!?")
            if amount and category:
                return f"{amount}|{category}"
    return None


def _extract_translation(text: str) -> str | None:
    patterns = (
        r"translate\s+(.+?)\s+to\s+([a-z]+)$",
        r"what is\s+(.+?)\s+in\s+([a-z]+)$",
        r"how to say\s+(.+?)\s+in\s+([a-z]+)$",
        r"translate to\s+([a-z]+)\s+(.+)$",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        if pattern.startswith("translate to"):
            target = match.group(1).strip()
            phrase = match.group(2).strip(" .!?")
        else:
            phrase = match.group(1).strip(" .!?")
            target = match.group(2).strip()
        if phrase and target:
            return f"{target}|{phrase}"
    return None


def _extract_phone_number(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\-\s]{7,}\d)", text)
    if not match:
        return None
    return re.sub(r"[^\d+]", "", match.group(1))


def _extract_phone_sms(text: str) -> str | None:
    patterns = (
        r"(?:send|text|sms)\s+(?:to\s+)?(\+?\d[\d\-\s]{7,}\d)\s+(?:saying|message|that)\s+(.+)",
        r"(?:send|text|sms)\s+(.+)\s+to\s+(\+?\d[\d\-\s]{7,}\d)",
    )
    for idx, pattern in enumerate(patterns):
        match = re.search(pattern, text)
        if not match:
            continue
        if idx == 0:
            number = re.sub(r"[^\d+]", "", match.group(1))
            message = match.group(2).strip(" .!?")
        else:
            message = match.group(1).strip(" .!?")
            number = re.sub(r"[^\d+]", "", match.group(2))
        if number and message:
            return f"{number}|{message}"
    return None


def _extract_open_app(text: str) -> str | None:
    match = re.search(r"(?:open|launch|start)\s+app\s+(.+)$", text)
    if match:
        return match.group(1).strip(" .!?")
    match = re.search(r"(?:open|launch|start)\s+(.+)$", text)
    if match:
        candidate = match.group(1).strip(" .!?")
        if candidate and "." not in candidate and "http" not in candidate:
            return candidate
    return None


def _extract_contact_add(text: str) -> str | None:
    patterns = (
        r"(?:add|save)\s+contact\s+([a-zA-Z ]+)\s+(?:number\s+)?(\+?\d[\d\-\s]{7,}\d)",
        r"contact\s+([a-zA-Z ]+)\s+is\s+(\+?\d[\d\-\s]{7,}\d)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip().lower()
            number = re.sub(r"[^\d+]", "", match.group(2))
            if name and number:
                return f"{name}|{number}"
    return None


def _extract_contact_sms(text: str) -> str | None:
    patterns = (
        r"(?:sms|text)\s+([a-zA-Z ]+)\s+(?:message|saying|that)\s+(.+)",
        r"(?:sms|text)\s+(.+)\s+to\s+([a-zA-Z ]+)",
    )
    for idx, pattern in enumerate(patterns):
        match = re.search(pattern, text)
        if not match:
            continue
        if idx == 0:
            name = match.group(1).strip().lower()
            message = match.group(2).strip(" .!?")
        else:
            message = match.group(1).strip(" .!?")
            name = match.group(2).strip().lower()
        if name and message:
            return f"{name}|{message}"
    return None


def _extract_whatsapp(text: str) -> str | None:
    patterns = (
        r"(?:whatsapp|wa)\s+(?:to\s+)?(.+?)\s+(?:message|saying|that)\s+(.+)",
        r"send whatsapp to\s+(.+?)\s+(?:message|saying|that)\s+(.+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            target = match.group(1).strip()
            message = match.group(2).strip(" .!?")
            if target and message:
                return f"{target}|{message}"
    return None


def _extract_event(text: str) -> str | None:
    patterns = (
        r"(?:add|create|schedule)\s+event\s+(.+?)\s+at\s+([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2})",
        r"(?:add|create|schedule)\s+event\s+(.+?)\s+on\s+([0-9]{4}-[0-9]{2}-[0-9]{2})",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip(" .!?")
            when = match.group(2).strip()
            if len(when) == 10:
                when = when + " 10:00"
            if title and when:
                return f"{title}|{when}"
    return None


def _is_greeting(text: str) -> bool:
    if text in ("hi", "hello", "hey", "good morning", "good evening", "what's up", "whats up"):
        return True
    return bool(re.match(r"^(hi|hello|hey)\b", text))


def _looks_like_math_expression(expr: str) -> bool:
    compact = expr.replace(" ", "")
    if not any(ch.isdigit() for ch in compact):
        return False
    return bool(re.fullmatch(r"[0-9\.\+\-\*/%\^()]+", compact))


def parse_intent(command: str) -> Intent:
    text = _normalize_text(command)

    if _contains_any(text, ("exit", "quit", "stop", "goodbye", "bye")):
        return Intent(IntentType.EXIT)

    if _is_greeting(text):
        return Intent(IntentType.GREETING)

    if _contains_any(text, ("how are you", "how do you feel", "are you okay")):
        return Intent(IntentType.HOW_ARE_YOU)

    if _contains_any(text, ("daily chores", "plan my day", "routine for today", "today plan")):
        return Intent(IntentType.DAILY_CHORES)

    if _contains_any(text, ("motivate me", "motivation", "i feel lazy", "encourage me")):
        return Intent(IntentType.MOTIVATION)

    reminder_text = _extract_after_phrase(
        text,
        ("remind me to ", "set reminder to ", "add reminder to ", "remember to ", "remind me 2 "),
    )
    if reminder_text:
        return Intent(IntentType.ADD_REMINDER, payload=reminder_text)

    if _contains_any(text, ("show reminders", "my reminders", "list reminders", "what are my reminders")):
        return Intent(IntentType.LIST_REMINDERS)

    reminder_index = _extract_index(
        text,
        (
            r"(?:delete|remove)\s+reminder\s+(\d+)",
            r"reminder\s+(\d+)\s+(?:delete|remove)",
        ),
    )
    if reminder_index:
        return Intent(IntentType.DELETE_REMINDER, payload=reminder_index)

    if _contains_any(text, ("clear reminders", "delete all reminders", "remove all reminders")):
        return Intent(IntentType.CLEAR_REMINDERS)

    task_text = _extract_after_phrase(
        text,
        ("add task ", "add todo ", "todo ", "to do "),
    )
    if task_text:
        return Intent(IntentType.ADD_TASK, payload=task_text)

    if _contains_any(text, ("show tasks", "my tasks", "list tasks", "todo list", "to do list")):
        return Intent(IntentType.LIST_TASKS)

    task_done_index = _extract_index(
        text,
        (
            r"(?:complete|finish|done)\s+task\s+(\d+)",
            r"mark\s+task\s+(\d+)\s+done",
        ),
    )
    if task_done_index:
        return Intent(IntentType.COMPLETE_TASK, payload=task_done_index)

    task_delete_index = _extract_index(
        text,
        (
            r"(?:delete|remove)\s+task\s+(\d+)",
            r"task\s+(\d+)\s+(?:delete|remove)",
        ),
    )
    if task_delete_index:
        return Intent(IntentType.DELETE_TASK, payload=task_delete_index)

    if _contains_any(text, ("clear tasks", "delete all tasks", "remove all tasks")):
        return Intent(IntentType.CLEAR_TASKS)

    add_contact_payload = _extract_contact_add(text)
    if add_contact_payload:
        return Intent(IntentType.ADD_CONTACT, payload=add_contact_payload)

    if _contains_any(text, ("show contacts", "list contacts", "my contacts")):
        return Intent(IntentType.LIST_CONTACTS)

    contact_sms_payload = _extract_contact_sms(text)
    if contact_sms_payload:
        return Intent(IntentType.SMS_CONTACT, payload=contact_sms_payload)

    whatsapp_payload = _extract_whatsapp(text)
    if whatsapp_payload:
        return Intent(IntentType.WHATSAPP_MESSAGE, payload=whatsapp_payload)

    event_payload = _extract_event(text)
    if event_payload:
        return Intent(IntentType.ADD_EVENT, payload=event_payload)

    if _contains_any(text, ("show schedule", "my schedule", "calendar events", "upcoming events")):
        return Intent(IntentType.SHOW_SCHEDULE)

    if _contains_any(text, ("sync tasks to calendar", "sync my tasks", "calendar sync")):
        return Intent(IntentType.SYNC_TASKS_CALENDAR)

    if _contains_any(text, ("undo", "undo last")):
        return Intent(IntentType.UNDO)

    if _contains_any(text, ("google login", "login google", "connect google")):
        return Intent(IntentType.GOOGLE_LOGIN)

    if _contains_any(text, ("sync google contacts", "google contacts sync", "import google contacts")):
        return Intent(IntentType.GOOGLE_SYNC_CONTACTS)

    if _contains_any(text, ("sync google calendar", "import google calendar", "pull google calendar")):
        return Intent(IntentType.GOOGLE_SYNC_CALENDAR)

    if _contains_any(text, ("push events to google", "sync events to google", "export calendar")):
        return Intent(IntentType.GOOGLE_PUSH_EVENTS)

    call_number = _extract_phone_number(text) if _contains_any(text, ("call", "dial", "ring")) else None
    if call_number:
        return Intent(IntentType.PHONE_CALL, payload=call_number)

    call_contact_name = _extract_after_phrase(text, ("call ", "dial "))
    if call_contact_name:
        cleaned_name = call_contact_name.split(" at ", 1)[0].split(" number ", 1)[0].strip()
        if cleaned_name and not any(ch.isdigit() for ch in cleaned_name):
            return Intent(IntentType.CALL_CONTACT, payload=cleaned_name)

    sms_payload = _extract_phone_sms(text)
    if sms_payload:
        return Intent(IntentType.PHONE_SMS, payload=sms_payload)

    if _contains_any(text, ("open app", "launch app", "start app")):
        app_name = _extract_open_app(text)
        if app_name:
            return Intent(IntentType.PHONE_OPEN_APP, payload=app_name)

    study_plan_topic = _extract_after_phrase(
        text,
        ("study plan for ", "make study plan for "),
    )
    if study_plan_topic:
        return Intent(IntentType.STUDY_PLAN, payload=study_plan_topic)

    explain_topic = _extract_after_phrase(
        text,
        ("explain ", "teach me ", "i want to learn "),
    )
    if explain_topic:
        return Intent(IntentType.STUDY_EXPLAIN, payload=explain_topic)

    quiz_topic = _extract_after_phrase(
        text,
        ("quiz me on ", "test me on "),
    )
    if quiz_topic:
        return Intent(IntentType.STUDY_QUIZ, payload=quiz_topic)

    translation_payload = _extract_translation(text)
    if translation_payload:
        return Intent(IntentType.TRANSLATE, payload=translation_payload)

    if _contains_any(text, ("supported languages", "translation languages", "translate languages")):
        return Intent(IntentType.SHOW_TRANSLATE_LANGS)

    if _contains_any(text, ("thank you", "thanks", "thank u")):
        return Intent(IntentType.THANKS)

    name_text = _extract_after_phrase(
        text,
        ("my name is ", "call me "),
    )
    if name_text:
        return Intent(IntentType.SET_NAME, payload=name_text)

    if _contains_any(text, ("what is my name", "do you know my name", "who am i")):
        return Intent(IntentType.GET_NAME)

    if _contains_any(text, ("check in with me", "check on me", "how am i doing")):
        return Intent(IntentType.CHECK_IN)

    if _contains_any(text, ("breathing exercise", "help me breathe", "calm me down")):
        return Intent(IntentType.BREATHING)

    if _contains_any(text, ("affirm me", "give me affirmation", "say something positive")):
        return Intent(IntentType.AFFIRMATION)

    if _contains_any(text, ("study tip", "help me study", "study advice")):
        return Intent(IntentType.STUDY_TIP)

    if _contains_any(text, ("fitness tip", "workout tip", "health tip")):
        return Intent(IntentType.FITNESS_TIP)

    if _contains_any(text, ("money tip", "finance tip", "save money")):
        return Intent(IntentType.MONEY_TIP)

    if _contains_any(text, ("sleep tip", "help me sleep", "better sleep")):
        return Intent(IntentType.SLEEP_TIP)

    expense_payload = _extract_expense(text)
    if expense_payload:
        return Intent(IntentType.ADD_EXPENSE, payload=expense_payload)

    if _contains_any(text, ("show expenses", "list expenses", "my expenses")):
        return Intent(IntentType.SHOW_EXPENSES)

    if _contains_any(text, ("expense report", "monthly expense report", "spending report")):
        return Intent(IntentType.EXPENSE_REPORT)

    habit_text = _extract_after_phrase(text, ("add habit ", "new habit "))
    if habit_text:
        return Intent(IntentType.ADD_HABIT, payload=habit_text)

    done_habit = _extract_after_phrase(text, ("done habit ", "mark habit done "))
    if done_habit:
        return Intent(IntentType.DONE_HABIT, payload=done_habit)

    if _contains_any(text, ("show habits", "list habits", "my habits")):
        return Intent(IntentType.SHOW_HABITS)

    if _contains_any(text, ("summarize my day", "day summary", "daily summary")):
        return Intent(IntentType.DAY_SUMMARY)

    if _contains_any(text, ("show history", "chat history", "conversation history")):
        return Intent(IntentType.SHOW_HISTORY)

    if _contains_any(text, ("clear history", "delete history", "erase history")):
        return Intent(IntentType.CLEAR_HISTORY)

    if _contains_any(
        text,
        (
            "what can you do",
            "help",
            "commands",
            "how can you help",
            "features",
        ),
    ):
        return Intent(IntentType.HELP)

    if "time" in text:
        return Intent(IntentType.GET_TIME)

    if "date" in text or "day" in text:
        return Intent(IntentType.GET_DATE)

    site = _extract_site_name(text)
    if site:
        return Intent(IntentType.OPEN_SITE, payload=site)

    search_query = _extract_after_phrase(
        text,
        ("search for ", "search ", "look up ", "find "),
    )
    if search_query:
        return Intent(IntentType.SEARCH_WEB, payload=search_query)

    calc_expr = _extract_after_phrase(
        text,
        ("calculate ", "compute ", "what is "),
    )
    if calc_expr and _looks_like_math_expression(calc_expr):
        return Intent(IntentType.CALCULATE, payload=calc_expr)

    note_text = _extract_after_phrase(
        text,
        ("note ", "write this down ", "save note ", "take a note "),
    )
    if note_text:
        return Intent(IntentType.SAVE_NOTE, payload=note_text)

    if "joke" in text:
        return Intent(IntentType.JOKE)

    return Intent(IntentType.UNKNOWN)
