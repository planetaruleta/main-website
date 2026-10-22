#!/usr/bin/env python3
"""Write /llms-full.txt from the published guide HTML.

The body is the text already on each guide page. Navigation, footer, and the
repeated Telegram aside are left out. Wording, numbers, and caveats stay as
published. This does not invent claims.

Usage:
  python3 scripts/render_llms_full.py
  python3 scripts/render_llms_full.py --check
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "llms-full.txt"
ORIGIN = "https://www.planetaruleta.com"

# Sitemap order for the guide index and the eight guides.
PAGES: list[tuple[str, str]] = [
    ("guias/index.html", f"{ORIGIN}/guias/"),
    ("guias/rtp-volatilidad/index.html", f"{ORIGIN}/guias/rtp-volatilidad/"),
    ("guias/max-bet-contribucion-bono/index.html", f"{ORIGIN}/guias/max-bet-contribucion-bono/"),
    ("guias/cashback-rakeback-lossback/index.html", f"{ORIGIN}/guias/cashback-rakeback-lossback/"),
    ("guias/como-leer-una-promo-casino/index.html", f"{ORIGIN}/guias/como-leer-una-promo-casino/"),
    ("guias/usdt-vs-btc-bankroll/index.html", f"{ORIGIN}/guias/usdt-vs-btc-bankroll/"),
    ("guias/antes-de-retirar-rollover-kyc/index.html", f"{ORIGIN}/guias/antes-de-retirar-rollover-kyc/"),
    ("guias/rtp-ventaja-casa-ruleta/index.html", f"{ORIGIN}/guias/rtp-ventaja-casa-ruleta/"),
    ("guias/cloudbet-registro-paises-kyc/index.html", f"{ORIGIN}/guias/cloudbet-registro-paises-kyc/"),
]

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_TAGS = {"script", "style", "svg", "nav", "footer", "noscript"}
INLINE_TAGS = {
    "a", "abbr", "b", "br", "cite", "code", "em", "i", "kbd", "mark", "q",
    "s", "samp", "small", "span", "strong", "sub", "sup", "time", "u", "wbr",
}
HEADING_TAGS = {"h1", "h2", "h3", "h4"}

HEADER = """# Planeta Ruleta — texto de las guías

> Copia en texto de las guías públicas de alfabetización. El wording es el de cada página. Este archivo no agrega cifras, licencias ni rankings. +18. No es consejo de apuesta ni un enlace de afiliado.

Cada guía en el sitio cierra con la misma invitación al canal de Telegram @planetaruleta. Esa invitación no es un enlace de afiliado y no abre un depósito. Aquí se omite para no repetirla nueve veces.

"""


class Node:
    def __init__(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag = tag
        self.attrs = {key: (value or "") for key, value in attrs}
        self.children: list[Node | str] = []

    def classes(self) -> list[str]:
        return self.attrs.get("class", "").split()


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [])
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def find_article(node: Node) -> Node | None:
    if node.tag == "main" and "article" in node.classes():
        return node
    for child in node.children:
        if isinstance(child, Node):
            found = find_article(child)
            if found is not None:
                return found
    return None


def skipped(node: Node) -> bool:
    if node.tag in SKIP_TAGS:
        return True
    if node.tag == "aside" and "canal-cta" in node.classes():
        return True
    return False


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def edges(text: str) -> tuple[str, str, str]:
    lead = re.match(r"^\s*", text).group(0)
    trail = re.search(r"\s*$", text).group(0)
    return lead, clean(text), trail


def absolute(href: str, page_url: str) -> str:
    href = href.strip()
    if href.startswith(("https://", "http://", "mailto:")):
        return href
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return ORIGIN + href
    if href.startswith("#"):
        return page_url + href
    return href


def inline_raw(node: Node | str, page_url: str) -> str:
    """Keep the page's own spacing. Markup wraps the visible text only."""
    if isinstance(node, str):
        return node
    if skipped(node):
        return ""
    if node.tag == "br":
        return " "
    allowed = INLINE_TAGS | HEADING_TAGS | {"p", "li", "caption", "figcaption", "td", "th"}
    if node.tag not in allowed:
        return ""
    inner = "".join(inline_raw(child, page_url) for child in node.children)
    if node.tag == "a":
        lead, label, trail = edges(inner)
        href = node.attrs.get("href", "")
        if not href or not label:
            return inner
        url = absolute(href, page_url)
        shown = url if label == url else f"[{label}]({url})"
        return f"{lead}{shown}{trail}"
    if node.tag in {"strong", "b"}:
        lead, label, trail = edges(inner)
        return f"{lead}**{label}**{trail}" if label else inner
    if node.tag in {"em", "i"}:
        lead, label, trail = edges(inner)
        return f"{lead}*{label}*{trail}" if label else inner
    if node.tag == "code":
        lead, label, trail = edges(inner)
        return f"{lead}`{label}`{trail}" if label else inner
    return inner


