/**
 * Planeta Ruleta — public site config (safe to commit; no secrets).
 *
 * 1. GA4: Admin → Data streams → your Web stream → Measurement ID (G-…).
 *    Real ID is set below. analytics.js will not load gtag.js for empty /
 *    G-XXXXXXXXXX placeholders.
 *
 * 2. Google Search Console HTML-tag verification (optional):
 *    paste only the content= token, not the whole meta tag.
 *    Empty = omit. HTML file or DNS TXT is more reliable on GitHub Pages;
 *    see README.
 */
window.PR_GA_MEASUREMENT_ID = "G-VMKXD8779P";
window.PR_GOOGLE_SITE_VERIFICATION = "";
