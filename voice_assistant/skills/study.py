from __future__ import annotations


def build_study_plan(topic: str) -> str:
    return (
        f"Study plan for {topic}: "
        "1. Learn core concepts for 30 minutes. "
        "2. Solve 5 practice questions. "
        "3. Review mistakes and make short notes. "
        "4. Revision after 24 hours and again after 7 days."
    )


def explain_topic(topic: str) -> str:
    return (
        f"{topic}: start with the basic definition, then understand one real example, "
        "then practice with a simple question, and finally explain it in your own words."
    )


def quiz_topic(topic: str) -> str:
    return (
        f"Quick quiz on {topic}: "
        "Q1. What is the main idea? "
        "Q2. Give one real-world example. "
        "Q3. What is a common mistake and how to avoid it?"
    )
