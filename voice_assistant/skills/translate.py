from __future__ import annotations

import json
from urllib import request


LANG_ALIASES = {
    "en": "english",
    "english": "english",
    "te": "telugu",
    "telugu": "telugu",
    "hi": "hindi",
    "hindi": "hindi",
    "es": "spanish",
    "spanish": "spanish",
    "ta": "tamil",
    "tamil": "tamil",
    "fr": "french",
    "french": "french",
}

LANG_TO_CODE = {
    "english": "en",
    "telugu": "te",
    "hindi": "hi",
    "spanish": "es",
    "tamil": "ta",
    "french": "fr",
}


PHRASE_TABLE = {
    "hello": {
        "english": "hello",
        "telugu": "నమస్తే",
        "hindi": "नमस्ते",
        "spanish": "hola",
        "tamil": "வணக்கம்",
        "french": "bonjour",
    },
    "how are you": {
        "english": "how are you",
        "telugu": "నువ్వు ఎలా ఉన్నావు",
        "hindi": "कैसे हो",
        "spanish": "como estas",
        "tamil": "நீங்கள் எப்படி இருக்கிறீர்கள்",
        "french": "comment ca va",
    },
    "thank you": {
        "english": "thank you",
        "telugu": "ధన్యవాదాలు",
        "hindi": "धन्यवाद",
        "spanish": "gracias",
        "tamil": "நன்றி",
        "french": "merci",
    },
    "good morning": {
        "english": "good morning",
        "telugu": "శుభోదయం",
        "hindi": "सुप्रभात",
        "spanish": "buenos dias",
        "tamil": "காலை வணக்கம்",
        "french": "bonjour",
    },
    "good night": {
        "english": "good night",
        "telugu": "శుభ రాత్రి",
        "hindi": "शुभ रात्रि",
        "spanish": "buenas noches",
        "tamil": "இனிய இரவு",
        "french": "bonne nuit",
    },
    "i need help": {
        "english": "i need help",
        "telugu": "నాకు సహాయం కావాలి",
        "hindi": "मुझे मदद चाहिए",
        "spanish": "necesito ayuda",
        "tamil": "எனக்கு உதவி வேண்டும்",
        "french": "jai besoin daide",
    },
}


def supported_languages_text() -> str:
    return "Supported translation languages: english, telugu, hindi, spanish, tamil, french."


def _translate_via_api(api_url: str, phrase: str, target_code: str) -> str | None:
    if not api_url.strip():
        return None
    body = json.dumps({"q": phrase, "source": "auto", "target": target_code}).encode("utf-8")
    req = request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=8.0) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
        translated = parsed.get("translatedText")
        if isinstance(translated, str) and translated.strip():
            return translated.strip()
    except Exception:
        return None
    return None


def translate_text(payload: str, api_url: str = "") -> str:
    if "|" not in payload:
        return "Use format like: translate hello to telugu."
    target_raw, phrase_raw = payload.split("|", 1)
    target = LANG_ALIASES.get(target_raw.strip().lower())
    if not target:
        return supported_languages_text()

    phrase = phrase_raw.strip().lower()
    values = PHRASE_TABLE.get(phrase)
    if not values:
        target_code = LANG_TO_CODE.get(target, "")
        translated = _translate_via_api(api_url, phrase_raw.strip(), target_code)
        if translated:
            return f"{phrase_raw.strip()} in {target} is: {translated}"
        examples = ", ".join(sorted(PHRASE_TABLE.keys()))
        return (
            f"I currently know common phrases offline. Try one of: {examples}. "
            "For broader translation, set TRANSLATION_API_URL in .env."
        )

    translated = values.get(target)
    if not translated:
        return supported_languages_text()
    return f"{phrase_raw.strip()} in {target} is: {translated}"