def inline(node: Node | str, page_url: str) -> str:
    return clean(inline_raw(node, page_url))


def cell_text(node: Node, page_url: str) -> str:
    return inline(node, page_url).replace("|", "\\|")


def render_table(node: Node, page_url: str) -> str:
    caption = ""
    headers: list[str] = []
    rows: list[list[str]] = []
    for child in node.children:
        if not isinstance(child, Node):
            continue
        if child.tag == "caption":
            caption = inline(child, page_url)
        elif child.tag == "thead":
            for row in child.children:
                if isinstance(row, Node) and row.tag == "tr":
                    headers = [
                        cell_text(cell, page_url)
                        for cell in row.children
                        if isinstance(cell, Node) and cell.tag in {"th", "td"}
                    ]
        elif child.tag == "tbody":
            for row in child.children:
                if isinstance(row, Node) and row.tag == "tr":
                    rows.append(
                        [
                            cell_text(cell, page_url)
                            for cell in row.children
                            if isinstance(cell, Node) and cell.tag in {"th", "td"}
                        ]
                    )
        elif child.tag == "tr":
            rows.append(
                [
                    cell_text(cell, page_url)
                    for cell in child.children
                    if isinstance(cell, Node) and cell.tag in {"th", "td"}
                ]
            )
    width = max([len(headers), *[len(row) for row in rows]], default=0)
    if width == 0:
        return ""

    def pad(row: list[str]) -> list[str]:
        return row + [""] * (width - len(row))

    lines: list[str] = []
    if caption:
        lines.append(f"*{caption}*")
        lines.append("")
    head = pad(headers) if headers else [""] * width
    lines.append("| " + " | ".join(head) + " |")
    lines.append("| " + " | ".join("---" for _ in head) + " |")
    for row in rows:
        lines.append("| " + " | ".join(pad(row)) + " |")
    return "\n".join(lines)


def render_list(node: Node, page_url: str, ordered: bool) -> str:
    items: list[str] = []
    index = 1
    for child in node.children:
        if not isinstance(child, Node) or child.tag != "li" or skipped(child):
            continue
        item = render_blocks(child, page_url, in_list=True).strip()
        if not item:
            continue
        marker = f"{index}." if ordered else "-"
        item_lines = item.split("\n")
        indented = "\n".join(
            item_lines[0] if line_no == 0 else ("  " + line if line else "")
            for line_no, line in enumerate(item_lines)
        )
        items.append(f"{marker} {indented}")
        index += 1
    return "\n".join(items)


