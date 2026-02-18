from voice_assistant.skills.tasks import (
    add_task,
    clear_tasks,
    complete_task,
    delete_task,
    list_tasks_text,
)


def test_task_lifecycle() -> None:
    tasks: list[dict[str, object]] = []
    assert add_task(tasks, "finish resume") == "Task added: finish resume"
    assert "finish resume" in list_tasks_text(tasks)
    assert complete_task(tasks, 1) == "Task marked done: finish resume"
    assert delete_task(tasks, 1) == "Deleted task: finish resume"
    assert list_tasks_text(tasks) == "You do not have any tasks yet."


def test_clear_tasks_empty_and_non_empty() -> None:
    tasks: list[dict[str, object]] = []
    assert clear_tasks(tasks) == "You do not have any tasks to clear."
    add_task(tasks, "x")
    assert clear_tasks(tasks) == "All tasks cleared."
