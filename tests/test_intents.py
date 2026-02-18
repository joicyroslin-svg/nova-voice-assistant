from voice_assistant.intents import IntentType, parse_intent


def test_exit_intent() -> None:
    intent = parse_intent("exit now")
    assert intent.intent_type == IntentType.EXIT


def test_time_intent() -> None:
    intent = parse_intent("what time is it")
    assert intent.intent_type == IntentType.GET_TIME


def test_date_intent() -> None:
    intent = parse_intent("tell me the date")
    assert intent.intent_type == IntentType.GET_DATE


def test_open_site_intent() -> None:
    intent = parse_intent("open github")
    assert intent.intent_type == IntentType.OPEN_SITE
    assert intent.payload == "github"


def test_open_site_natural_phrase() -> None:
    intent = parse_intent("can you open youtube please")
    assert intent.intent_type == IntentType.OPEN_SITE
    assert intent.payload == "youtube"


def test_search_web_intent() -> None:
    intent = parse_intent("search python speech recognition")
    assert intent.intent_type == IntentType.SEARCH_WEB
    assert intent.payload == "python speech recognition"


def test_search_web_natural_phrase() -> None:
    intent = parse_intent("please search for python decorators")
    assert intent.intent_type == IntentType.SEARCH_WEB
    assert intent.payload == "python decorators"


def test_save_note_intent() -> None:
    intent = parse_intent("note prepare interview pitch")
    assert intent.intent_type == IntentType.SAVE_NOTE
    assert intent.payload == "prepare interview pitch"


def test_save_note_natural_phrase() -> None:
    intent = parse_intent("write this down finish portfolio website")
    assert intent.intent_type == IntentType.SAVE_NOTE
    assert intent.payload == "finish portfolio website"


def test_joke_intent() -> None:
    intent = parse_intent("tell me a joke")
    assert intent.intent_type == IntentType.JOKE


def test_how_are_you_intent() -> None:
    intent = parse_intent("how are you")
    assert intent.intent_type == IntentType.HOW_ARE_YOU


def test_how_are_you_slang_intent() -> None:
    intent = parse_intent("hru")
    assert intent.intent_type == IntentType.HOW_ARE_YOU


def test_daily_chores_intent() -> None:
    intent = parse_intent("show daily chores")
    assert intent.intent_type == IntentType.DAILY_CHORES


def test_greeting_sms_intent() -> None:
    intent = parse_intent("gud mrng")
    assert intent.intent_type == IntentType.GREETING


def test_add_reminder_intent() -> None:
    intent = parse_intent("remind me to submit resume")
    assert intent.intent_type == IntentType.ADD_REMINDER
    assert intent.payload == "submit resume"


def test_delete_reminder_intent() -> None:
    intent = parse_intent("delete reminder 2")
    assert intent.intent_type == IntentType.DELETE_REMINDER
    assert intent.payload == "2"


def test_clear_reminders_intent() -> None:
    intent = parse_intent("clear reminders")
    assert intent.intent_type == IntentType.CLEAR_REMINDERS


def test_list_reminders_intent() -> None:
    intent = parse_intent("show reminders")
    assert intent.intent_type == IntentType.LIST_REMINDERS


def test_add_task_intent() -> None:
    intent = parse_intent("add task finish portfolio")
    assert intent.intent_type == IntentType.ADD_TASK
    assert intent.payload == "finish portfolio"


def test_list_tasks_intent() -> None:
    intent = parse_intent("show tasks")
    assert intent.intent_type == IntentType.LIST_TASKS


def test_complete_task_intent() -> None:
    intent = parse_intent("mark task 1 done")
    assert intent.intent_type == IntentType.COMPLETE_TASK
    assert intent.payload == "1"


def test_delete_task_intent() -> None:
    intent = parse_intent("delete task 3")
    assert intent.intent_type == IntentType.DELETE_TASK
    assert intent.payload == "3"


def test_clear_tasks_intent() -> None:
    intent = parse_intent("clear tasks")
    assert intent.intent_type == IntentType.CLEAR_TASKS


def test_thanks_intent() -> None:
    intent = parse_intent("thanks")
    assert intent.intent_type == IntentType.THANKS


def test_thanks_sms_intent() -> None:
    intent = parse_intent("thx")
    assert intent.intent_type == IntentType.THANKS


def test_help_intent() -> None:
    intent = parse_intent("what can you do")
    assert intent.intent_type == IntentType.HELP


def test_set_name_intent() -> None:
    intent = parse_intent("my name is sunil")
    assert intent.intent_type == IntentType.SET_NAME
    assert intent.payload == "sunil"


