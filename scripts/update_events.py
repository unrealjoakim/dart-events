import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

EVENTS_FILE = os.path.join(os.path.dirname(__file__), "..", "Dart-event.json")
DART_SE_URL = "https://dart.se/tavlingar/"


def fetch_events_from_dart_se():
    events = []
    try:
        response = requests.get(DART_SE_URL, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Warning: Could not fetch events from {DART_SE_URL}: {e}")
        return events

    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select("article, .event, .tavling, .tournament"):
        name_tag = item.find(["h1", "h2", "h3", "h4"])
        name = name_tag.get_text(strip=True) if name_tag else ""
        if not name:
            continue

        date_tag = item.find(class_=lambda c: c and "date" in c.lower()) or item.find("time")
        date_str = ""
        if date_tag:
            date_str = date_tag.get("datetime", "") or date_tag.get_text(strip=True)

        link_tag = item.find("a", href=True)
        link = link_tag["href"] if link_tag else DART_SE_URL
        if link and not link.startswith("http"):
            link = "https://dart.se" + link

        city_tag = item.find(class_=lambda c: c and "city" in c.lower())
        city = city_tag.get_text(strip=True) if city_tag else "Sverige"

        desc_tag = item.find("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        events.append({
            "namn": name,
            "datum": date_str,
            "tid": "",
            "plats": city,
            "stad": city,
            "land": "Sverige",
            "kategori": "Nationell",
            "arrangör": "Svenska Dartförbundet",
            "beskrivning": description,
            "anmälningsavgift": "",
            "bild": "",
            "länk": link,
        })

    return events


def load_existing_events():
    try:
        with open(EVENTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def merge_events(existing, fetched):
    existing_keys = {(e.get("namn", ""), e.get("datum", "")) for e in existing}
    merged = list(existing)
    for event in fetched:
        key = (event.get("namn", ""), event.get("datum", ""))
        if key not in existing_keys:
            merged.append(event)
            existing_keys.add(key)
    return merged


def save_events(events):
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)


def main():
    print("Fetching Swedish dart events...")
    fetched = fetch_events_from_dart_se()
    print(f"Found {len(fetched)} new event(s) from dart.se")

    existing = load_existing_events()
    print(f"Existing events in file: {len(existing)}")

    merged = merge_events(existing, fetched)
    print(f"Total events after merge: {len(merged)}")

    save_events(merged)
    print("Dart-event.json updated successfully.")


if __name__ == "__main__":
    main()
