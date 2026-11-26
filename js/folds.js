/* Open a server-rendered <details> when a hash targets it or something inside it.
   The folded copy is already in the HTML; this only reveals it. */
(() => {
  const stick = () => {
    const mast = document.querySelector(".mast");
    if (!mast) return;
    const sticky = getComputedStyle(mast).position === "sticky";
    const h = sticky ? Math.ceil(mast.getBoundingClientRect().height) : 0;
    document.documentElement.style.setProperty("--af-stick", h + "px");
  };
  const openFor = () => {
    const raw = location.hash.slice(1);
    if (!raw) return;
    let id = raw;
    try { id = decodeURIComponent(raw); } catch (err) { /* keep the raw hash */ }
    const el = document.getElementById(id);
    if (!el) return;
    let node = el.closest("details");
    while (node) {
      node.open = true;
      node = node.parentElement ? node.parentElement.closest("details") : null;
    }
    el.scrollIntoView();
  };
  stick();
  window.addEventListener("resize", stick);
  window.addEventListener("hashchange", openFor);
  openFor();
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", () => { setTimeout(openFor, 0); });
  });
})();
