from __future__ import annotations

import re

POSITIVE_WORDS = {
    "good",
    "great",
    "awesome",
    "nice",
    "love",
    "happy",
    "excited",
    "amazing",
    "cool",
    "thanks",
    "thank",
    "grateful",
    "enjoy",
    "fun",
    "cheerful",
    "win",
    "progress",
}

NEGATIVE_WORDS = {
    "sad",
    "angry",
    "upset",
    "tired",
    "anxious",
    "stress",
    "stressed",
    "depressed",
    "bad",
    "bored",
    "lonely",
    "hate",
    "annoyed",
    "frustrated",
    "overwhelmed",
    "fail",
    "give up",
}


def detect_sentiment(text: str) -> str:
    """
    Lightweight sentiment detection for personalization.
    Returns: "positive", "negative", or "neutral".
    """
    lowered = text.lower()
    tokens = re.findall(r"[a-z']+", lowered)
    pos_hits = sum(1 for tok in tokens if tok in POSITIVE_WORDS)
    neg_hits = sum(1 for tok in tokens if tok in NEGATIVE_WORDS)

    if pos_hits - neg_hits >= 2:
        return "positive"
    if neg_hits - pos_hits >= 2:
        return "negative"
    if pos_hits > neg_hits:
        return "positive"
    if neg_hits > pos_hits:
        return "negative"
    return "neutral"
