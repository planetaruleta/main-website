/**
 * Planeta Ruleta — GA4 (page_view) + Telegram CTA clicks.
 * Reads window.PR_GA_MEASUREMENT_ID / PR_GOOGLE_SITE_VERIFICATION from config.js.
 * No marketing pixels. No PII in events.
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

  document.addEventListener("click", function (event) {
    var target = event.target;
    if (!target || typeof target.closest !== "function") return;
    var link = target.closest('a[data-cta="telegram"]');
    if (!link) return;

    var location = (link.getAttribute("data-cta-location") || "unknown").trim() || "unknown";
    gtag("event", "cta_telegram_click", {
      cta_location: location,
      link_url: link.href || "",
    });
  });
})();
