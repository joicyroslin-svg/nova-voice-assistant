from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path


def load_expenses(path: str) -> list[dict[str, object]]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    expenses: list[dict[str, object]] = []
    for item in data:
        if (
            isinstance(item, dict)
            and isinstance(item.get("amount"), (int, float))
            and isinstance(item.get("category"), str)
            and isinstance(item.get("date"), str)
        ):
            expenses.append(item)
    return expenses


def save_expenses(path: str, expenses: list[dict[str, object]]) -> None:
    Path(path).write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def add_expense(expenses: list[dict[str, object]], amount: float, category: str) -> str:
    entry = {
        "amount": round(float(amount), 2),
        "category": category.strip(),
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    expenses.append(entry)
    return f"Expense added: {entry['amount']:.2f} for {entry['category']}."


def show_expenses_text(expenses: list[dict[str, object]]) -> str:
    if not expenses:
        return "You do not have any expenses yet."
    last_five = expenses[-5:]
    lines = [
        f"{idx + 1}. {item['date']} - {item['amount']:.2f} on {item['category']}"
        for idx, item in enumerate(last_five)
    ]
    return "Recent expenses: " + "; ".join(lines)


def monthly_expense_report_text(expenses: list[dict[str, object]]) -> str:
    current_month = datetime.now().strftime("%Y-%m")
    monthly = [e for e in expenses if str(e.get("date", "")).startswith(current_month)]
    if not monthly:
        return "No expenses found for this month."
    total = sum(float(e["amount"]) for e in monthly)
    by_category: dict[str, float] = {}
    for item in monthly:
        cat = str(item["category"])
        by_category[cat] = by_category.get(cat, 0.0) + float(item["amount"])
    top = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:3]
    top_text = ", ".join(f"{cat}: {amt:.2f}" for cat, amt in top)
    return f"This month you spent {total:.2f}. Top categories: {top_text}."
