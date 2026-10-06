/**
 * Planeta Ruleta — GA4 (page_view), Telegram CTA clicks, outbound clicks.
 * Reads window.PR_GA_MEASUREMENT_ID / PR_GOOGLE_SITE_VERIFICATION from config.js.
 * No marketing pixels. No PII in events. Does not add affiliate or UTM params.
 *
 * Events:
 * - page_view (gtag)
 * - cta_telegram_click (cta_location, link_url)
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

  document.addEventListener("click", function (event) {
    var target = event.target;
    if (!target || typeof target.closest !== "function") return;
    var link = target.closest("a[href]");
    if (!link) return;

    if (link.getAttribute("data-cta") === "telegram") {
      var location = (link.getAttribute("data-cta-location") || "unknown").trim() || "unknown";
      gtag("event", "cta_telegram_click", {
        cta_location: location,
        link_url: link.href || "",
      });
      return;
    }

    var outbound = outboundParams(link);
    if (!outbound) return;
    gtag("event", "outbound_click", outbound);
  });
})();
