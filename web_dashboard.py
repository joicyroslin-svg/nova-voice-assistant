from __future__ import annotations

import os
import secrets
from datetime import timedelta
from functools import wraps
from flask import Flask, redirect, render_template_string, request, session, url_for, flash

from voice_assistant.config import Settings
from voice_assistant.skills.contacts import add_contact, list_contacts_text, resolve_contact_number
from voice_assistant.skills.phone import make_call, send_sms, send_whatsapp_message
from voice_assistant.skills.tasks import complete_task, delete_task, list_tasks_text, add_task
from voice_assistant.skills.reminders import load_reminders
from voice_assistant.skills.calendar_tools import add_event, show_schedule_text
from voice_assistant.skills.tasks import load_tasks
from voice_assistant.skills.event_store import load_events
from voice_assistant.storage.sqlite_store import MigrationSources, SQLiteStore


settings = Settings()

app = Flask(__name__)
app.secret_key = os.getenv("DASHBOARD_SECRET", "change-me")
app.permanent_session_lifetime = timedelta(hours=8)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


store = SQLiteStore(
    settings.sqlite_db_file,
    sources=MigrationSources(
        reminders_file=settings.reminders_file,
        tasks_file=settings.tasks_file,
        profile_file=settings.profile_file,
        expenses_file=settings.expenses_file,
        habits_file=settings.habits_file,
        history_file=settings.history_file,
        contacts_file=settings.contacts_file,
        events_file=settings.events_file,
    ),
)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("auth"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/", methods=["GET"])
def root() -> str:
    if not session.get("auth"):
        return redirect(url_for("login"))
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    contacts = store.load_contacts()
    contacts_text = list_contacts_text(contacts)
    tasks = load_tasks(settings.tasks_file) if not store else store.load_tasks()
    reminders = load_reminders(settings.reminders_file) if not store else store.load_reminders()
    events = load_events(settings.events_file) if not store else store.load_events()
    tasks_text = list_tasks_text(tasks)
    events_text = show_schedule_text(events)
    return render_template_string(
        """
        <h2>Nova Assistant Dashboard</h2>
        <p>{{ contacts_text }}</p>
        <h3>Add Contact</h3>
        <form method="post" action="{{ url_for('add_contact_route') }}">
            Name: <input name="name">
            Number: <input name="number">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Save</button>
        </form>
        <h3>Call/SMS/WhatsApp</h3>
        <form method="post" action="{{ url_for('call_route') }}">
            Contact or Number: <input name="target">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Call</button>
        </form>
        <form method="post" action="{{ url_for('sms_route') }}">
            Contact or Number: <input name="target">
            Message: <input name="message">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">SMS</button>
        </form>
        <form method="post" action="{{ url_for('wa_route') }}">
            Contact or Number: <input name="target">
            Message: <input name="message">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">WhatsApp</button>
        </form>
        <h3>Tasks</h3>
        <p>{{ tasks_text }}</p>
        <form method="post" action="{{ url_for('add_task_route') }}">
            Task: <input name="task">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Add Task</button>
        </form>
        <form method="post" action="{{ url_for('complete_task_route') }}">
            Index: <input name="index">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Mark Done</button>
        </form>
        <form method="post" action="{{ url_for('delete_task_route') }}">
            Index: <input name="index">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Delete Task</button>
        </form>
        <h3>Reminders</h3>
        <p>{{ reminders }}</p>
        <form method="post" action="{{ url_for('add_reminder_route') }}">
            Reminder: <input name="text">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Add Reminder</button>
        </form>
        <form method="post" action="{{ url_for('delete_reminder_route') }}">
            Index: <input name="index">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Delete Reminder</button>
        </form>
        <form method="post" action="{{ url_for('clear_reminders_route') }}">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Clear Reminders</button>
        </form>
        <h3>Schedule</h3>
        <p>{{ events_text }}</p>
        <form method="post" action="{{ url_for('add_event_route') }}">
            Title: <input name="title">
            When (YYYY-MM-DD HH:MM): <input name="when">
            <input type="hidden" name="csrf" value="{{ csrf }}">
            <button type="submit">Add Event</button>
        </form>
        <p><a href="{{ url_for('logout') }}">Logout</a></p>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for msg in messages %}
              <li>{{ msg }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        """,
        contacts_text=contacts_text,
        tasks_text=tasks_text,
        reminders=", ".join(reminders),
        events_text=events_text,
        csrf=session.get("csrf", ""),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == os.getenv("DASHBOARD_PASSWORD", "letmein"):
            session["auth"] = True
            session["csrf"] = secrets.token_hex(16)
            return redirect(url_for("root"))
        flash("Invalid password")
    return render_template_string(
        """
        <h2>Login</h2>
        <form method="post">
            Password: <input name="password" type="password">
            <button type="submit">Login</button>
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for msg in messages %}
              <li>{{ msg }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        """
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/add-contact", methods=["POST"])
@login_required
def add_contact_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    name = request.form.get("name", "")
    number = request.form.get("number", "")
    contacts = store.load_contacts()
    msg = add_contact(contacts, name, number)
    store.save_contacts(contacts)
    flash(msg)
    return redirect(url_for("root"))


def _resolve_target(target: str) -> str:
    contacts = store.load_contacts()
    return resolve_contact_number(contacts, target) or target


@app.route("/call", methods=["POST"])
@login_required
def call_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    target = request.form.get("target", "")
    number = _resolve_target(target)
    flash(
        make_call(
            number,
            adb_enabled=settings.phone_adb_enabled,
            adb_path=settings.phone_adb_path,
        )
    )
    return redirect(url_for("root"))


@app.route("/sms", methods=["POST"])
@login_required
def sms_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    target = request.form.get("target", "")
    message = request.form.get("message", "")
    number = _resolve_target(target)
    flash(
        send_sms(
            number,
            message,
            adb_enabled=settings.phone_adb_enabled,
            adb_path=settings.phone_adb_path,
        )
    )
    return redirect(url_for("root"))


@app.route("/wa", methods=["POST"])
@login_required
def wa_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    target = request.form.get("target", "")
    message = request.form.get("message", "")
    number = _resolve_target(target)
    flash(
        send_whatsapp_message(
            number,
            message,
            adb_enabled=settings.phone_adb_enabled,
            adb_path=settings.phone_adb_path,
        )
    )
    return redirect(url_for("root"))


@app.route("/add-task", methods=["POST"])
@login_required
def add_task_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    task = request.form.get("task", "")
    tasks = store.load_tasks()
    msg = add_task(tasks, task)
    store.save_tasks(tasks)
    flash(msg)
    return redirect(url_for("root"))


@app.route("/complete-task", methods=["POST"])
@login_required
def complete_task_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    index = request.form.get("index", "")
    tasks = store.load_tasks()
    try:
        idx = int(index)
        msg = complete_task(tasks, idx)
        store.save_tasks(tasks)
        flash(msg)
    except Exception as exc:
        flash(f"Could not complete task: {exc}")
    return redirect(url_for("root"))


@app.route("/delete-task", methods=["POST"])
@login_required
def delete_task_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    index = request.form.get("index", "")
    tasks = store.load_tasks()
    try:
        idx = int(index)
        msg = delete_task(tasks, idx)
        store.save_tasks(tasks)
        flash(msg)
    except Exception as exc:
        flash(f"Could not delete task: {exc}")
    return redirect(url_for("root"))


@app.route("/add-reminder", methods=["POST"])
@login_required
def add_reminder_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    text = request.form.get("text", "")
    reminders = store.load_reminders()
    reminders.append(text)
    store.save_reminders(reminders)
    flash("Reminder added.")
    return redirect(url_for("root"))


@app.route("/delete-reminder", methods=["POST"])
@login_required
def delete_reminder_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    index = request.form.get("index", "")
    reminders = store.load_reminders()
    try:
        idx = int(index)
        if 1 <= idx <= len(reminders):
            reminders.pop(idx - 1)
            store.save_reminders(reminders)
            flash("Reminder deleted.")
        else:
            flash("Index out of range.")
    except Exception as exc:
        flash(f"Could not delete reminder: {exc}")
    return redirect(url_for("root"))


@app.route("/clear-reminders", methods=["POST"])
@login_required
def clear_reminders_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    store.save_reminders([])
    flash("Reminders cleared.")
    return redirect(url_for("root"))


@app.route("/add-event", methods=["POST"])
@login_required
def add_event_route():
    if request.form.get("csrf") != session.get("csrf"):
        flash("CSRF token mismatch.")
        return redirect(url_for("root"))
    title = request.form.get("title", "")
    when = request.form.get("when", "")
    events = store.load_events()
    msg = add_event(events, title, when)
    store.save_events(events)
    flash(msg)
    return redirect(url_for("root"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