def test_get_name_intent() -> None:
    intent = parse_intent("what is my name")
    assert intent.intent_type == IntentType.GET_NAME


def test_check_in_intent() -> None:
    intent = parse_intent("check in with me")
    assert intent.intent_type == IntentType.CHECK_IN


def test_breathing_intent() -> None:
    intent = parse_intent("help me breathe")
    assert intent.intent_type == IntentType.BREATHING


def test_affirmation_intent() -> None:
    intent = parse_intent("give me affirmation")
    assert intent.intent_type == IntentType.AFFIRMATION


def test_study_tip_intent() -> None:
    intent = parse_intent("study tip")
    assert intent.intent_type == IntentType.STUDY_TIP


def test_fitness_tip_intent() -> None:
    intent = parse_intent("fitness tip")
    assert intent.intent_type == IntentType.FITNESS_TIP


def test_money_tip_intent() -> None:
    intent = parse_intent("money tip")
    assert intent.intent_type == IntentType.MONEY_TIP


def test_sleep_tip_intent() -> None:
    intent = parse_intent("sleep tip")
    assert intent.intent_type == IntentType.SLEEP_TIP


def test_calculate_intent() -> None:
    intent = parse_intent("calculate 2 + 2")
    assert intent.intent_type == IntentType.CALCULATE
    assert intent.payload == "2 + 2"


def test_non_math_what_is_not_calculate() -> None:
    intent = parse_intent("what is this life brooo")
    assert intent.intent_type == IntentType.UNKNOWN


def test_open_site_sms_intent() -> None:
    intent = parse_intent("plz open github")
    assert intent.intent_type == IntentType.OPEN_SITE
    assert intent.payload == "github"


def test_unknown_intent() -> None:
    intent = parse_intent("sing a song")
    assert intent.intent_type == IntentType.UNKNOWN


def test_telugu_greeting_intent() -> None:
    intent = parse_intent("నమస్తే")
    assert intent.intent_type == IntentType.GREETING


def test_telugu_time_intent() -> None:
    intent = parse_intent("సమయం ఎంత")
    assert intent.intent_type == IntentType.GET_TIME


def test_telugu_romanized_how_are_you_intent() -> None:
    intent = parse_intent("ela unav")
    assert intent.intent_type == IntentType.HOW_ARE_YOU


def test_telugu_romanized_bagunnava_intent() -> None:
    intent = parse_intent("bagunnava")
    assert intent.intent_type == IntentType.HOW_ARE_YOU


def test_telugu_reminder_intent() -> None:
    intent = parse_intent("నాకు గుర్తు చేయి నీళ్లు తాగు")
    assert intent.intent_type == IntentType.ADD_REMINDER
    assert intent.payload == "నీళ్లు తాగు"


def test_hindi_thanks_intent() -> None:
    intent = parse_intent("धन्यवाद")
    assert intent.intent_type == IntentType.THANKS


def test_hindi_open_intent() -> None:
    intent = parse_intent("खोलो github")
    assert intent.intent_type == IntentType.OPEN_SITE
    assert intent.payload == "github"


def test_hindi_romanized_open_intent() -> None:
    intent = parse_intent("kholo github")
    assert intent.intent_type == IntentType.OPEN_SITE
    assert intent.payload == "github"


def test_spanish_greeting_intent() -> None:
    intent = parse_intent("hola")
    assert intent.intent_type == IntentType.GREETING


def test_spanish_reminder_intent() -> None:
    intent = parse_intent("recuerdame beber agua")
    assert intent.intent_type == IntentType.ADD_REMINDER
    assert intent.payload == "beber agua"


def test_add_expense_intent() -> None:
    intent = parse_intent("spent 250 on groceries")
    assert intent.intent_type == IntentType.ADD_EXPENSE
    assert intent.payload == "250|groceries"


def test_show_expenses_intent() -> None:
    intent = parse_intent("show expenses")
    assert intent.intent_type == IntentType.SHOW_EXPENSES


def test_expense_report_intent() -> None:
    intent = parse_intent("monthly expense report")
    assert intent.intent_type == IntentType.EXPENSE_REPORT


def test_add_habit_intent() -> None:
    intent = parse_intent("add habit reading")
    assert intent.intent_type == IntentType.ADD_HABIT
    assert intent.payload == "reading"


def test_done_habit_intent() -> None:
    intent = parse_intent("done habit reading")
    assert intent.intent_type == IntentType.DONE_HABIT
    assert intent.payload == "reading"


