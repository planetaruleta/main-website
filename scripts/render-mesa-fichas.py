#!/usr/bin/env python3
"""Render mesa fichas for the five offshore operators.

Facts come from the homepage intel JSON, the señales archive, and the 03 OCT 2026
fact-check of official help, terms, and licence pages. HTML in /mesa/ is the
published page. Re-run this script after editing copy here.
Unverified cells stay explicit. No scores, no affiliate URL, no /casinos/ play pages.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "https://www.planetaruleta.com"
ORG_ID = f"{HOST}/#organization"

OPS = [
    ("rainbet", "Rainbet", True, "En la mesa"),
    ("shuffle", "Shuffle", True, "En la mesa"),
    ("stake", "Stake", True, "En la mesa"),
    ("cloudbet", "Cloudbet", True, "En la mesa"),
    ("roobet", "Roobet", True, "En la mesa"),
]

ROWS = [
    (
        "Tipo de bono real",
        [
            "Welcome: x40 sobre depósito+bono, o camino sin ese rollover. Race y torneo de lobby son señales, no este chip.",
            "Rakeback 5% del house edge (Bronze), cash, casino. Level Up es señal aparte (aprox). FTD: bases no publicadas.",
            "Rakeback 3.5% del house edge (welcome), vía código. No es un match con WR fijo.",
            "≤$2.5k/30d · 10% RB. Tal cual la celda (30 SEP 2026). Sin WR en la celda.",
            "Instant RB · +10% welcome 24h. Tal cual la celda (30 SEP 2026). Sin WR en la celda.",
        ],
    ),
    (
        "Criptos / redes",
        [
            "FAQ 25 SEP 2026: BTC, ETH, LTC, XRP, SOL, TRX, BNB, USDT, USDC. Redes: no verificado · 03 OCT 2026.",
            "Clase: crypto · fiat/cards. Lista y redes: no verificado · 03 OCT 2026. USDT solo en el ejemplo de rakeback.",
            "Clase: crypto · fiat. Lista y redes: no verificado · 03 OCT 2026. BTC solo en el ejemplo de rakeback.",
            "Clase: crypto · buy card (Swapped). Lista y redes: no verificado · 03 OCT 2026.",
            "Clase: crypto · fiat+Swapped. Lista y redes: no verificado · 03 OCT 2026.",
        ],
    ),
    (
        "KYC",
        [
            "ID + selfie + prueba de domicilio (Sumsub). Terms/AML: pueden restringir si el ID no se completa en 72 h; la verificación puede tardar hasta 7 días hábiles.",
            "ID de gobierno antes del primer retiro (Terms). Help: email → datos → ID → prueba de domicilio.",
            "Help 24 ago 2026: pasaporte, DNI ambos lados o licencia ambos lados. Cuándo lo exigen: no verificado · 25 SEP 2026.",
            "Niveles · L2 ID + prueba de domicilio + face (Sumsub). Más detalle del disparador: no verificado · 03 OCT 2026.",
            "L2 ID (pasaporte, licencia o documento de gobierno). Más detalle del disparador: no verificado · 03 OCT 2026.",
        ],
    ),
    (
        "Sportsbook",
        [
            "Sportsbook declarado en la homepage y en /sportsbook (título “Online Sportsbook”). 03 OCT 2026.",
            "Sportsbook declarado: título de la homepage y /sports. El help de coin-mixing nombra “the sportsbook”. El rakeback no corre en sports. 03 OCT 2026.",
            "Sportsbook declarado en el help (sección Sports; las apuestas sports cuentan al wager). stake.com/sports HTTP 403 el 03 OCT 2026.",
            "Sportsbook declarado: /en/sports, título “Crypto Sports Betting”. 03 OCT 2026.",
            "no verificado · 03 OCT 2026",
        ],
    ),
    (
        "Licencia",
        [
            "Anjouan, declarada en Terms, AML y footer (25 SEP 2026). Validador no chequeado.",
            "Curaçao Gaming Authority, OGL/2024/1337/0628, Natural Nine B.V. (160998). /info/license dice “Gaming Control Board”; Terms y el certificado CGA dicen “Gaming Authority”. Certificado Active.",
            "Curaçao-class por certificado CGA: OGL/2024/1451/0918, Active, otorgado 09/06/2025. Footer del operador no capturado (HTTP 403).",
            "Curaçao Gaming Authority, OGL/2024/328/0599, Halcyon Super Holdings B.V. (148526). Help, 03 OCT 2026. No es licencia de Argentina.",
            "no verificado · 30 SEP 2026",
        ],
    ),
    (
        "En la mesa",
        [
            "sí",
            "sí",
            "sí",
            "sí",
            "sí",
        ],
    ),
    (
        "Última revisión",
        [
            "25 SEP 2026 (fila). Señales de lobby: 26 SEP y 30 SEP 2026.",
            "28 SEP 2026 (rakeback). Level Up: 02 OCT 2026.",
            "25 SEP 2026",
            "30 SEP 2026 (bono, KYC, métodos). Licencia y sportsbook: 03 OCT 2026.",
            "30 SEP 2026 (bono, KYC, métodos). Sportsbook y licencia rechequeados: 03 OCT 2026.",
        ],
    ),
]


def e(text: str) -> str:
    return html.escape(text, quote=True)


def compare_table() -> str:
    heads = []
    for slug, name, has_ficha, sub in OPS:
        label = f'<a href="/mesa/{slug}/">{e(name)}</a>' if has_ficha else e(name)
        heads.append(f'                <th scope="col">{label}<span>{e(sub)}</span></th>\n')
    body = []
    for label, cells in ROWS:
        tds = []
        for (slug, name, has_ficha, sub), cell in zip(OPS, cells):
            op = name if has_ficha else f"{name} · candidato"
            tds.append(
                f'                <td data-op="{e(op)}"><span class="op-name">{e(op)}</span>{e(cell)}</td>\n'
            )
        body.append(
            "              <tr>\n"
            f'                <th scope="row">{e(label)}</th>\n'
            + "".join(tds)
            + "              </tr>\n"
        )
    return f"""
        <p class="scroll-hint">Deslizá para comparar</p>
        <div class="cmp-scroll">
          <table class="cmp">
            <caption>Misma tabla en la mesa y al pie de cada ficha. Sin insignia de ganador. Si el dato no está en la mesa ni en una señal, la celda dice no verificado.</caption>
            <thead>
              <tr>
                <th scope="col">Dato</th>
{''.join(heads)}
              </tr>
            </thead>
            <tbody>
              {''.join(body)}
            </tbody>
          </table>
        </div>
