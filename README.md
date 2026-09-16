# Planeta Ruleta — main website

Static GitHub Pages site for [www.planetaruleta.com](https://www.planetaruleta.com/). Media/community (not a casino). Primary conversion is Telegram.

Public pages: `/`, `/sobre/`, `/faq/`, `/como-funciona/`. Canonical host is **www**.

## Analytics (GA4) — for Aviv

Measurement ID is set in [`js/config.js`](js/config.js):

```js
window.PR_GA_MEASUREMENT_ID = "G-VMKXD8779P";
```

Merge so GitHub Pages deploys. **gtag.js** loads with that ID (empty / `G-XXXXXXXXXX` would skip loading). Confirm in GA4 **Reports → Realtime** (open the site, then click **Sumate al canal**). You should see `page_view` and `cta_telegram_click`.

Events we send (nothing else):

| Event | When | Params |
| --- | --- | --- |
| `page_view` | automatic from gtag | standard |
| `cta_telegram_click` | click on Telegram / join CTAs | `cta_location` (`hero`, `bottom`, `nav`, `contact`, `faq`), `link_url` |

To use those params in standard reports: **Admin → Custom definitions → Create custom dimension** (event-scoped) for `cta_location` and, if you want it, `link_url`.

Optional: in the data stream, under **Enhanced measurement**, you can turn **Outbound clicks** off so Telegram isn’t double-counted (our custom event already covers it).

No ads pixels, no user IDs, no PII in events.

## Google Search Console

1. Add the **www** property: `https://www.planetaruleta.com/` ([Search Console](https://search.google.com/search-console)).
2. Verify with any one method:

   | Method | What to do |
   | --- | --- |
   | **HTML file** (simplest on GitHub Pages) | Download Google’s `google*.html` file, commit it at the **repo root**, merge, then click Verify. |
   | **HTML tag** | Paste the `content` token into `window.PR_GOOGLE_SITE_VERIFICATION` in [`js/config.js`](js/config.js). Empty = the meta tag is omitted. Google’s verifier often reads raw HTML and may **not** run JS — if the tag method fails, use the HTML file or DNS. You can also paste the meta tag into each page `<head>`. |
   | **DNS TXT** | Add the TXT record Google shows at your domain DNS (covers www and apex if you use a Domain property). |

3. After verification: **Sitemaps → Add** `https://www.planetaruleta.com/sitemap.xml`.
4. Request indexing for the homepage if you want it in sooner (**URL inspection → Request indexing**).

`robots.txt` allows crawl (`Allow: /`) and points at that sitemap. Public pages have **no** `noindex` meta.

## Crawl files

- [`robots.txt`](robots.txt) — allow all, sitemap URL
- [`sitemap.xml`](sitemap.xml) — the four live public paths, absolute `https://www.planetaruleta.com/` URLs
