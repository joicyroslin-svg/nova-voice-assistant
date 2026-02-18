from __future__ import annotations

import webbrowser
from urllib.parse import quote_plus


KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
}


def open_site(site_name: str) -> str:
    key = site_name.strip().lower()
    url = KNOWN_SITES.get(key)
    if not url:
        url = f"https://{key}.com"
    webbrowser.open(url)
    return f"Opening {key}."


def search_web(query: str) -> str:
    encoded = quote_plus(query.strip())
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return f"Searching the web for {query}."
