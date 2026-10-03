#!/usr/bin/env python3
"""Render señales HTML from the shared public feed.

Source: content/senales.json (published copy only).
Order: fecha descending. Rows that share a fecha keep their order in that file.
Homepage: the first 3 (HOME_LIMIT). Archive (/senales/): the full list.

The intel pack (content/intel/homepage-offshore-wave1-2026-09-25.json) is the
claim record. Every ready id in senales_lead, senales_timeline, and senales_hold
must match this feed (id + fecha) before anything is written. Internal draft
paths are never rendered from that pack.

Usage:
  python3 scripts/render_senales.py
  python3 scripts/render_senales.py --check
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED_PATH = ROOT / "content" / "senales.json"
INTEL_PATH = ROOT / "content" / "intel" / "homepage-offshore-wave1-2026-09-25.json"
HOME_PATH = ROOT / "index.html"
ARCHIVE_PATH = ROOT / "senales" / "index.html"

HOME_LIMIT = 3
MONTHS = (
    None,
    "ENE",
    "FEB",
    "MAR",
    "ABR",
    "MAY",
    "JUN",
    "JUL",
    "AGO",
    "SEP",
    "OCT",
    "NOV",
    "DIC",
)

HOME_START = "<!-- senales:home -->"
HOME_END = "<!-- /senales:home -->"
ARCHIVE_START = "<!-- senales:archive -->"
ARCHIVE_END = "<!-- /senales:archive -->"
JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json" id="senales-ld">)(.*?)(</script>)',
    re.S,
)


def fecha_corta(iso: str) -> str:
    year, month, day = iso.split("-")
    if len(year) != 4:
        raise ValueError(f"bad fecha: {iso}")
    return f"{int(day):02d} {MONTHS[int(month)]}"


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def esc_attr(value: str) -> str:
    return html.escape(value, quote=True)


def newest_first(items: list[dict]) -> list[dict]:
    """Stable sort: newest fecha first; equal fechas keep feed order."""
    return sorted(items, key=lambda item: item["fecha"], reverse=True)


def load_feed() -> list[dict]:
    data = json.loads(FEED_PATH.read_text())
    items = data["senales"]
    if not isinstance(items, list) or not items:
        raise SystemExit("content/senales.json has no señales")
    seen = set()
    for item in items:
        for key in ("id", "fecha", "kicker", "titulo", "resumen", "fuentes_html"):
            if not item.get(key):
                raise SystemExit(f"{item.get('id', '?')} missing {key}")
        if item["id"] in seen:
            raise SystemExit(f"duplicate id {item['id']}")
        seen.add(item["id"])
        fecha_corta(item["fecha"])
        blob = item["resumen"] + item["fuentes_html"] + item["titulo"]
        if "docs/" in blob or "docs\\drafts" in blob:
            raise SystemExit(f"{item['id']} contains an internal draft path")
    return items


def assert_matches_intel(items: list[dict]) -> None:
    intel = json.loads(INTEL_PATH.read_text())
    ready = []
    for key in ("senales_lead", "senales_timeline", "senales_hold"):
        for row in intel.get(key, []):
            if row.get("status") == "ready":
                ready.append(row)
    feed_by_id = {item["id"]: item for item in items}
    intel_by_id = {row["id"]: row for row in ready}
    if set(feed_by_id) != set(intel_by_id):
        missing = sorted(set(intel_by_id) - set(feed_by_id))
        extra = sorted(set(feed_by_id) - set(intel_by_id))
        raise SystemExit(
            "señales feed and intel pack diverged. "
            f"missing from feed: {missing or '—'} extra in feed: {extra or '—'}"
        )
    for item_id, item in feed_by_id.items():
        if item["fecha"] != intel_by_id[item_id]["fecha"]:
            raise SystemExit(
                f"{item_id} fecha {item['fecha']} != intel {intel_by_id[item_id]['fecha']}"
            )


def render_li(item: dict, heading: str) -> str:
    return "\n".join(
        [
            f'          <li id="{esc_attr(item["id"])}">',
            f'            <time datetime="{esc_attr(item["fecha"])}">{esc(fecha_corta(item["fecha"]))}</time>',
            "            <div>",
            f'              <p class="kicker">{esc(item["kicker"])}</p>',
            f'              <{heading}>{esc(item["titulo"])}</{heading}>',
            f'              <p class="resumen">{esc(item["resumen"])}</p>',
            f'              <p class="fuentes">{item["fuentes_html"]}</p>',
            "            </div>",
            "          </li>",
        ]
    )


def render_home(items: list[dict]) -> str:
    lead = items[0]
    rows = items[1:]
    numero = lead.get("numero") or ""
    numero_html = (
        f'          <p class="lead-num"><i>{esc(numero)}</i></p>\n' if numero else ""
    )
    lead_html = "\n".join(
        [
            '        <article class="lead" id="senal-lead">',
            numero_html.rstrip("\n"),
            f'          <div class="lead-body" id="{esc_attr(lead["id"])}">',
            (
                f'            <p class="kicker"><time datetime="{esc_attr(lead["fecha"])}">'
                f'{esc(fecha_corta(lead["fecha"]))}</time> · {esc(lead["kicker"])}</p>'
            ),
            f'            <h3>{esc(lead["titulo"])}</h3>',
            f'            <p class="resumen">{esc(lead["resumen"])}</p>',
            f'            <p class="fuentes">{lead["fuentes_html"]}</p>',
            "          </div>",
            "        </article>",
        ]
    )
    # Drop the blank line when there is no numero block.
    if not numero:
        lead_html = lead_html.replace(
            '        <article class="lead" id="senal-lead">\n\n',
            '        <article class="lead" id="senal-lead">\n',
        )
    timeline = "\n".join(
        ['        <ol class="timeline">', *[render_li(item, "h3") for item in rows], "        </ol>"]
    )
    return lead_html + "\n\n" + timeline


def render_archive(items: list[dict]) -> str:
    return "\n".join(render_li(item, "h2") for item in items)


def render_jsonld(items: list[dict]) -> str:
    description = (
        "Todas las señales publicadas, de la más nueva a la más vieja. "
        "Declarado sale del texto del operador. +18. No somos un casino."
    )
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://www.planetaruleta.com/#organization",
                "name": "Planeta Ruleta",
                "url": "https://www.planetaruleta.com/",
                "logo": "https://www.planetaruleta.com/logo-saturn.png",
                "email": "planetaruleta@protonmail.com",
                "description": "Comunidad e inteligencia de casinos, en español. El día a día está en Telegram. No somos un casino.",
                "sameAs": ["https://t.me/planetaruleta"],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "consultas",
                    "email": "planetaruleta@protonmail.com",
                    "url": "https://t.me/planetaruleta",
                    "availableLanguage": "es",
                },
            },
            {
                "@type": "CollectionPage",
                "@id": "https://www.planetaruleta.com/senales/#webpage",
                "url": "https://www.planetaruleta.com/senales/",
                "name": "Archivo de señales — Planeta Ruleta",
                "description": description,
                "inLanguage": "es",
                "dateModified": items[0]["fecha"],
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://www.planetaruleta.com/#website",
                    "name": "Planeta Ruleta",
                    "url": "https://www.planetaruleta.com/",
                },
                "about": {"@id": "https://www.planetaruleta.com/#organization"},
                "publisher": {"@id": "https://www.planetaruleta.com/#organization"},
                "breadcrumb": {"@id": "https://www.planetaruleta.com/senales/#breadcrumb"},
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(items),
                    "itemListOrder": "https://schema.org/ItemListOrderDescending",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index,
                            "name": item["titulo"],
                            "url": f"https://www.planetaruleta.com/senales/#{item['id']}",
                        }
                        for index, item in enumerate(items, start=1)
                    ],
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": "https://www.planetaruleta.com/senales/#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Inicio",
                        "item": "https://www.planetaruleta.com/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Archivo de señales",
                        "item": "https://www.planetaruleta.com/senales/",
                    },
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def replace_marked(text: str, start: str, end: str, inner: str, label: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{inner}\n        {end}"
    new, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"missing {label} markers")
    return new


def replace_jsonld(text: str, payload: str) -> str:
    indented = "\n".join(f"  {line}" if line else line for line in payload.splitlines())

    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}\n{indented}\n  {match.group(3)}"

    new, count = JSONLD_RE.subn(repl, text, count=1)
    if count != 1:
        raise SystemExit("missing #senales-ld script")
    return new


def assert_hero_matches_newest(home_html: str, newest: dict) -> None:
    match = re.search(
        r'class="ultima-meta">Última señal · <time datetime="([^"]+)">',
        home_html,
    )
    if not match:
        raise SystemExit("homepage hero is missing the Última señal chip")
    if match.group(1) != newest["fecha"]:
        raise SystemExit(
            "Última señal chip is "
            f"{match.group(1)} but the newest señal is {newest['fecha']} ({newest['id']}). "
            "Update the hero chip, then render again."
        )


def self_test_sort() -> None:
    sample = [
        {"id": "older-same-day", "fecha": "2026-09-25"},
        {"id": "newest", "fecha": "2026-10-02"},
        {"id": "later-same-day", "fecha": "2026-09-25"},
        {"id": "middle", "fecha": "2026-09-28"},
    ]
    ordered = [item["id"] for item in newest_first(sample)]
    expect = ["newest", "middle", "older-same-day", "later-same-day"]
    if ordered != expect:
        raise SystemExit(f"sort self-test failed: {ordered}")


def build() -> tuple[str, str, list[dict], list[dict]]:
    self_test_sort()
    feed = load_feed()
    assert_matches_intel(feed)
    ordered = newest_first(feed)
    if len(ordered) < HOME_LIMIT:
        raise SystemExit(f"need at least {HOME_LIMIT} señales, found {len(ordered)}")
    home_items = ordered[:HOME_LIMIT]
    if len(home_items) != HOME_LIMIT:
        raise SystemExit("homepage slice did not cap at 3")
    home_html = HOME_PATH.read_text()
    archive_html = ARCHIVE_PATH.read_text()
    assert_hero_matches_newest(home_html, ordered[0])
    home_html = replace_marked(home_html, HOME_START, HOME_END, render_home(home_items), "homepage")
    archive_html = replace_marked(
        archive_html, ARCHIVE_START, ARCHIVE_END, render_archive(ordered), "archive"
    )
    archive_html = replace_jsonld(archive_html, render_jsonld(ordered))
    return home_html, archive_html, home_items, ordered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render homepage and /senales/ from content/senales.json")
    parser.add_argument("--check", action="store_true", help="fail if rendered HTML is stale")
    args = parser.parse_args()
    home_html, archive_html, home_items, ordered = build()
    if args.check:
        stale = []
        if home_html != HOME_PATH.read_text():
            stale.append(str(HOME_PATH))
        if archive_html != ARCHIVE_PATH.read_text():
            stale.append(str(ARCHIVE_PATH))
        if stale:
            print("stale señales HTML: " + ", ".join(stale), file=sys.stderr)
            print("run: python3 scripts/render_senales.py", file=sys.stderr)
            return 1
    else:
        HOME_PATH.write_text(home_html)
        ARCHIVE_PATH.write_text(archive_html)
    print(f"homepage ({HOME_LIMIT}): " + ", ".join(item["id"] for item in home_items))
    print(f"archive ({len(ordered)}): " + ", ".join(item["id"] for item in ordered))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