"""


def org() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Planeta Ruleta",
        "url": f"{HOST}/",
        "logo": f"{HOST}/logo-saturn.png",
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
    }


def crumbs_html(items: list[tuple[str, str | None]]) -> str:
    lis = []
    for name, href in items:
        if href:
            lis.append(f'<li><a href="{e(href)}">{e(name)}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{e(name)}</span></li>')
    return f'<nav class="crumbs" aria-label="Migas"><ol>{"".join(lis)}</ol></nav>'


def breadcrumb_ld(url: str, items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": item,
            }
            for i, (name, item) in enumerate(items, start=1)
        ],
    }


def faq_ld(url: str, faqs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "url": url,
        "inLanguage": "es",
        "isPartOf": {"@id": f"{HOST}/#website"},
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def faq_html(faqs: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in faqs:
        blocks.append(
            f"""<details class="faq">
          <summary><h3>{e(q)}</h3></summary>
          <div class="answer"><p>{e(a)}</p></div>
        </details>"""
        )
    return f'<div class="faq-list">{"".join(blocks)}</div>'


def sheet_html(rows: list[tuple[str, str]]) -> str:
    parts = []
    for dt, dd in rows:
        parts.append(f"<div><dt>{e(dt)}</dt><dd>{e(dd)}</dd></div>")
    return f'<dl class="sheet">{"".join(parts)}</dl>'


def fuentes_html(links: list[tuple[str, str]]) -> str:
    bits = []
    for label, href in links:
        bits.append(
            f'<a href="{e(href)}" target="_blank" rel="noopener">{e(label)}</a>'
        )
    return f'<p class="fuentes">Fuentes · {" · ".join(bits)}</p>'


def senales_block(data: dict) -> str:
    items = data["senales"]
    if not items:
        return "<p>No hay señales de este operador en el archivo. No es un hub por operador.</p>"
    return (
        "<p>Salen del archivo de señales. No es un hub por operador.</p>\n          "
        + senales_html(items)
    )


def senales_html(items: list[dict]) -> str:
    lis = []
    for item in items:
        lis.append(
            f"""<li>
            <time datetime="{e(item["date"])}">{e(item["when"])}</time>
            <a href="/senales/#{e(item["id"])}">{e(item["title"])}</a>
            <p>{e(item["line"])}</p>
          </li>"""
        )
    return f'<ul class="senal-list">{"".join(lis)}</ul>'


def affiliate_html() -> str:
    return """<aside class="affiliate-slot" aria-label="Enlace de afiliado">
        <p class="affiliate-kicker">Afiliado</p>
        <p class="affiliate-empty">Enlace de afiliado no activo.</p>
      </aside>"""


def mast() -> str:
    return """<a class="skip" href="#contenido">Saltar al contenido</a>
  <header class="mast">
    <div class="mast-inner">
      <a class="brand" href="/"><span class="brand-name">Planeta Ruleta</span></a>
      <nav aria-label="Principal">
        <a href="/#senales">Señales</a>
        <a href="/mesa/" aria-current="page">Mesa</a>
        <a href="/como-funciona/">Cómo funciona</a>
        <a href="/sobre/">Sobre</a>
        <a href="/guias/">Guías</a>
        <a href="/faq/">FAQ</a>
      </nav>
      <p class="mast-end">
        <a class="mast-tg" href="https://t.me/planetaruleta" target="_blank" rel="noopener" data-cta="telegram" data-cta-location="nav">Sumate al canal</a>
      </p>
    </div>
  </header>"""


def footer() -> str:
    return """<footer class="site-footer">
    <a href="/mesa/">Mesa</a> ·
    <a href="/#senales">Señales</a> ·
    <a href="/como-funciona/">Cómo funciona</a> ·
    <a href="/sobre/">Sobre</a> ·
    <a href="/guias/">Guías</a> ·
    <a href="/faq/">FAQ</a><br />
    +18 · no somos un casino · offshore no es licencia de Argentina · <a href="mailto:planetaruleta@protonmail.com">planetaruleta@protonmail.com</a> · <a href="https://www.planetaruleta.com/">planetaruleta.com</a><br />
    Planeta Ruleta © <span data-year></span>
  </footer>
  <script>
    (() => {
      const year = new Date().getFullYear();
      document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = String(year); });
    })();
  </script>"""


def head(title: str, description: str, path: str, graph: list) -> str:
    url = f"{HOST}{path}"
    payload = {"@context": "https://schema.org", "@graph": graph}
    ld = json.dumps(payload, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <link rel="canonical" href="{e(url)}" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{e(url)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:image" content="{HOST}/logo-saturn.png" />
  <meta property="og:locale" content="es_LA" />
  <meta property="og:site_name" content="Planeta Ruleta" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(description)}" />
  <meta name="twitter:image" content="{HOST}/logo-saturn.png" />
  <script type="application/ld+json">
{ld}
  </script>
  <meta name="theme-color" content="#0B1520" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=Ibarra+Real+Nova:ital,wght@0,500;0,600;0,700;1,500;1,600&amp;family=Schibsted+Grotesk:ital,wght@0,500;0,600;0,700;1,500&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/mesa.css" />
  <script src="/js/config.js"></script>
  <script src="/js/analytics.min.js"></script>
</head>"""


def page(title: str, description: str, path: str, graph: list, body: str) -> str:
    return f"""{head(title, description, path, graph)}
<body>
  {mast()}
  <main id="contenido" class="page">
    <div class="wrap">
      {body}
    </div>
  </main>
  {footer()}
</body>
</html>
"""


def otros_html(current: str | None) -> str:
    bits = []
    for slug, name, has_ficha, _sub in OPS:
        if slug == current:
            continue
        if has_ficha:
            bits.append(
                f'<li><a href="/mesa/{slug}/">{e(name)}</a><span class="tag">En la mesa · ficha</span></li>'
            )
        else:
            bits.append(
                f"<li><span>{e(name)}</span><span class=\"tag\">Candidato · sin ficha</span></li>"
            )
    return f'<ul class="otros">{"".join(bits)}</ul>'


INDEX_FAQS = [
    (
        "¿Estas fichas son un ranking?",
        "No. No hay puntaje ni puesto. La comparación repite hechos declarados en la mesa o en las señales. Si el dato no está, la celda dice no verificado.",
    ),
    (
        "¿Cloudbet y Roobet tienen ficha?",
        "Sí. Las cinco fichas están en la mesa: Rainbet, Shuffle, Stake, Cloudbet y Roobet. No hay puntaje ni enlace de afiliado.",
    ),
    (
        "¿El enlace de afiliado está activo?",
        "No. En cada ficha el espacio está y dice enlace de afiliado no activo. No hay botón de juego ni código para cargar.",
    ),
    (
        "¿Offshore es una licencia de Argentina?",
        "No. Una licencia que el operador publica en Anjouan o en Curaçao no es una licencia del registro argentino. La mesa no ordena filas por licencia local. +18.",
    ),
]


