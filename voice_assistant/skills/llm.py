from __future__ import annotations

import json
from urllib import request

from voice_assistant.skills.history import read_history


def generate_llm_reply(
    user_text: str,
    history_file: str,
    api_key: str,
    model: str,
    base_url: str,
    timeout_seconds: float = 8.0,
) -> str | None:
    if not api_key.strip():
        return None

    history = read_history(history_file, limit=8)
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a friendly personal assistant. Understand slang, short forms, and mixed-language text. "
                "Reply naturally, briefly, and helpfully."
            ),
        }
    ]
    for item in history:
        if item["role"] in ("user", "assistant"):
            messages.append({"role": item["role"], "content": item["text"]})
    messages.append({"role": "user", "content": user_text})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        base_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as resp:
            body = resp.read().decode("utf-8")
        parsed = json.loads(body)
        return parsed["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
