from voice_assistant.skills.expenses import (
    add_expense,
    monthly_expense_report_text,
    show_expenses_text,
)


def test_add_and_show_expense() -> None:
    expenses: list[dict[str, object]] = []
    reply = add_expense(expenses, 120, "food")
    assert "Expense added" in reply
    assert "food" in show_expenses_text(expenses)


def test_monthly_report_text() -> None:
    expenses = [{"amount": 100.0, "category": "food", "date": "2099-01-10"}]
    report = monthly_expense_report_text(expenses)
    assert isinstance(report, str)
