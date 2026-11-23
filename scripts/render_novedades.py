#!/usr/bin/env python3
"""Render the homepage Novedades strip from content/novedades.json.

The homepage must not go more than 4 days without a visible update
(Aviv, 22 Nov 2026). Edit the JSON (3–4 shipped items, newest first),
then run this script.

Usage:
  python3 scripts/render_novedades.py
  python3 scripts/render_novedades.py --check
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "content" / "novedades.json"
HOME_PATH = ROOT / "index.html"
START = "<!-- novedades:home -->"
END = "<!-- /novedades:home -->"
MONTHS = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC",
}
MIN_ITEMS = 3
MAX_ITEMS = 4


def load_items() -> list[dict]:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    items = payload.get("items")
    if not isinstance(items, list):
        raise SystemExit(f"{DATA_PATH}: missing items list")
    if not MIN_ITEMS <= len(items) <= MAX_ITEMS:
        raise SystemExit(
            f"{DATA_PATH}: need {MIN_ITEMS}–{MAX_ITEMS} items, got {len(items)}"
        )
    parsed: list[dict] = []
    prev: date | None = None
    for index, raw in enumerate(items, start=1):
        try:
            day = date.fromisoformat(str(raw["date"]))
        except (KeyError, ValueError) as exc:
            raise SystemExit(f"{DATA_PATH}: item {index} has a bad date") from exc
        title = str(raw.get("title") or "").strip()
        href = str(raw.get("href") or "").strip()
        line = str(raw.get("line") or "").strip()
        if not title or not href or not line:
            raise SystemExit(f"{DATA_PATH}: item {index} needs title, href and line")
        if not (href.startswith("/") or href.startswith("https://")):
            raise SystemExit(f"{DATA_PATH}: item {index} href must be a root path or https URL")
        if prev is not None and day > prev:
            raise SystemExit(f"{DATA_PATH}: items must be newest first (item {index} is later)")
        prev = day
        parsed.append({"date": day, "title": title, "href": href, "line": line})
    return parsed


def format_visible(day: date) -> str:
    return f"{day.day:02d} {MONTHS[day.month]}"


def attr(url: str) -> str:
    extra = ' target="_blank" rel="noopener"' if url.startswith("https://") else ""
    return f'href="{html.escape(url, quote=True)}"{extra}'


def render_items(items: list[dict]) -> str:
    lines = [START]
    for item in items:
        visible = format_visible(item["date"])
        iso = item["date"].isoformat()
        title = html.escape(item["title"])
        line = html.escape(item["line"])
        lines.append(
            f'        <p class="mesa-aside"><time datetime="{iso}">{visible}</time>'
            f' · <strong><a {attr(item["href"])}>{title}</a>.</strong> {line}</p>'
        )
    lines.append(f"        {END}")
    return "\n".join(lines)


def replace_marked(text: str, body: str) -> str:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        raise SystemExit(f"{HOME_PATH}: missing {START} … {END} markers")
    return pattern.sub(body, text, count=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the homepage strip is stale")
    args = parser.parse_args()
    items = load_items()
    rendered = render_items(items)
    current = HOME_PATH.read_text(encoding="utf-8")
    updated = replace_marked(current, rendered)
    if args.check:
        if current != updated:
            print("index.html Novedades strip is stale. Run: python3 scripts/render_novedades.py", file=sys.stderr)
            return 1
        print("index.html Novedades strip matches content/novedades.json")
        return 0
    if current != updated:
        HOME_PATH.write_text(updated, encoding="utf-8")
        print(f"updated {HOME_PATH.relative_to(ROOT)} ({len(items)} items)")
    else:
        print(f"{HOME_PATH.relative_to(ROOT)} already matches content/novedades.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