def render_index() -> str:
    path = "/mesa/"
    url = f"{HOST}{path}"
    title = "Mesa — fichas | Planeta Ruleta"
    description = (
        "Fichas editoriales de la mesa: Rainbet, Shuffle, Stake, Cloudbet y Roobet. "
        "Sin puntaje ni enlace de afiliado. +18."
    )
    graph = [
        org(),
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "es",
            "isPartOf": {"@type": "WebSite", "@id": f"{HOST}/#website", "name": "Planeta Ruleta", "url": f"{HOST}/"},
            "about": {"@id": ORG_ID},
            "publisher": {"@id": ORG_ID},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "dateModified": "2026-10-03",
        },
        breadcrumb_ld(url, [("Inicio", f"{HOST}/"), ("Mesa", url)]),
        faq_ld(url, INDEX_FAQS),
    ]
    body = f"""
      {crumbs_html([("Inicio", "/"), ("Mesa", None)])}
      <p class="estado">Fichas</p>
      <h1>Mesa</h1>
      <p class="lede">La mesa pública, en fichas. Rainbet, Shuffle, Stake, Cloudbet y Roobet tienen perfil editorial.</p>
      <p class="lede">No hay puntaje. El enlace de afiliado no está activo. +18.</p>
      <ul class="cards">
        <li><a class="card" href="/mesa/rainbet/"><p class="estado">En la mesa</p><h2>Rainbet</h2><p>Welcome con dos caminos declarados. Licencia de Anjouan, según la casa. Retiro sin SLA.</p></a></li>
        <li><a class="card" href="/mesa/shuffle/"><p class="estado">En la mesa</p><h2>Shuffle</h2><p>Chip de rakeback 5% HE (Bronze). Level Up es otra señal, con números aproximados.</p></a></li>
        <li><a class="card" href="/mesa/stake/"><p class="estado">En la mesa</p><h2>Stake</h2><p>Welcome publicado como rakeback 3.5% HE. La licencia citada es el certificado CGA: el footer del sitio no se pudo leer.</p></a></li>
        <li><a class="card" href="/mesa/cloudbet/"><p class="estado">En la mesa</p><h2>Cloudbet</h2><p>Welcome de hasta 2.500 USD en 30 días y rakeback 10% del house edge en casino. Licencia CGA declarada en el help.</p></a></li>
        <li><a class="card" href="/mesa/roobet/"><p class="estado">En la mesa</p><h2>Roobet</h2><p>Instant rakeback y un boost de +10% por 24 h al registrarse. Licencia y sportsbook público: no verificado.</p></a></li>
      </ul>
      <p>La tira corta sigue en <a href="/#mesa">la home</a>. Los cinco nombres abren su ficha.</p>
      {affiliate_html()}
      <section class="cmp-sec" id="comparacion" aria-labelledby="comparacion-title">
        <h2 id="comparacion-title">Comparación</h2>
        <p class="cmp-note">Las cinco fichas. Hechos de la mesa y de las señales. Hueco = no verificado, con fecha.</p>
        {compare_table()}
      </section>
      <section class="block" id="faq" aria-labelledby="faq-title">
        <h2 id="faq-title">Preguntas</h2>
        {faq_html(INDEX_FAQS)}
      </section>
"""
    return page(title, description, path, graph, body)