def test_show_habits_intent() -> None:
    intent = parse_intent("show habits")
    assert intent.intent_type == IntentType.SHOW_HABITS


def test_day_summary_intent() -> None:
    intent = parse_intent("summarize my day")
    assert intent.intent_type == IntentType.DAY_SUMMARY


def test_show_history_intent() -> None:
    intent = parse_intent("show history")
    assert intent.intent_type == IntentType.SHOW_HISTORY


def test_clear_history_intent() -> None:
    intent = parse_intent("clear history")
    assert intent.intent_type == IntentType.CLEAR_HISTORY


def test_phone_call_intent() -> None:
    intent = parse_intent("nova please call +91 9876543210")
    assert intent.intent_type == IntentType.PHONE_CALL
    assert intent.payload == "+919876543210"


def test_phone_sms_intent() -> None:
    intent = parse_intent("send to 9876543210 message I will be late")
    assert intent.intent_type == IntentType.PHONE_SMS
    assert intent.payload == "9876543210|i will be late"


def test_phone_open_app_intent() -> None:
    intent = parse_intent("open app whatsapp")
    assert intent.intent_type == IntentType.PHONE_OPEN_APP
    assert intent.payload == "whatsapp"


def test_add_contact_intent() -> None:
    intent = parse_intent("add contact mom 9876543210")
    assert intent.intent_type == IntentType.ADD_CONTACT
    assert intent.payload == "mom|9876543210"


def test_call_contact_intent() -> None:
    intent = parse_intent("call mom")
    assert intent.intent_type == IntentType.CALL_CONTACT
    assert intent.payload == "mom"


def test_sms_contact_intent() -> None:
    intent = parse_intent("sms mom message reach home")
    assert intent.intent_type == IntentType.SMS_CONTACT
    assert intent.payload == "mom|reach home"


def test_whatsapp_intent() -> None:
    intent = parse_intent("whatsapp mom message hello")
    assert intent.intent_type == IntentType.WHATSAPP_MESSAGE
    assert intent.payload == "mom|hello"


def test_add_event_intent() -> None:
    intent = parse_intent("add event exam revision at 2026-02-20 18:00")
    assert intent.intent_type == IntentType.ADD_EVENT
    assert intent.payload == "exam revision|2026-02-20 18:00"


def test_show_schedule_intent() -> None:
    intent = parse_intent("show schedule")
    assert intent.intent_type == IntentType.SHOW_SCHEDULE


def test_sync_tasks_calendar_intent() -> None:
    intent = parse_intent("sync tasks to calendar")
    assert intent.intent_type == IntentType.SYNC_TASKS_CALENDAR


def test_study_plan_intent() -> None:
    intent = parse_intent("make study plan for data structures")
    assert intent.intent_type == IntentType.STUDY_PLAN
    assert intent.payload == "data structures"


def test_study_explain_intent() -> None:
    intent = parse_intent("explain binary search")
    assert intent.intent_type == IntentType.STUDY_EXPLAIN
    assert intent.payload == "binary search"


def test_study_quiz_intent() -> None:
    intent = parse_intent("quiz me on operating systems")
    assert intent.intent_type == IntentType.STUDY_QUIZ
    assert intent.payload == "operating systems"


def test_translate_intent() -> None:
    intent = parse_intent("translate hello to telugu")
    assert intent.intent_type == IntentType.TRANSLATE
    assert intent.payload == "telugu|hello"


def test_translate_intent_in_form() -> None:
    intent = parse_intent("what is thank you in hindi")
    assert intent.intent_type == IntentType.TRANSLATE
    assert intent.payload == "hindi|thank you"


def test_translate_languages_intent() -> None:
    intent = parse_intent("supported languages")
    assert intent.intent_type == IntentType.SHOW_TRANSLATE_LANGS


def test_google_login_intent() -> None:
    intent = parse_intent("google login")
    assert intent.intent_type == IntentType.GOOGLE_LOGIN


def test_google_sync_contacts_intent() -> None:
    intent = parse_intent("sync google contacts")
    assert intent.intent_type == IntentType.GOOGLE_SYNC_CONTACTS


def test_google_sync_calendar_intent() -> None:
    intent = parse_intent("sync google calendar")
    assert intent.intent_type == IntentType.GOOGLE_SYNC_CALENDAR


def test_google_push_events_intent() -> None:
    intent = parse_intent("push events to google")
    assert intent.intent_type == IntentType.GOOGLE_PUSH_EVENTS


def test_undo_intent() -> None:
    intent = parse_intent("undo")
    assert intent.intent_type == IntentType.UNDO
