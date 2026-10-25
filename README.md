# Planeta Ruleta — main website

**Publicly indexable** as of 25 Sep 2026. Aviv authorized go-index after the first offshore juice (Rainbet + Stake) shipped. Public pages omit a robots meta tag. Do not add `noindex`.

Static GitHub Pages site for [www.planetaruleta.com](https://www.planetaruleta.com/). Media and community, not a casino. Primary conversion is Telegram ([t.me/planetaruleta](https://t.me/planetaruleta)); the site supports the channel and does not replace it.

Public pages: `/`, `/senales/`, `/sobre/`, `/faq/`, `/como-funciona/`, `/guias/` and five literacy guides (`rtp-volatilidad`, `max-bet-contribucion-bono`, `cashback-rakeback-lossback`, `como-leer-una-promo-casino`, `usdt-vs-btc-bankroll`), plus fichas at `/mesa/`, `/mesa/rainbet/`, `/mesa/shuffle/`, `/mesa/stake/`, `/mesa/cloudbet/`, `/mesa/roobet/` and `/mesa/duelbits/`. Canonical host is **www**. The homepage is the Copper Desk pattern in Ocean slate: wordmark masthead, a still R-01 hero, señales, the offshore mesa (Rainbet, Shuffle, Stake, then Cloudbet, Roobet and Duelbits), pull quote, Telegram band. Those rows come from [`content/intel/homepage-offshore-wave1-2026-09-25.json`](content/intel/homepage-offshore-wave1-2026-09-25.json). `sheet_ready` stays false: no `/casinos/` play pages and no affiliate URL. Nav **Mesa** goes to `/mesa/`. The homepage `#mesa` strip stays; all six operator names link to their ficha. Ficha copy is rendered by [`scripts/render-mesa-fichas.py`](scripts/render-mesa-fichas.py). The strip shows Operador, KYC, Bono, and Métodos, with one line above the table: Actualizado · SEP 2026. Métodos cells on the strip are the payment class only (no coin list). Ámbito and Retiro stay in the JSON and are not strip columns. Retiro is deferred until there is a real SLA. Primary CTA label is **Súmate al canal**. The ficha affiliate slot is present and empty. Age language stays in the legal footer. The hero wheel is a still image until Creative ships real layered assets.

The homepage señales block is capped at the latest 3 that are still live. [`content/senales.json`](content/senales.json) is the public feed (the copy that ships). [`scripts/render_senales.py`](scripts/render_senales.py) sorts that list newest-first — same-day rows keep file order — and writes the first 3 non-expired rows into the homepage and the full list into `/senales/`. A row with `ends_at` closes when that UTC timestamp has passed; `expired: true` publishes the closed state before then. Closed rows stay in the archive with an EXPIRADA badge and do not count toward the homepage. The /senales/ JSON-LD ItemList omits them and numbers the remaining positions from 1. Operator names in that render link to `/mesa/[slug]/` when a ficha exists (Rainbet, Shuffle, Stake, Cloudbet, Roobet, Duelbits). A kicker that names two of those operators is left as text, with no single-operator ficha link. Cloudbet (Monster Mash) and Roobet (Heat Check) are in the feed as of 22 OCT 2026 and do not replace the mesa chips. It also checks that every ready id in the intel pack matches the feed, including `ends_at`. Re-run the script after editing the feed. The hero “Última señal” chip stays hand-set and has to match the newest live fecha. `/senales/` is not in the nav or the footer; the homepage line “Ver todas las señales” is the way in.

## Preview local

From the repo root:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`. Inner pages: `/senales/`, `/mesa/`, `/sobre/`, `/faq/`, `/como-funciona/`, `/guias/`.

Confirm the raw HTML of each public page has no `name="robots"` meta (no `noindex`).

## Crawl

`robots.txt` allows fetch (`User-agent: *` / `Allow: /`) and points at `sitemap.xml`. Leave the Search Console verification file in place.

## Analytics (GA4) — for Aviv

Measurement ID is set in [`js/config.js`](js/config.js):

```js
window.PR_GA_MEASUREMENT_ID = "G-VMKXD8779P";
```

**gtag.js** loads with that ID (empty / `G-XXXXXXXXXX` would skip loading). Confirm in GA4 **Reports → Realtime** (open the site, then click **Súmate al canal**). You should see `page_view` and `cta_telegram_click`. On a ficha, click an operator or source link (for example `help.rainbet.com`) and you should see `outbound_click` with `link_domain`. A Telegram CTA does not also fire `outbound_click`. **Admin → DebugView** shows those parameters (GA Debugger extension, or `debug_mode` on the hit).

Events we send (nothing else):

| Event | When | Params |
| --- | --- | --- |
| `page_view` | automatic from gtag | standard |
| `cta_telegram_click` | click on Telegram / join CTAs | `cta_location` (`hero`, `band`, `nav`, `footer`, `bottom`, `contact`, `faq`, `guia`, `guia-canal`, `mesa-canal`; `unknown` for an untagged t.me link), `placement` (same value), `link_url`, `cta_page_path`. Sent with beacon transport, on click and middle-click, for every `t.me` / `telegram.me` link even without `data-cta` |
| `outbound_click` | click on an http(s) link that leaves planetaruleta.com (operator sites, help articles, other sources) | `link_url` (full href), `link_domain` (hostname). `link_context` only when the anchor already has `data-link-context` |

Same-origin and relative links, `mailto:`, `tel:`, and bare `#` hashes are ignored. Telegram (`data-cta="telegram"`, or a `t.me` / `telegram.me` / `telegram.org` host) stays on `cta_telegram_click` only. Nothing is appended to the href.

The soft canal block on `/guias/` (`guia-canal`) and `/mesa/` index plus fichas (`mesa-canal`) uses [`js/config.js`](js/config.js) `SITE_CTA_TG_URL` (`https://t.me/+ijyhpAPYO5Q5ZDFk`, Telegram label `site-cta`). [`js/canal-cta.js`](js/canal-cta.js) rewrites `a[data-site-cta-tg]` after the block is in the document. The HTML href stays `https://t.me/planetaruleta` as the no-JS fallback. The block is literacy, not an affiliate door. The ficha affiliate slot stays “Enlace de afiliado no activo.” Nav and footer Telegram links stay on the public channel.

To use those params in standard reports: **Admin → Custom definitions → Create custom dimension** (event-scoped) for `cta_location`, `link_domain`, and, if you want the full address, `link_url`. GA4 keeps parameter values up to 100 characters, so a long article URL can be cut off; `link_domain` stays whole.

Optional: in the data stream, under **Enhanced measurement**, you can turn **Outbound clicks** off so Telegram and these source links aren’t double-counted (our custom events already cover them).

No ads pixels, no user IDs, no PII in events.

## Google Search Console

Verification can stay (HTML file at the repo root, and the token in [`js/config.js`](js/config.js)). Pages no longer send `noindex,nofollow`.