FICHAS = {
    "rainbet": {
        "name": "Rainbet",
        "title": "Rainbet — ficha de la mesa | Planeta Ruleta",
        "description": "Ficha editorial de Rainbet: licencia de Anjouan declarada, welcome x40 o sin rollover, KYC y señales. Sin puntaje. Offshore no es licencia de Argentina. +18.",
        "modified": "2026-10-03",
        "lede": [
            "Rainbet está en la mesa como operador crypto/offshore: la casa declara licencia de Anjouan y un welcome con dos caminos.",
            "Esta ficha no pone nota ni abre un depósito. Junta la fila, las señales y lo que sigue sin verificar.",
        ],
        "sheet": [
            ("Empresa", "Rain Group Ltd (co. 16077, Hamchako), en Terms, AML y footer. El JSON-LD de la homepage también nombra RBGAMING N.V. Las dos cadenas están publicadas y no coinciden: no elegimos una sola razón social."),
            ("Licencia", "Anjouan, declarada en Terms, AML y footer (25 SEP 2026). El validador de Anjouan no se chequeó. No es una licencia del registro argentino."),
            ("Monedas", "FAQ de rainbet.com, 25 SEP 2026: BTC, ETH, LTC, XRP, SOL, TRX, BNB, USDT y USDC. Redes: no verificado · 03 OCT 2026."),
            ("Idiomas", "JSON-LD knowsLanguage: en, ar, es, fr, ja, pt, ru, tr, zh (homepage, 03 OCT 2026)."),
            ("Última revisión", "Fila de la mesa: 25 SEP 2026. Señales de lobby: Daily Race 26 SEP 2026 y torneo Gates of Olympus 30 SEP 2026. Huecos marcados al armar la ficha: 03 OCT 2026."),
        ],
        "fuentes": [
            ("rainbet.com", "https://rainbet.com/"),
            ("Terms", "https://rainbet.com/terms"),
            ("AML", "https://rainbet.com/aml"),
            ("Daily Race", "https://rainbet.com/daily-race"),
            ("Torneo Gates of Olympus", "https://rainbet.com/promotions/gates-of-olympus-2500-multiplier-mayhem-40k-tournament"),
        ],
        "plata_title": "Cómo entra y sale la plata",
        "plata": [
            "El FAQ declara criptos, entre ellas USDT, y también bank transfers, cards y gift cards. La tira de la home sigue en la clase crypto · fiat/cards. La tabla de esta ficha lista las criptos del FAQ. Redes: no verificado.",
            "Ese “bank transfer” es una frase del operador. No es un depósito por CBU ni un cajero de casino regulado en Argentina.",
            "En la homepage también está escrito un mínimo de retiro de 15 USD y apostar 1x el depósito antes de retirar. No es un plazo. El marketing de 5 a 15 minutos no entra como SLA: el retiro de la mesa sigue en sin dato.",
        ],
        "bono": [
            "El chip de la fila es el welcome, no el race. Camino A: 40x sobre depósito+bono (100% / 50% / 100% + 20 tiradas, mínimo 30 USD, máximo 700 USD por tramo, apuesta máxima 2% del depósito, slots con RTP mayor a 97,4% fuera). Camino B: sin ese rollover; se desbloquea al jugar. Hay que optar en promotions antes de depositar. Fuente: homepage, 25 SEP 2026.",
            "El Daily Race del 26 SEP y el torneo Gates of Olympus 2500 del 30 SEP son señales de lobby, con ventana publicada. No reemplazan el chip.",
            "Para leer un rollover y un rakeback sin mezclarlos: guías de promo, de max bet y de rakeback.",
        ],
        "kyc": "KYC declarado: documento de identidad, selfie y prueba de domicilio. Sumsub está nombrado en el AML, no en Terms §20. Terms §20: pueden restringir la cuenta si el ID no se completa en 72 horas; la verificación puede tardar hasta 7 días hábiles; el equipo de KYC habla de 24 horas una vez Temporarily Approved. Fuente: Terms y AML, revisión de mesa 25 SEP 2026 / rechequeo 03 OCT 2026.",
        "offshore": "Rainbet publica una licencia de Anjouan. Eso no es una licencia de Argentina ni convierte a esta página en un casino. No hay puntaje, no hay puesto y no hay instrucciones para saltar un bloqueo. +18.",
        "senales": [
            {
                "id": "lobby-rainbet-gates-olympus-40k-2026-09-30",
                "date": "2026-09-30",
                "when": "30 SEP 2026 · Lobby",
                "title": "Gates of Olympus 2500: torneo $40K — multiplicadores, no jackpot por caer",
                "line": "Promo oficial verificado el 30 SEP 2026. Pozo publicado 40.000 USD, 100 lugares. No es el Daily Race ni el chip de welcome.",
            },
            {
                "id": "lobby-rainbet-daily-race-2026-09-26",
                "date": "2026-09-26",
                "when": "26 SEP 2026 · Lobby",
                "title": "Daily Race: ventana de 24 h — race por volumen",
                "line": "Página daily-race verificada el 26 SEP 2026. 200 lugares. No publicamos pozo total. No es el chip de bono de la mesa.",
            },
            {
                "id": "bono-rainbet-x40-dual-2026-09-25",
                "date": "2026-09-25",
                "when": "25 SEP 2026 · Bono",
                "title": "Dos caminos de welcome — x40 sobre D+B o unlock sin rollover",
                "line": "Homepage, fetch 25 SEP 2026. Este es el chip de la fila.",
            },
        ],
        "faqs": [
            (
                "¿Rainbet tiene licencia de Argentina?",
                "No. La casa declara licencia de Anjouan en Terms, AML y el footer (revisión de mesa 25 SEP 2026). Eso no es una licencia del registro argentino. El JSON-LD de la homepage nombra RBGAMING N.V., distinto de Rain Group Ltd: no resolvemos una sola razón social.",
            ),
            (
                "¿El bono de la ficha es el Daily Race o el torneo?",
                "No. El chip de la mesa sigue siendo el welcome: x40 sobre depósito+bono, o el camino sin ese rollover. El Daily Race (26 SEP 2026) y el torneo Gates of Olympus 2500 (30 SEP 2026) son señales de lobby.",
            ),
            (
                "¿El depósito es por CBU, como en un casino local?",
                "No. El FAQ declara criptos (incluye USDT) y también bank transfers, cards y gift cards. Un bank transfer en ese texto no es un cajero por CBU de un casino regulado en Argentina. El tiempo de retiro no está adoptado: la frase de 5 a 15 minutos no es un SLA.",
            ),
            (
                "¿Hay enlace de afiliado o código para cargar?",
                "No. El espacio está en la ficha y dice enlace de afiliado no activo. Esta página no abre una puerta de depósito.",
            ),
        ],
    },
    "shuffle": {
        "name": "Shuffle",
        "title": "Shuffle — ficha de la mesa | Planeta Ruleta",
        "description": "Ficha editorial de Shuffle: Natural Nine B.V., licencia de Curaçao declarada, rakeback 5% HE y señales de Level Up. Sin puntaje. +18.",
        "modified": "2026-10-03",
        "lede": [
            "Shuffle está en la mesa como operador crypto/offshore, con licencia de Curaçao publicada a nombre de Natural Nine B.V.",
            "El dato de bono que la fila defiende es rakeback de casino. El Level Up es otra señal, con números aproximados.",
        ],
        "sheet": [
            ("Empresa", "Natural Nine B.V. (160998), Korporaalweg 10, Willemstad. Declarado en /info/license, Terms y homepage."),
            ("Licencia", "Curaçao Gaming Authority, OGL/2024/1337/0628, Natural Nine B.V. (160998). /info/license dice “Gaming Control Board”; Terms y el certificado CGA dicen “Gaming Authority”. Certificado Active. No es licencia de Argentina."),
            ("Monedas", "La celda de métodos es la clase: crypto · fiat/cards. No hay catálogo de monedas ni de redes en la mesa. USDT aparece en el ejemplo de rakeback (1000 USDT), no como lista. Catálogo: no verificado · 03 OCT 2026."),
            ("Idiomas", "no verificado · 03 OCT 2026. Esta ficha está en español de Latinoamérica; eso no dice qué idiomas publica el operador."),
            ("Última revisión", "Rakeback re-verificado 28 SEP 2026. Level Up: 02 OCT 2026. KYC: 25 SEP 2026. Huecos marcados al armar la ficha: 03 OCT 2026."),
        ],
        "fuentes": [
            ("shuffle.com", "https://shuffle.com/"),
            ("Licencia", "https://shuffle.com/info/license"),
            ("Terms", "https://shuffle.com/info/terms"),
            ("Account verification", "https://help.shuffle.com/en/articles/6918878-account-verification"),
            ("Coin-mixing", "https://help.shuffle.com/en/articles/6941286-coin-mixing"),
            ("Rakeback", "https://help.shuffle.com/en/articles/10020509-how-does-rakeback-work"),
            ("Cómo se gana el rakeback", "https://help.shuffle.com/en/articles/10020510-how-do-i-earn-rakeback"),
            ("Level Up", "https://help.shuffle.com/en/articles/8528228-shuffle-level-up-bonus"),
            ("Promo Level Up", "https://shuffle.com/promotions/level-up"),
            (
                "Certificado CGA",
                "https://cert.cga.cw/certificate?id=ZXlKcGRpSTZJazlqWkhKRk1ETnNlVWh1TUVGNlRVZGFjMUpLZDFFOVBTSXNJblpoYkhWbElqb2llbWQ1Y0ROUlRXeE5ZbFp1UzJWM1ZUTlJOelp2VVQwOUlpd2liV0ZqSWpvaVlqWm1NelJrWkRjeE9UWmtOakEwTURJMU9XRXlNVEJtWkdJMU1tTmtZalppWlRNeFpqSmxOMkZqTWpsbU5HSTJOVEprWXpVNVpXRXhPVE5oWWprMk55SXNJblJoWnlJNklpSjk%3D",
            ),
        ],
        "plata_title": "Cómo entra y sale la plata",
        "plata": [
            "La homepage declara depósitos fiat con tarjeta, Apple Pay y Google Pay, vía socios de pago, más la clase crypto. Los Terms hablan de retiros fiat. La celda de la mesa no lista monedas.",
            "USDT está en el ejemplo de rakeback del help (1000 USDT a 2% de house edge → 1 USDT). Eso no es un catálogo de redes.",
            "Antes de retirar hay que apostar 1x el depósito (help de coin-mixing, 28 jul 2026). No hay horas de pago: el retiro de la mesa sigue en sin dato. No es un cajero por CBU de un casino regulado en Argentina.",
        ],
        "bono": [
            "Chip de la fila: rakeback de casino = 5% del house edge, en cash, no en sports, y no es un match de depósito. Ejemplo declarado: apostar 1000 USDT en un juego con 2% de house edge devuelve 1 USDT, se gane o se pierda. Se desbloquea al apostar 1.000 USD en total (Bronze) y se reclama en la página VIP. Help del 21 oct 2024, re-verificado 28 SEP 2026.",
            "Las bases de un FTD con rollover no están publicadas. No inventamos un Nx.",
            "Level Up (02 OCT 2026) es otra señal: al subir de rango se abren Rank Up, Level Up Reload y Recent Play. Los montos del escalón “1” están publicados como aproximados (Silver ≈ 25 USD, Gold ≈ 210 USD, y el resto en la señal). No reemplaza el chip. La promo figura desde el 1 nov 2024 hasta el 2 nov 2026.",
            "Para no leer un rakeback como si fuera un match: guía de cashback, rakeback y lossback, y la guía de cómo leer una promo.",
        ],
        "kyc": "KYC declarado: los Terms pueden exigir pasaporte, DNI o licencia al cruzar un umbral y, en cualquier caso, antes del primer retiro. El help de Account Verification describe niveles: email, datos básicos, ID de gobierno y prueba de domicilio. Fuente: Terms y help, señal del 25 SEP 2026.",
        "offshore": "Shuffle publica OGL/2024/1337/0628 a nombre de Natural Nine B.V. /info/license dice Curaçao Gaming Control Board; Terms y el certificado CGA dicen Curaçao Gaming Authority. Eso no es una licencia de Argentina. Esta ficha no rankea operadores y no explica cómo evadir un bloqueo. +18.",
        "senales": [
            {
                "id": "bono-shuffle-level-up-approx-2026-10-02",
                "date": "2026-10-02",
                "when": "02 OCT 2026 · Bono",
                "title": "Level Up ≠ solo rakeback — paquete aprox",
                "line": "Help y promo oficiales. Números aproximados en el escalón 1. No es el rakeback 5% HE. Peter QC PASS 02 OCT 2026.",
            },
            {
                "id": "bono-shuffle-rakeback-5pct-he-2026-09-25",
                "date": "2026-09-28",
                "when": "28 SEP 2026 · Bono",
                "title": "Rakeback ≠ match: 5% del house edge (Bronze)",
                "line": "Este es el chip de la fila. Cash, casino, no sports. FTD sin bases publicadas.",
            },
            {
                "id": "kyc-shuffle-id-before-wd-2026-09-25",
                "date": "2026-09-25",
                "when": "25 SEP 2026 · KYC",
                "title": "Documento de identidad antes del primer retiro",
                "line": "Terms y help de verificación. Además, 1x del depósito antes de retirar. Sin SLA de horas.",
            },
        ],
        "faqs": [
            (
                "¿El rakeback de Shuffle es un bono de bienvenida con rollover?",
                "No. El help, re-verificado el 28 SEP 2026, dice 5% del house edge en cash, en juegos de casino, no en sports, y no es un depósito match. Las bases de un FTD con rollover no están publicadas.",
            ),
            (
                "¿Level Up reemplaza al chip de la mesa?",
                "No. El Level Up del 02 OCT 2026 es una señal aparte: Rank Up, Level Up Reload y Recent Play, con montos aproximados. El chip de la fila sigue siendo rakeback 5% HE (Bronze).",
            ),
            (
                "¿Cuándo piden documento?",
                "Los Terms dicen que pueden exigir pasaporte, DNI o licencia al cruzar un umbral y, en cualquier caso, antes del primer retiro. El help describe niveles: email, datos básicos, ID de gobierno y prueba de domicilio. Señal del 25 SEP 2026.",
            ),
            (
                "¿La licencia de Curaçao es una licencia argentina?",
                "No. El número es OGL/2024/1337/0628, Natural Nine B.V. /info/license dice Curaçao Gaming Control Board; Terms y el certificado CGA dicen Curaçao Gaming Authority. Offshore no es el registro de Argentina. El enlace de afiliado de esta ficha no está activo. +18.",
            ),
        ],
    },
    "stake": {
        "name": "Stake",
        "title": "Stake — ficha de la mesa | Planeta Ruleta",
        "description": "Ficha editorial de Stake: rakeback 3.5% HE de welcome y licencia citada por certificado CGA. El footer del operador no se capturó (HTTP 403). Sin puntaje. +18.",
        "modified": "2026-10-03",
        "lede": [
            "Stake está en la mesa como operador crypto/offshore.",
            "La licencia que citamos sale de un certificado del Curaçao Gaming Control Board, porque el texto del propio sitio no se pudo leer en el fetch del 25 SEP 2026.",
        ],
        "sheet": [
            ("Empresa", "Medium Rare N.V. (145353), en el certificado CGA de stake.com. No sale de un footer del operador: el fetch de términos devolvió HTTP 403 el 25 SEP 2026."),
            ("Licencia", "Curaçao-class. Certificado CGA OGL/2024/1451/0918, otorgado el 09/06/2025, estado Active. Es certificado del regulador, no una frase leída en el footer de stake.com. No es licencia de Argentina."),
            ("Monedas", "La celda de métodos es la clase: crypto · fiat. No hay catálogo de monedas ni de redes. BTC aparece en el ejemplo de rakeback, no como lista. Catálogo: no verificado · 03 OCT 2026."),
            ("Idiomas", "no verificado · 03 OCT 2026. Esta ficha está en español de Latinoamérica; eso no dice qué idiomas publica el operador."),
            ("Última revisión", "Mesa y señal de welcome: 25 SEP 2026 (help fechado 24 ago 2026). Huecos marcados al armar la ficha: 03 OCT 2026."),
        ],
        "fuentes": [
            ("stake.com", "https://stake.com/"),
            ("Welcome offer", "https://help.stake.com/en/articles/5091363-how-to-get-my-welcome-offer"),
            ("Proof of identity", "https://help.stake.com/en/articles/5886574-proof-of-identity-acceptable-documentation"),
            ("Retiro crypto", "https://help.stake.com/en/articles/5091165-crypto-how-to-make-a-withdrawal"),
            ("Ayuda de retiros crypto", "https://help.stake.com/en/articles/4915741-crypto-help-with-withdrawals"),
            ("Wager crypto", "https://help.stake.com/en/articles/4929043-what-is-a-wager-requirement-for-crypto"),
            ("Wager en moneda local", "https://help.stake.com/en/articles/8226254-is-there-a-wager-requirement-for-local-currencies"),
            ("Deposit bonus", "https://help.stake.com/en/articles/9609744-what-is-a-deposit-bonus-requirement"),
            (
                "Certificado CGA",
                "https://cert.cga.cw/certificate?id=ZXlKcGRpSTZJbkJtT0dKb04zWTRhbmc1VERsd1RXTTRRMjVHZDNjOVBTSXNJblpoYkhWbElqb2lSVEJwU2t0emJYSm9LMUkzYm04NVVqSkZRMnRxZHowOUlpd2liV0ZqSWpvaVpEWm1NV0kwT1dNeE9XVmpaVFkyTnpFd01HVmpPV1V4WmpWaU5qRm1NVEprWXpjd05tTTJaamczWkdNM1pHSXdaVEl6T1RFeVlUSXlOell6TnpJNVpTSXNJblJoWnlJNklpSjk%3D",
            ),
        ],
        "plata_title": "Cómo entra y sale la plata",
        "plata": [
            "El help declara retiros crypto y reglas de apuesta para moneda local / FIAT. La celda de la mesa es crypto · fiat, sin lista de monedas.",
            "BTC está en el ejemplo de rakeback (1 BTC apostado a 2% de house edge → 0,0007 BTC). Eso no es un catálogo de redes.",
            "Antes de retirar hay que apostar el 100% del depósito, en crypto y en moneda local (help del 24 ago 2026). No hay plazo en horas: montos grandes pueden ir a proceso manual y la red tiene sus confirmaciones. El retiro de la mesa sigue en sin dato. No es un cajero por CBU de un casino regulado en Argentina.",
        ],
        "bono": [
            "Chip de la fila: el welcome desbloquea rakeback Bronze, 3.5% del house edge, con un código. No es un match de depósito con rollover fijo. Ejemplo declarado: 1 BTC apostado a 2% de house edge → 0,0007 BTC de rakeback. Help actualizado el 24 ago 2026.",
            "El rollover de un deposit-bonus “varía”. El help da un ejemplo de 30x y no fija un producto de match. No lo copiamos como chip.",
            "No hay señal de race ni de level-up de Stake en la mesa. Para leer rakeback aparte de un match: la guía de cashback, rakeback y lossback.",
        ],
        "kyc": "El help Proof of Identity (24 ago 2026) acepta pasaporte, documento nacional de ambos lados o licencia de ambos lados, fotografiado y con vigencia de al menos 3 meses. En qué momento lo exigen no quedó en ese fetch: no verificado · 25 SEP 2026. Fuente: help.stake.com.",
        "offshore": "La celda dice Curaçao-class porque el certificado CGA de stake.com está Active y el footer del operador no se pudo leer (HTTP 403). Eso no es una licencia de Argentina. Esta ficha no pone nota y no explica cómo evadir un bloqueo. +18.",
        "senales": [
            {
                "id": "bono-stake-rakeback-welcome-2026-09-25",
                "date": "2026-09-25",
                "when": "25 SEP 2026 · Bono",
                "title": "Welcome ≠ match: rakeback 3.5% del house edge vía código",
                "line": "Help oficial, actualizado 24 ago 2026. Este es el chip de la fila. El ejemplo 30x de un deposit-bonus no es un SKU de welcome.",
            },
        ],
        "faqs": [
            (
                "¿El welcome de Stake es un match de depósito?",
                "No, en lo publicado en el help (24 ago 2026; mesa 25 SEP 2026). El welcome desbloquea rakeback Bronze: 3.5% del house edge, con un código. El rollover de un deposit-bonus varía; el help da un ejemplo 30x y no fija un match.",
            ),
            (
                "¿De dónde sale la licencia si el sitio devolvió 403?",
                "Del certificado CGA de stake.com: Medium Rare N.V. (145353), OGL/2024/1451/0918, otorgado el 09/06/2025, estado Active. No es una frase leída en el footer: ese fetch devolvió HTTP 403. Por eso la celda dice Curaçao-class.",
            ),
            (
                "¿Cuándo piden el documento?",
                "El help de Proof of Identity lista pasaporte, documento nacional de ambos lados o licencia de ambos lados, con foto y vigencia de al menos 3 meses (24 ago 2026). En qué momento lo exigen: no verificado · 25 SEP 2026.",
            ),
            (
                "¿Hay plazo de retiro o enlace de afiliado?",
                "No hay horas de pago en la mesa: el retiro sigue en sin dato. Antes de retirar hay que apostar el 100% del depósito (help de crypto y de moneda local, 24 ago 2026). El enlace de afiliado de esta ficha no está activo.",
            ),
        ],
    },
    "cloudbet": {
        "name": "Cloudbet",
        "title": "Cloudbet — ficha de la mesa | Planeta Ruleta",
        "description": "Ficha editorial de Cloudbet: welcome de hasta 2.500 USD en 30 días, rakeback 10% del house edge en casino y licencia CGA OGL/2024/328/0599. Sin puntaje. +18.",
        "modified": "2026-10-03",
        "lede": [
            "Cloudbet está en la mesa como operador crypto/offshore. El help declara licencia de la Curaçao Gaming Authority y un paquete de hasta 2.500 USD en 30 días, con rakeback del 10% en casino.",
            "Esta ficha no pone nota ni abre un depósito. El apex cloudbet.com, el 03 OCT 2026, devolvió el shell de JavaScript; los hechos salen de /en, de los Terms y del help.",
        ],
        "sheet": [
            ("Empresa", "Halcyon Super Holdings B.V. (148526), nombrada en el help de licencias. Domicilio: no verificado · 03 OCT 2026."),
            ("Licencia", "Curaçao Gaming Authority, OGL/2024/328/0599, Halcyon Super Holdings B.V. (148526). Help, 03 OCT 2026. No es licencia de Argentina."),
            ("Monedas", "La celda de la tabla es la clase crypto · buy card (Swapped). El artículo de compra nombra monedas de esa pasarela; no las copiamos como catálogo. Redes: no verificado · 03 OCT 2026."),
            ("Idiomas", "no verificado · 03 OCT 2026. Esta ficha está en español de Latinoamérica; eso no dice qué idiomas publica el operador."),
            ("Última revisión", "Bono, KYC y métodos de la fila: 30 SEP 2026. Licencia y sportsbook: 03 OCT 2026."),
        ],
        "fuentes": [
            ("cloudbet.com/en", "https://www.cloudbet.com/en"),
            ("Sports", "https://www.cloudbet.com/en/sports"),
            ("Terms", "https://www.cloudbet.com/en/help/terms"),
            ("Licencias", "https://www.cloudbet.com/en/support/articles/107963-what-gambling-licenses-does-cloudbet-have"),
            ("Niveles de verificación", "https://www.cloudbet.com/en/support/articles/415596-what-are-cloudbet-s-verification-levels"),
            ("Documentos", "https://www.cloudbet.com/en/support/articles/103148-what-documents-are-accepted-for-account-verification"),
            ("Por qué piden verificar", "https://www.cloudbet.com/en/support/articles/455235-why-am-i-asked-to-verify-my-account"),
            ("Comprar con Swapped", "https://www.cloudbet.com/en/support/articles/324281-how-to-buy-crypto-with-swapped-on-cloudbet"),
        ],
        "plata_title": "Cómo entra y sale la plata",
        "plata": [
            "La celda de métodos es crypto · buy card (Swapped). El help, artículo actualizado el 24 SEP 2026, dice que el depósito con tarjeta pasa por Swapped: se elige depositar con tarjeta y después Swapped.",
            "Ese artículo nombra monedas de la compra. No es un catálogo de la mesa ni una lista de redes. Redes: no verificado · 03 OCT 2026.",
            "El retiro de la fila sigue sin dato. El marketing de velocidad de retiro no entra como SLA. No es un cajero por CBU de un casino regulado en Argentina.",
        ],
        "bono": [
            "Chip de la fila: paquete de bienvenida de hasta 2.500 USD en un programa de 30 días, y 10% del house edge en cada apuesta de casino elegible. Las apuestas de sports no suman rakeback. Terms §8.4, chequeo 03 OCT 2026.",
            "El período de 30 días empieza al hacer la primera apuesta después de ese depósito (§8.4.2), no desde la hora del depósito. No hay un Nx de rollover publicado para este paquete. No inventamos uno.",
            "No hay señal de Cloudbet en el archivo. El chip es el de la fila. Para leer un rakeback aparte de un match: la guía de cashback, rakeback y lossback.",
        ],
        "kyc": "KYC declarado por niveles. Level 2: foto del documento, prueba de domicilio y verificación de rostro. Sumsub está en Terms §21.1.3; el artículo de niveles no lo nombra. El help dice que pueden pedir la verificación en cualquier momento. Los topes de Level 1 están publicados (2.200 USD de depósito de por vida y 2.200 USD de retiro diario) y no están en la celda de la tabla. Un disparador fijo, más allá de “en cualquier momento”: no verificado · 03 OCT 2026. Fuente: help y Terms, 03 OCT 2026.",
        "offshore": "Cloudbet publica Curaçao Gaming Authority, OGL/2024/328/0599, a nombre de Halcyon Super Holdings B.V. (148526). Eso no es una licencia de Argentina. Esta ficha no rankea operadores y no explica cómo evadir un bloqueo. +18.",
        "senales": [],
        "faqs": [
            (
                "¿El bono de Cloudbet es un match con rollover?",
                "No, en lo publicado en Terms §8.4 (03 OCT 2026). Es un paquete de hasta 2.500 USD en 30 días y un rakeback del 10% del house edge en apuestas de casino elegibles. Ese artículo no publica un Nx. Los 30 días empiezan con la primera apuesta después del depósito.",
            ),
            (
                "¿Las apuestas de sports suman rakeback?",
                "No. Terms §8.4 dicen que las apuestas de sports no suman rakeback. El sportsbook sí está declarado: /en/sports, título “Crypto Sports Betting”, 03 OCT 2026.",
            ),
            (
                "¿La licencia de Curaçao es una licencia argentina?",
                "No. El help de licencias nombra Curaçao Gaming Authority, OGL/2024/328/0599, Halcyon Super Holdings B.V. (148526). Offshore no es el registro de Argentina. El enlace de afiliado de esta ficha no está activo. +18.",
            ),
            (
                "¿El depósito es por CBU?",
                "No. La celda es crypto · buy card (Swapped). El help describe la compra con tarjeta a través de Swapped. El retiro de la mesa sigue sin dato: no hay un SLA de horas en esta ficha.",
            ),
        ],
    },
    "roobet": {
        "name": "Roobet",
        "title": "Roobet — ficha de la mesa | Planeta Ruleta",
        "description": "Ficha editorial de Roobet: instant rakeback y boost de +10% por 24 h al registrarse. Licencia y sportsbook público: no verificado. Sin puntaje. +18.",
        "modified": "2026-10-03",
        "lede": [
            "Roobet está en la mesa como operador crypto/offshore. El help declara instant rakeback y, al registrarse, un boost de +10% durante 24 horas.",
            "Esta ficha no pone nota ni abre un depósito. La licencia y el sportsbook del HTML público siguen en no verificado.",
        ],
        "sheet": [
            ("Empresa", "no verificado · 03 OCT 2026. El artículo Welcome no nombra sociedad ni número."),
            ("Licencia", "no verificado · 30 SEP 2026. Rechequeo 03 OCT 2026: el artículo Welcome dice “fully licensed and regulated” y no nombra autoridad ni número. No es licencia de Argentina."),
            ("Monedas", "La celda de la tabla es la clase crypto · fiat+Swapped. El help de depósito nombra criptos; no las copiamos como catálogo. Redes: no verificado · 03 OCT 2026."),
            ("Idiomas", "no verificado · 03 OCT 2026. Esta ficha está en español de Latinoamérica; eso no dice qué idiomas publica el operador."),
            ("Última revisión", "Bono, KYC y métodos de la fila: 30 SEP 2026. Sportsbook y licencia rechequeados el 03 OCT 2026: siguen sin número y sin sportsbook en el HTML público."),
        ],
        "fuentes": [
            ("roobet.com", "https://roobet.com/"),
            ("/sports", "https://roobet.com/sports"),
            ("Rewards", "https://help.roobet.com/en/articles/9546773-rewards-explained"),
            ("Level 2", "https://help.roobet.com/en/articles/14709132-level-2-verification"),
            ("Depósito crypto", "https://help.roobet.com/en/articles/4665363-depositing-to-roobet-using-cryptocurrency"),
            ("Depósito con Swapped", "https://help.roobet.com/en/articles/11979123-how-to-deposit-using-swapped"),
            ("Welcome", "https://help.roobet.com/en/articles/4901197-welcome"),
        ],
        "plata_title": "Cómo entra y sale la plata",
        "plata": [
            "El help declara fiat y crypto, y compra de cripto vía Swapped (tarjeta, Apple Pay y Google Pay). La celda de la mesa se queda en la clase crypto · fiat+Swapped.",
            "El artículo de depósito en cripto nombra un conjunto de monedas. No entra como catálogo de la tabla ni como lista de redes. Redes: no verificado · 03 OCT 2026.",
            "El retiro de la fila sigue sin dato. No es un cajero por CBU de un casino regulado en Argentina.",
        ],
        "bono": [
            "Chip de la fila: Instant rakeback, un porcentaje de lo apostado, reclamable cada 30 minutos y sin vencimiento. Al registrarse hay un boost de +10% durante 24 horas sobre ese rakeback. No es un match de depósito. El artículo no publica un Nx. Help de rewards, rechequeo 03 OCT 2026.",
            "No hay señal de Roobet en el archivo. El chip es el de la fila. Para no leer un rakeback como si fuera un match: la guía de cashback, rakeback y lossback.",
        ],
        "kyc": "KYC declarado en Level 2 (help del 23 jul 2026): pasaporte, licencia de conducir o documento de gobierno, con captura de frente y dorso. Ese artículo no da un umbral. Cuándo lo exigen: no verificado · 03 OCT 2026. Fuente: help.roobet.com.",
        "offshore": "En las páginas chequeadas el 03 OCT 2026 no hay número de licencia ni autoridad. “Fully licensed and regulated” en el artículo Welcome no nombra un registro. Eso no es una licencia de Argentina. El HTML público de roobet.com y de /sports no muestra un sportsbook (cero veces la palabra sport); un sportsbook con sesión iniciada no se chequeó. Esta ficha no rankea operadores y no explica cómo evadir un bloqueo. +18.",
        "senales": [],
        "faqs": [
            (
                "¿El +10% de Roobet es un match de depósito?",
                "No. El help de rewards lo publica como un boost de bienvenida de +10% durante 24 horas sobre el instant rakeback. El instant rakeback es un porcentaje de lo apostado, se reclama cada 30 minutos y no vence. Ese artículo no publica un Nx.",
            ),
            (
                "¿Roobet tiene sportsbook?",
                "En el HTML público de roobet.com y de /sports, el 03 OCT 2026, el título es de casino y no aparece la palabra sport. Un sportsbook con sesión iniciada no se chequeó. La celda queda en no verificado · 03 OCT 2026.",
            ),
            (
                "¿Qué licencia publica?",
                "No verificado. El artículo Welcome dice que es un casino licenciado y regulado, y no nombra autoridad ni número (rechequeo 03 OCT 2026). Eso no es una licencia de Argentina. +18.",
            ),
            (
                "¿Hay enlace de afiliado o depósito por CBU?",
                "No. El espacio de afiliado dice enlace de afiliado no activo. La celda de métodos es crypto · fiat+Swapped, no un cajero por CBU. El retiro de la mesa sigue sin dato.",
            ),
        ],
    },
}


