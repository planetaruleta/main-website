/**
 * Planeta Ruleta — GA4 (page_view), Telegram CTA clicks, outbound clicks.
 * Reads window.PR_GA_MEASUREMENT_ID / PR_GOOGLE_SITE_VERIFICATION from config.js.
 * No marketing pixels. No PII in events. Does not add affiliate or UTM params.
 *
 * Events:
 * - page_view (gtag)
 * - cta_telegram_click (cta_location, placement, link_url, cta_page_path) on every
 *   t.me / telegram.me link, tagged or not; sent with beacon transport
 * - outbound_click (link_url, link_domain, optional link_context from data-link-context)
 *
 * Readable source. Public pages load /js/analytics.min.js — keep that file in sync.
 */
(function () {
  "use strict";

  var measurementId = String(window.PR_GA_MEASUREMENT_ID || "").trim();
  var siteVerification = String(window.PR_GOOGLE_SITE_VERIFICATION || "").trim();

  if (siteVerification) {
    var existing = document.querySelector('meta[name="google-site-verification"]');
    if (!existing) {
      var meta = document.createElement("meta");
      meta.setAttribute("name", "google-site-verification");
      meta.setAttribute("content", siteVerification);
      document.head.appendChild(meta);
    }
  }

  function isUsableMeasurementId(id) {
    if (!id) return false;
    if (/^G-X+$/i.test(id)) return false;
    if (/^G-YOUR/i.test(id)) return false;
    return /^G-[A-Z0-9]+$/i.test(id);
  }

  if (!isUsableMeasurementId(measurementId)) {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  gtag("js", new Date());
  gtag("config", measurementId);

  var gtagScript = document.createElement("script");
  gtagScript.async = true;
  gtagScript.src =
    "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
  document.head.appendChild(gtagScript);

  function hostIs(host, name) {
    return host === name || host.slice(-(name.length + 1)) === "." + name;
  }

  function isInternalHost(host) {
    var here = String(window.location.hostname || "").toLowerCase();
    if (host === here) return true;
    return hostIs(host, "planetaruleta.com");
  }

  function isTelegramHost(host) {
    return hostIs(host, "t.me") || hostIs(host, "telegram.me") || hostIs(host, "telegram.org");
  }

  // http(s) link that leaves this site. Telegram CTAs stay on cta_telegram_click.
  function outboundParams(link) {
    if (!link || link.getAttribute("data-cta") === "telegram") return null;

    var raw = String(link.getAttribute("href") || "").trim();
    if (!raw || raw.charAt(0) === "#") return null;

    var url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (err) {
      return null;
    }
    if (url.protocol !== "http:" && url.protocol !== "https:") return null;

    var host = String(url.hostname || "").toLowerCase();
    if (!host || isInternalHost(host) || isTelegramHost(host)) return null;

    var params = {
      link_url: link.href,
      link_domain: host,
      // Not a reported dimension. Lets a same-tab leave still send the hit.
      transport_type: "beacon",
    };
    var context = String(link.getAttribute("data-link-context") || "").trim();
    if (context) params.link_context = context;
    return params;
  }

  // Telegram link: tagged CTA, or any anchor that points at t.me / telegram.me.
  function telegramParams(link) {
    var tagged = link.getAttribute("data-cta") === "telegram";
    var host = "";
    try {
      host = String(new URL(link.href, window.location.href).hostname || "").toLowerCase();
    } catch (err) {
      host = "";
    }
    if (!tagged && !(host && isTelegramHost(host))) return null;

    var placement = (link.getAttribute("data-cta-location") || "unknown").trim() || "unknown";
    return {
      cta_location: placement,
      placement: placement,
      link_url: link.href || "",
      // page_path is a reserved gtag field (sent as the built-in Page path, dp),
      // so keep an explicit copy as an event parameter too.
      cta_page_path: window.location.pathname || "/",
      // Not a reported dimension. Sends the hit even if the page is left right away.
      transport_type: "beacon",
    };
  }

  function onLinkActivate(event) {
    // Left click, or middle click (auxclick) that opens a new tab.
    if (event.type === "auxclick" && event.button !== 1) return;
    var target = event.target;
    if (!target || typeof target.closest !== "function") return;
    var link = target.closest("a[href]");
    if (!link) return;

    var telegram = telegramParams(link);
    if (telegram) {
      gtag("event", "cta_telegram_click", telegram);
      return;
    }

    var outbound = outboundParams(link);
    if (!outbound) return;
    gtag("event", "outbound_click", outbound);
  }

  // Capture phase so a handler that stops propagation cannot swallow the event.
  document.addEventListener("click", onLinkActivate, true);
  document.addEventListener("auxclick", onLinkActivate, true);
})();
