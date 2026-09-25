# Planeta Ruleta — main website

**Publicly indexable** as of 25 Sep 2026. Aviv authorized go-index after the first offshore juice (Rainbet + Stake) shipped. Public pages omit a robots meta tag. Do not add `noindex`.

Static GitHub Pages site for [www.planetaruleta.com](https://www.planetaruleta.com/). Media and community, not a casino. Primary conversion is Telegram ([t.me/planetaruleta](https://t.me/planetaruleta)); the site supports the channel and does not replace it.

Public pages: `/`, `/sobre/`, `/faq/`, `/como-funciona/`. Canonical host is **www**. The homepage is the Copper Desk pattern in Ocean slate: wordmark masthead, a still R-01 hero, señales, the offshore Wave 1 mesa (Rainbet, Shuffle, Stake), pull quote, Telegram band. Those rows come from [`content/intel/homepage-offshore-wave1-2026-09-25.json`](content/intel/homepage-offshore-wave1-2026-09-25.json). `sheet_ready` is false: no `/casinos/` pages; operator names link only to the official site. The mesa shows Operador, KYC, Bono, and Métodos, with one line above the table: Actualizado · SEP 2026. Métodos cells are the payment class only (no coin list). Ámbito and Retiro stay in the JSON and are not table columns. Retiro is deferred until there is a real SLA. Primary CTA label is **Sumate al canal**. Age language stays in the legal footer. The hero wheel is a still image until Creative ships real layered assets.

## Preview local

From the repo root:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`. Inner pages: `/sobre/`, `/faq/`, `/como-funciona/`.

Confirm the raw HTML of each public page has no `name="robots"` meta (no `noindex`).

## Crawl

`robots.txt` allows fetch (`User-agent: *` / `Allow: /`) and points at `sitemap.xml`. Leave the Search Console verification file in place.

## Analytics (GA4) — for Aviv

Measurement ID is set in [`js/config.js`](js/config.js):

```js
window.PR_GA_MEASUREMENT_ID = "G-VMKXD8779P";
```

**gtag.js** loads with that ID (empty / `G-XXXXXXXXXX` would skip loading). Confirm in GA4 **Reports → Realtime** (open the site, then click **Sumate al canal**). You should see `page_view` and `cta_telegram_click`.

Events we send (nothing else):

| Event | When | Params |
| --- | --- | --- |
| `page_view` | automatic from gtag | standard |
| `cta_telegram_click` | click on Telegram / join CTAs | `cta_location` (`hero`, `band`, `nav`, `footer`, `bottom`, `contact`, `faq`), `link_url` |

To use those params in standard reports: **Admin → Custom definitions → Create custom dimension** (event-scoped) for `cta_location` and, if you want it, `link_url`.

Optional: in the data stream, under **Enhanced measurement**, you can turn **Outbound clicks** off so Telegram isn’t double-counted (our custom event already covers it).

No ads pixels, no user IDs, no PII in events.

## Google Search Console

Verification can stay (HTML file at the repo root, and the token in [`js/config.js`](js/config.js)). Pages no longer send `noindex,nofollow`.