GUIDE_LINKS = """<p>Guías para leer el texto, no para depositar: <a href="/guias/como-leer-una-promo-casino/">cómo leer una promo</a>, <a href="/guias/cashback-rakeback-lossback/">cashback, rakeback y lossback</a>, <a href="/guias/max-bet-contribucion-bono/">max bet y contribución</a>, <a href="/guias/usdt-vs-btc-bankroll/">USDT y BTC en un depósito crypto</a>.</p>"""


def render_ficha(slug: str) -> str:
    data = FICHAS[slug]
    path = f"/mesa/{slug}/"
    url = f"{HOST}{path}"
    title = data["title"]
    description = data["description"]
    faqs = data["faqs"]
    graph = [
        org(),
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "es",
            "isPartOf": {"@type": "WebSite", "@id": f"{HOST}/#website", "name": "Planeta Ruleta", "url": f"{HOST}/"},
            "about": {"@id": ORG_ID},
            "publisher": {"@id": ORG_ID},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "mainEntity": {"@id": f"{url}#article"},
            "dateModified": data["modified"],
        },
        {
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": title,
            "description": description,
            "inLanguage": "es",
            "datePublished": "2026-10-03",
            "dateModified": data["modified"],
            "image": f"{HOST}/logo-saturn.png",
            "author": {"@id": ORG_ID},
            "publisher": {"@id": ORG_ID},
            "mainEntityOfPage": {"@id": f"{url}#webpage"},
        },
        breadcrumb_ld(
            url,
            [("Inicio", f"{HOST}/"), ("Mesa", f"{HOST}/mesa/"), (data["name"], url)],
        ),
        faq_ld(url, faqs),
    ]
    lede = "".join(f'<p class="lede">{e(p)}</p>' for p in data["lede"])
    plata = "".join(f"<p>{e(p)}</p>" for p in data["plata"])
    bono = "".join(f"<p>{e(p)}</p>" for p in data["bono"])
    body = f"""
      {crumbs_html([("Inicio", "/"), ("Mesa", "/mesa/"), (data["name"], None)])}
      <article class="ficha">
        <p class="estado">En la mesa</p>
        <h1>{e(data["name"])}</h1>
        {lede}
        <section class="block" aria-labelledby="declarada">
          <h2 id="declarada">Ficha declarada</h2>
          {sheet_html(data["sheet"])}
          {fuentes_html(data["fuentes"])}
        </section>
        <section class="block" aria-labelledby="plata">
          <h2 id="plata">{e(data["plata_title"])}</h2>
          {plata}
        </section>
        <section class="block" aria-labelledby="bono">
          <h2 id="bono">Bono real y marketing</h2>
          {bono}
          {GUIDE_LINKS}
        </section>
        <section class="block" aria-labelledby="kyc">
          <h2 id="kyc">KYC</h2>
          <p>{e(data["kyc"])}</p>
        </section>
        <aside class="offshore">
          <p>{e(data["offshore"])}</p>
        </aside>
        <section class="block" aria-labelledby="senales">
          <h2 id="senales">Señales de este operador</h2>
          {senales_block(data)}
        </section>
        {affiliate_html()}
        <section class="block" id="faq" aria-labelledby="faq-title">
          <h2 id="faq-title">Preguntas</h2>
          {faq_html(faqs)}
        </section>
      </article>
      <section class="cmp-sec" id="comparacion" aria-labelledby="comparacion-title">
        <h2 id="comparacion-title">Comparación</h2>
        <p class="cmp-note">La misma tabla que en <a href="/mesa/#comparacion">/mesa/</a>. Sin insignia de ganador.</p>
        {compare_table()}
      </section>
      <section class="block" aria-labelledby="otros">
        <h2 id="otros">Otros en la mesa</h2>
        {otros_html(slug)}
        <p class="after"><a href="/mesa/">Todas las fichas</a> · <a href="/#mesa">Tira corta en la home</a></p>
      </section>
"""
    return page(title, description, path, graph, body)


def main() -> None:
    out_index = ROOT / "mesa" / "index.html"
    out_index.parent.mkdir(parents=True, exist_ok=True)
    files = {out_index: render_index()}
    for slug in FICHAS:
        path = ROOT / "mesa" / slug / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        files[path] = render_ficha(slug)
    banned = ("mejor casino", "vpn", "AggregateRating", "noindex", '"@type": "Review"')
    for path, text in files.items():
        low = text.lower()
        for word in banned:
            if word.lower() in low:
                raise SystemExit(f"banned phrase {word!r} in {path}")
        if "Enlace de afiliado no activo." not in text:
            raise SystemExit(f"missing empty affiliate slot in {path}")
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
