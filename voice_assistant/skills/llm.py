from __future__ import annotations

import json
import time
from urllib import error, request

from voice_assistant.skills.history import read_history


def generate_llm_reply(
    user_text: str,
    history_file: str,
    api_key: str,
    model: str,
    base_url: str,
    timeout_seconds: float = 8.0,
    max_retries: int = 3,
    backoff_seconds: float = 1.5,
    memory_context: list[dict[str, str]] | None = None,
    user_name: str | None = None,
    sentiment: str | None = None,
    logger=None,
) -> str | None:
    if not api_key.strip():
        return None

    history = memory_context if memory_context is not None else read_history(history_file, limit=8)
    system_prompt = (
        "You are a friendly personal assistant. Understand slang, short forms, code-switching, and SMS-style text. "
        "Reply naturally, concisely, and helpfully. Use recent context to stay coherent."
    )
    if user_name:
        system_prompt += f" The user's name is {user_name}. Use it where it feels natural."
    if sentiment:
        system_prompt += (
            f" Current mood signal: {sentiment}. If negative, be calm and supportive; "
            "if positive, encourage momentum; stay neutral otherwise."
        )

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
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
    attempt = 0
    last_status: int | None = None
    while attempt < max_retries:
        try:
            with request.urlopen(req, timeout=timeout_seconds) as resp:
                body = resp.read().decode("utf-8")
            parsed = json.loads(body)
            reply = parsed["choices"][0]["message"]["content"].strip()
            if logger:
                logger.info("LLM reply received (attempt %s): %.120s", attempt + 1, reply)
            return reply
        except error.HTTPError as exc:
            last_status = exc.code
            if exc.code == 429:
                if logger:
                    logger.warning("LLM rate limited (attempt %s/%s)", attempt + 1, max_retries)
                time.sleep(backoff_seconds * (attempt + 1))
                attempt += 1
                continue
            if logger:
                logger.exception("LLM HTTP error")
            return None
        except Exception as exc:  # pragma: no cover - network dependent
            if logger:
                logger.exception("LLM call failed")
            time.sleep(backoff_seconds * (attempt + 1))
            attempt += 1
            continue
    if last_status == 429:
        return "I am hitting the model rate limit right now. Give me a moment and try again?"
    return None
