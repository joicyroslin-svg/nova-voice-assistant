from __future__ import annotations

import subprocess
from urllib.parse import quote


APP_ALIASES = {
    "phone": "com.android.dialer",
    "dialer": "com.android.dialer",
    "contacts": "com.android.contacts",
    "messages": "com.google.android.apps.messaging",
    "whatsapp": "com.whatsapp",
    "youtube": "com.google.android.youtube",
    "chrome": "com.android.chrome",
    "maps": "com.google.android.apps.maps",
}


def _run_adb(adb_path: str, args: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            [adb_path, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except Exception as exc:
        return False, f"ADB command failed: {exc}"
    if completed.returncode != 0:
        return False, completed.stderr.strip() or "ADB returned non-zero status."
    return True, completed.stdout.strip()


def make_call(number: str, adb_enabled: bool, adb_path: str) -> str:
    if not adb_enabled:
        return f"I am ready to call {number}. Enable ADB phone control in .env to place calls."
    ok, msg = _run_adb(
        adb_path,
        ["shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{number}"],
    )
    return f"Calling {number}." if ok else f"Could not place call: {msg}"


def send_sms(number: str, message: str, adb_enabled: bool, adb_path: str) -> str:
    if not adb_enabled:
        return f"I prepared an SMS to {number}: {message}. Enable ADB phone control to send."
    ok, msg = _run_adb(
        adb_path,
        [
            "shell",
            "am",
            "start",
            "-a",
            "android.intent.action.SENDTO",
            "-d",
            f"sms:{number}",
            "--es",
            "sms_body",
            message,
        ],
    )
    return f"Opened SMS draft for {number}." if ok else f"Could not open SMS composer: {msg}"


def open_phone_app(app_name: str, adb_enabled: bool, adb_path: str) -> str:
    package = APP_ALIASES.get(app_name.lower().strip(), app_name.lower().strip())
    if not adb_enabled:
        return f"I am ready to open {app_name}. Enable ADB phone control in .env to launch apps."
    ok, msg = _run_adb(adb_path, ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"])
    return f"Opening {app_name}." if ok else f"Could not open app: {msg}"


def send_whatsapp_message(target_number: str, message: str, adb_enabled: bool, adb_path: str) -> str:
    number = "".join(ch for ch in target_number if ch.isdigit() or ch == "+")
    if not number:
        return "Could not send WhatsApp message. Target number is invalid."
    encoded = quote(message)
    wa_url = f"https://wa.me/{number}?text={encoded}"
    if not adb_enabled:
        return (
            f"I prepared WhatsApp message to {number}: {message}. "
            "Enable ADB phone control to open WhatsApp directly."
        )
    ok, msg = _run_adb(
        adb_path,
        ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", wa_url],
    )
    return f"Opening WhatsApp chat for {number}." if ok else f"Could not open WhatsApp: {msg}"
