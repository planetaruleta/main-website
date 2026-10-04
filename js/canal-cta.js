/**
 * Planeta Ruleta — soft canal CTA href.
 * Reads window.SITE_CTA_TG_URL from config.js and points a[data-site-cta-tg]
 * at it. Static HTML already links https://t.me/planetaruleta so the path
 * exists without JS. Only https://t.me/ and https://telegram.me/ are applied.
 */
(function () {
  "use strict";

  var raw = String(window.SITE_CTA_TG_URL || "").trim();
  if (!raw) return;

  var url;
  try {
    url = new URL(raw);
  } catch (err) {
    return;
  }
  if (url.protocol !== "https:") return;
  if (url.username || url.password) return;
  if (url.hostname !== "t.me" && url.hostname !== "telegram.me") return;

  var links = document.querySelectorAll("a[data-site-cta-tg]");
  for (var i = 0; i < links.length; i++) {
    links[i].href = url.href;
  }
})();