def render_blocks(node: Node, page_url: str, in_list: bool = False) -> str:
    chunks: list[str] = []
    inline_run: list[Node | str] = []

    def flush_inline() -> None:
        if not inline_run:
            return
        text = clean("".join(inline_raw(part, page_url) for part in inline_run))
        inline_run.clear()
        if text:
            chunks.append(text)

    for child in node.children:
        if isinstance(child, str) or (isinstance(child, Node) and child.tag in INLINE_TAGS):
            inline_run.append(child)
            continue
        flush_inline()
        if not isinstance(child, Node) or skipped(child):
            continue
        if child.tag in HEADING_TAGS:
            level = int(child.tag[1])
            text = inline(child, page_url)
            if not text:
                continue
            # A heading inside a card list stays in the item instead of breaking the list.
            chunks.append(f"**{text}**" if in_list else f"{'#' * level} {text}")
        elif child.tag == "p":
            text = inline(child, page_url)
            if text:
                chunks.append(text)
        elif child.tag == "ul":
            rendered = render_list(child, page_url, ordered=False)
            if rendered:
                chunks.append(rendered)
        elif child.tag == "ol":
            rendered = render_list(child, page_url, ordered=True)
            if rendered:
                chunks.append(rendered)
        elif child.tag == "table":
            rendered = render_table(child, page_url)
            if rendered:
                chunks.append(rendered)
        elif child.tag == "blockquote":
            text = inline(child, page_url)
            if text:
                chunks.append("\n".join(f"> {line}" for line in text.split("\n")))
        elif child.tag == "li":
            nested = render_blocks(child, page_url, in_list=True).strip()
            if nested:
                chunks.append(nested)
        else:
            nested = render_blocks(child, page_url, in_list=in_list).strip()
            if nested:
                chunks.append(nested)
    flush_inline()
    return "\n\n".join(chunk for chunk in chunks if chunk.strip())


def page_markdown(path: Path, page_url: str) -> str:
    parser = TreeBuilder()
    parser.feed(path.read_text(encoding="utf-8"))
    article = find_article(parser.root)
    if article is None:
        raise SystemExit(f"{path}: no <main class=\"article\">")
    body = render_blocks(article, page_url).strip()
    if "\n# " not in f"\n{body}" or not re.search(r"^# .+", body, re.M):
        raise SystemExit(f"{path}: article has no H1")
    return f"{body}\n\nURL: {page_url}\n"


def render() -> str:
    parts = [HEADER.rstrip(), ""]
    for relative, page_url in PAGES:
        parts.append(page_markdown(ROOT / relative, page_url).rstrip())
        parts.append("")
    text = "\n\n".join(part.strip("\n") for part in parts if part.strip()) + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    if text.startswith("---"):
        raise SystemExit("refusing to write a file Jekyll could treat as front matter")
    required = [
        "**Volatilidad baja:** premios más frecuentes y montos más pequeños.",
        "−1/37 = −0,0270… → ventaja **2,70 %**, RTP 36/37 = 97,297… ≈ **97,30 %**.",
        "−2/38 = −0,0526… → ventaja **5,26 %**, RTP 36/38 = 94,736… ≈ **94,74 %**.",
        "licencia **OGL/2024/328/0599**",
        "[/mesa/shuffle/](https://www.planetaruleta.com/mesa/shuffle/).",
        "[cómo leer una promo](https://www.planetaruleta.com/guias/como-leer-una-promo-casino/).",
        "**Cashback**, **rakeback** y **lossback**",
        "El **RTP** (return to player) es el porcentaje teórico",
        "- **[RTP y volatilidad en slots](https://www.planetaruleta.com/guias/rtp-volatilidad/)**",
    ]
    missing = [snippet for snippet in required if snippet not in text]
    if missing:
        raise SystemExit("guide extract dropped or rewrote published wording:\n- " + "\n- ".join(missing))
    if "- ## " in text or " ( return to player ) " in text:
        raise SystemExit("guide extract still splits inline markup")
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if llms-full.txt is stale")
    args = parser.parse_args()
    text = render()
    if args.check:
        current = OUT_PATH.read_text(encoding="utf-8") if OUT_PATH.exists() else ""
        if current != text:
            print("llms-full.txt is stale. Run: python3 scripts/render_llms_full.py", file=sys.stderr)
            return 1
        print("llms-full.txt matches the guide pages")
        return 0
    OUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(ROOT)} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
