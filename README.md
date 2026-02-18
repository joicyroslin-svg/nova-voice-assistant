# Voice Assistant AI (Portfolio Project) ![CI](https://github.com/joicyroslin-svg/nova-voice-assisstant-ai/actions/workflows/ci.yml/badge.svg) [![codecov](https://codecov.io/gh/joicyroslin-svg/nova-voice-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/joicyroslin-svg/nova-voice-assistant)

A production-style Python voice assistant project you can showcase in your portfolio and discuss in interviews.

## Features

- Voice input via microphone (`speech_recognition`)
- Text-to-speech output (`pyttsx3`)
- Intent parsing and command routing
- Human-style conversation and emotional support replies
- Multilingual phrase understanding (English + Telugu + Hindi + Spanish basics)
- Personalized memory (remembers your name)
- Short-term conversation memory for contextual replies
- Save notes
- Persistent reminders (saved to JSON)
- Task manager with status tracking
- LLM fallback with rate-limit handling and logged AI responses
- Sentiment-aware, personalized replies
- Safe calculator for quick math
- Built-in translator (common phrases)
- SQLite-backed persistent state (auto-migration from JSON on first run)
- Structured logging with rotating log files
- Android phone control via ADB (call, SMS draft, app launch)
- Study assistant mode (study plan, explain topic, quiz prompts)
- Contact book commands (`add contact`, `call mom`, `sms mom`)
- WhatsApp direct message support
- Calendar and task sync commands
- Optional Google sync (login, import contacts, import/push calendar)
- Data/logs default to `.data/` (auto-created)
- Data/logs default to `.data/` (auto-created)
- Built-in actions:
  - Time and date
  - Open websites
  - Web search
  - Tell a joke
- Keyboard fallback mode when microphone is unavailable
- Clean modular architecture with tests

## Project Structure

```text
voice-assistant-ai/
  app.py
  requirements.txt
  .env.example
  voice_assistant/
    __init__.py
    assistant.py
    audio.py
    config.py
    intents.py
    skills/
      __init__.py
      math_tools.py
      reminders.py
      notes.py
      system.py
      tasks.py
      web.py
  tests/
    test_intents.py
    test_math_tools.py
    test_reminder_actions.py
    test_reminders.py
    test_tasks.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy env template:

```bash
copy .env.example .env
```

4. Run:

```bash
python app.py
```

## LLM & Memory Options

- `LLM_ENABLED=true` to allow LLM fallback for unknown intents.
- `LLM_API_KEY`, `LLM_MODEL`, `LLM_TIMEOUT_SECONDS`, `LLM_MAX_RETRIES`, `LLM_BACKOFF_SECONDS` tune the model call and rate-limit backoff.
- `MEMORY_MESSAGE_LIMIT` controls the short-term context window used in LLM prompts.
- `AI_LOG_FILE` stores JSONL logs of every AI-generated reply (LLM + conversational fallback).

## Optional Phone Control (Android)

Set in `.env`:

```bash
PHONE_ADB_ENABLED=true
PHONE_ADB_PATH=adb
```

Requirements:
- Android phone with USB debugging enabled
- `adb` available in PATH

## Optional Google Sync

Place your OAuth client JSON at `GOOGLE_CREDENTIALS_FILE` (default `google_credentials.json`).

Set in `.env`:

```bash
GOOGLE_SYNC_ENABLED=true
GOOGLE_TOKEN_FILE=google_token.json
GOOGLE_CALENDAR_ID=primary
```

Commands:
- `google login`
- `sync google contacts`
- `sync google calendar`
- `push events to google`

## Optional Microphone Notes (Windows)

- If `PyAudio` install fails directly, try:

```bash
pip install pipwin
pipwin install pyaudio
```

Optional wake-word/VAD deps:

```bash
py -m pip install -r requirements-voice.txt
```

Add to Windows Startup (auto-launch assistant):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/add_to_startup.ps1
```

## Commands You Can Say

- "what time is it"
- "what is today's date"
- "open youtube"
- "search python dependency injection"
- "note buy milk and eggs"
- "tell me a joke"
- "how are you"
- "show daily chores"
- "motivate me"
- "remind me to apply for 3 jobs"
- "show reminders"
- "delete reminder 1"
- "clear reminders"
- "add task finish portfolio website"
- "show tasks"
- "mark task 1 done"
- "delete task 1"
- "clear tasks"
- "calculate 120 / 5 + 7"
- "my name is Sunil"
- "what is my name"
- "check in with me"
- "help me breathe"
- "give me affirmation"
- "study tip"
- "fitness tip"
- "money tip"
- "sleep tip"
- "నమస్తే"
- "సమయం ఎంత"
- "नमस्ते"
- "समय क्या है"
- "hola"
- "recuerdame beber agua"
- "translate hello to telugu"
- "what is thank you in hindi"
- "supported languages"
- "nova please call +91 9876543210"
- "send to 9876543210 message i will be late"
- "open app whatsapp"
- "add contact mom 9876543210"
- "call mom"
- "sms mom message i will be late"
- "whatsapp mom message reached safely"
- "add event exam revision at 2026-02-20 18:00"
- "show schedule"
- "sync tasks to calendar"
- "google login"
- "sync google contacts"
- "sync google calendar"
- "push events to google"
- "make study plan for data structures"
- "explain binary search"
- "quiz me on operating systems"
- "what can you do"
- "can you open youtube please"
- "please search for python decorators"
- "write this down finish my assignment"
- "i am stressed"
- "will you marry me"
- "exit"

## Test

```bash
pytest -q
```

Coverage locally:

```bash
pytest -q --cov=voice_assistant --cov-report=term-missing --cov-fail-under=40
```

## Interview Talking Points

- Layered architecture (`audio`, `assistant`, `intents`, `skills`)
- Reliability fallback from voice to typed input
- Extensible command pattern for new skills
- Simple testing strategy focused on intent parsing
