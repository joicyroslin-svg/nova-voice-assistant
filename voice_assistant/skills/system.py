from datetime import datetime
import random
import re


def get_time_text() -> str:
    return datetime.now().strftime("The time is %I:%M %p")


def get_date_text() -> str:
    return datetime.now().strftime("Today's date is %A, %d %B %Y")


def get_joke_text() -> str:
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I told my code to behave. It responded with a syntax error.",
        "Why was the function calm? It had no side effects.",
    ]
    return random.choice(jokes)


def get_greeting_text() -> str:
    responses = [
        "Hello. I am ready to help you.",
        "Hi. What would you like to do first?",
        "Hey. I am here and listening.",
    ]
    return random.choice(responses)


def get_how_are_you_text() -> str:
    responses = [
        "I am doing well and focused. Thanks for asking.",
        "I feel ready and productive. How are you feeling today?",
        "I am stable and energized to help with your tasks.",
    ]
    return random.choice(responses)


def get_daily_chores_text() -> str:
    chores = [
        "1. Make your bed and clean your workspace.",
        "2. Drink water and do a 10 minute stretch.",
        "3. Finish one high priority work task.",
        "4. Do a quick room cleanup.",
        "5. Review tomorrow's plan before sleep.",
    ]
    return "Here is a simple daily chore plan. " + " ".join(chores)


def get_motivation_text() -> str:
    messages = [
        "Small consistent steps beat perfect plans. Start with the next 15 minutes.",
        "Progress today is more important than intensity tomorrow.",
        "You are building proof through action. One completed task at a time.",
    ]
    return random.choice(messages)


def get_thanks_reply_text() -> str:
    return "You are welcome. I am always here to help."


def get_help_text() -> str:
    return (
        "You can talk naturally. I can tell time or date, open websites, search the web, "
        "save notes, add or manage reminders, manage tasks, do quick calculations, remember your name, "
        "share motivation, and support study, fitness, money, sleep, and emotional check-ins."
    )


def get_friend_reply_text(user_text: str) -> str:
    text = user_text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    slang_map = {
        "hru": "how are you",
        "idk": "i do not know",
        "wru": "where are you",
        "wyd": "what are you doing",
        "plz": "please",
        "pls": "please",
        "thx": "thanks",
        "ty": "thank you",
        "im": "i am",
        "gm": "good morning",
        "gn": "good night",
    }
    for src, dst in slang_map.items():
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)

    if text in ("nothing", "nothing much", "not much", "idk", "i don't know", "i do not know", "dont know"):
        return "No worries. We can keep it simple. Want a quick check-in, a motivation line, or just a joke?"

    if any(k in text for k in ("i am sad", "i feel sad", "depressed", "low")):
        return "I am sorry you are feeling this way. Want to talk for a minute and pick one small step together?"

    if any(k in text for k in ("i feel lonely", "alone", "no one understands me")):
        return "You are not alone right now. I am here with you, and we can take one steady step together."

    if any(k in text for k in ("i am stressed", "anxious", "overwhelmed")):
        return "That sounds heavy. Let us slow down and pick only one priority for the next 20 minutes."

    if any(k in text for k in ("i am tired", "exhausted", "burned out")):
        return "You have been carrying a lot. A short break, water, and one easy win can reset your energy."

    if any(k in text for k in ("will you marry me", "i love you")):
        return "I care about you as your AI friend. I am here to support your goals and daily life."

    if any(k in text for k in ("who are you", "what are you")):
        return "I am your voice assistant friend. You can chat naturally and I will help with tasks and reminders."

    if any(k in text for k in ("good night", "goodnight")):
        return "Good night. Rest well and we can plan a strong tomorrow."

    if any(k in text for k in ("good job", "well done", "you are great")):
        return "Thank you. You are doing strong work too."

    if any(k in text for k in ("i am bored", "bored")):
        return "Let us do something quick: short walk, music break, or finish one tiny task. Which one do you want?"

    if any(k in text for k in ("i want to give up", "i can't do this")):
        return "You are carrying a lot. Pause, breathe, and focus only on the smallest next step. I can help you pick it."

    return "I am here. Tell me what is going on, and we will figure it out together."


def get_check_in_text(name: str | None = None) -> str:
    who = name if name else "friend"
    return (
        f"Checking in, {who}. How is your energy from 1 to 10? "
        "If it is low, let us pick one tiny win and one short break."
    )


def get_breathing_text() -> str:
    return (
        "Let us do a quick breathing reset. Inhale for 4 seconds, hold for 4, exhale for 6. "
        "Repeat this 5 times."
    )


def get_affirmation_text() -> str:
    messages = [
        "You do not need perfect progress. Consistent effort is enough.",
        "You are improving every time you show up for yourself.",
        "Your current step matters. Keep moving with calm focus.",
    ]
    return random.choice(messages)


def get_study_tip_text() -> str:
    return (
        "Use a 25-5 focus cycle. Pick one topic, set a timer for 25 minutes, "
        "then take a 5 minute break and repeat."
    )


def get_fitness_tip_text() -> str:
    return (
        "Start simple: 20 minute walk, 10 pushups, and light stretching daily. "
        "Consistency is better than intensity."
    )


def get_money_tip_text() -> str:
    return (
        "Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings or debt payment. "
        "Track spending weekly."
    )


def get_sleep_tip_text() -> str:
    return (
        "Keep a fixed sleep time, avoid screens 30 minutes before bed, and reduce caffeine in late afternoon."
    )
