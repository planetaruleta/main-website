/**
 * Planeta Ruleta — calculadoras (rakeback vs cashback, rollover de bono).
 * Pure client-side math. No network calls, no storage, no analytics events
 * beyond the site's existing GA4 page_view. Numbers in and out use Spanish
 * format (coma decimal, punto de miles).
 *
 * The math functions are pure and are also exported for Node so
 * scripts/test_calculadoras.mjs can check them.
 */
(function (root) {
  "use strict";

  /* ---------- Formato y lectura de números (es) ---------- */

  function parseNumero(raw) {
    var s = String(raw == null ? "" : raw).trim().replace(/\s+/g, "").replace(/%$/, "");
    if (s === "") return NaN;
    if (s.indexOf(",") !== -1) {
      // 1.234,56 -> 1234.56
      s = s.replace(/\./g, "").replace(",", ".");
    } else if (/^-?\d{1,3}(\.\d{3})+$/.test(s)) {
      // 10.000 -> 10000 (punto de miles sin decimales)
      s = s.replace(/\./g, "");
    }
    if (!/^-?\d*(\.\d+)?$/.test(s) || s === "" || s === "-") return NaN;
    return Number(s);
  }

  function formatNumero(n, dec) {
    if (typeof n !== "number" || !isFinite(n)) return "—";
    var d = typeof dec === "number" ? dec : 2;
    var neg = n < 0;
    var fixed = Math.abs(n).toFixed(d);
    var parts = fixed.split(".");
    var ent = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    var out = parts.length > 1 ? ent + "," + parts[1] : ent;
    if (neg && Number(fixed) !== 0) out = "−" + out;
    return out;
  }

  /* ---------- Rakeback vs cashback ---------- */
  /**
   * volumen: total apostado en la ventana
   * ventaja: ventaja de la casa en % (2,70 = 2,70 %)
   * rakebackPct: % de rakeback
   * baseRakeback: "ventaja" (% de la ventaja de la casa) | "apostado" (% de lo apostado)
   * cashbackPct: % de cashback sobre la pérdida neta
   * topeCashback: tope de cashback por ventana (0 o vacío = sin tope)
   */
  function rakebackVsCashback(p) {
    var V = p.volumen, h = p.ventaja / 100, r = p.rakebackPct / 100, c = p.cashbackPct / 100;
    var tope = p.topeCashback > 0 ? p.topeCashback : 0;
    var perdidaEsperada = V * h;
    var rakeback = p.baseRakeback === "apostado" ? V * r : perdidaEsperada * r;
    var cashbackSinTope = perdidaEsperada * c;
    var cashback = tope ? Math.min(cashbackSinTope, tope) : cashbackSinTope;
    // Punto de equilibrio: % de rakeback que iguala al cashback (sin tope)
    var equilibrio = p.baseRakeback === "apostado" ? c * h * 100 : c * 100;
    return {
      perdidaEsperada: perdidaEsperada,
      rakeback: rakeback,
      cashback: cashback,
      cashbackTopeAplicado: !!(tope && cashbackSinTope > tope),
      costoConRakeback: perdidaEsperada - rakeback,
      costoConCashback: perdidaEsperada - cashback,
      diferencia: rakeback - cashback,
      equilibrioRakebackPct: equilibrio
    };
  }

  /* ---------- Rollover de bono ---------- */
  /**
   * bono: monto del bono
   * deposito: monto del depósito (solo cuenta si base = "bono-deposito")
   * base: "bono" | "bono-deposito"
   * multiplo: rollover en veces (35 = x35)
   * contribucion: % que aporta el juego al rollover (100 = cuenta todo)
   * ventaja: ventaja de la casa del juego en %
   */
  function rolloverBono(p) {
    var baseMonto = p.base === "bono-deposito" ? p.bono + p.deposito : p.bono;
    var requisito = baseMonto * p.multiplo;
    var k = p.contribucion / 100;
    var apuestaReal = k > 0 ? requisito / k : Infinity;
    var h = p.ventaja / 100;
    var perdidaEsperada = apuestaReal * h;
    var valorNeto = p.bono - perdidaEsperada;
    var ventajaEquilibrio = apuestaReal > 0 && isFinite(apuestaReal) ? (p.bono / apuestaReal) * 100 : NaN;
    return {
      baseMonto: baseMonto,
      requisito: requisito,
      apuestaReal: apuestaReal,
      vecesBono: p.bono > 0 ? apuestaReal / p.bono : NaN,
      perdidaEsperada: perdidaEsperada,
      valorNeto: valorNeto,
      ventajaEquilibrioPct: ventajaEquilibrio
    };
  }

  var api = {
    parseNumero: parseNumero,
    formatNumero: formatNumero,
    rakebackVsCashback: rakebackVsCashback,
    rolloverBono: rolloverBono
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
  root.PRCalc = api;

  /* ---------- Conexión con el formulario ---------- */
  if (typeof document === "undefined") return;

  function leer(form, name) {
    var el = form.elements[name];
    return el ? parseNumero(el.value) : NaN;
  }
  function valor(form, name) {
    var el = form.elements[name];
    return el ? el.value : "";
  }
  function pintar(scope, key, text) {
    var el = scope.querySelector('[data-out="' + key + '"]');
    if (el) el.textContent = text;
  }
  function error(scope, msg) {
    var el = scope.querySelector("[data-calc-error]");
    if (!el) return;
    el.textContent = msg || "";
    el.hidden = !msg;
  }

  function wireRakeback(form) {
    var scope = form.closest("[data-calc-scope]") || form;
    function run() {
      var p = {
        volumen: leer(form, "volumen"),
        ventaja: leer(form, "ventaja"),
        rakebackPct: leer(form, "rakeback"),
        baseRakeback: valor(form, "base_rakeback"),
        cashbackPct: leer(form, "cashback"),
        topeCashback: valor(form, "tope") === "" ? 0 : leer(form, "tope")
      };
      var bad = [p.volumen, p.ventaja, p.rakebackPct, p.cashbackPct, p.topeCashback].some(function (x) { return !isFinite(x) || x < 0; });
      if (bad || p.ventaja > 100 || p.rakebackPct > 100 || p.cashbackPct > 100) {
        error(scope, "Revisa los datos: usa números positivos, con coma decimal (por ejemplo 2,70). Los porcentajes van de 0 a 100.");
        return;
      }
      error(scope, "");
      var r = rakebackVsCashback(p);
      pintar(scope, "perdida", formatNumero(r.perdidaEsperada));
      pintar(scope, "rakeback", formatNumero(r.rakeback));
      pintar(scope, "cashback", formatNumero(r.cashback) + (r.cashbackTopeAplicado ? " (tope)" : ""));
      pintar(scope, "costo-rakeback", formatNumero(r.costoConRakeback));
      pintar(scope, "costo-cashback", formatNumero(r.costoConCashback));
      var dif = r.diferencia;
      var lectura;
      if (Math.abs(dif) < 0.005) lectura = "Con estos datos, el rakeback iguala a la cifra de cashback de esta cuenta.";
      else if (dif > 0) lectura = "Con estos datos, el rakeback devuelve " + formatNumero(dif) + " más que la cifra de cashback de esta cuenta.";
      else lectura = "Con estos datos, la cifra de cashback de esta cuenta supera al rakeback en " + formatNumero(-dif) + ".";
      lectura += p.topeCashback > 0 ? " Con tope, la cifra del cashback ya no es un piso: el promedio real puede quedar por debajo, porque en las ventanas con pérdidas grandes el tope corta la devolución y en las ganadoras no hay devolución." : " La cifra del cashback es un piso: sin tope y pagado en cash, el promedio real suele ser mayor, según la varianza de tus apuestas.";
      if (r.costoConRakeback > 0) lectura += " Con el rakeback, el costo esperado sigue siendo positivo: no vuelve la ventaja a tu favor.";
      else lectura += " Si el costo esperado con rakeback sale cero o negativo, revisa que el porcentaje y la base sean los que dicen los términos y si se paga en cash o en bono: la cuenta no modela niveles, exclusiones ni requisitos de apuesta.";
      pintar(scope, "lectura", lectura);
      pintar(scope, "equilibrio", formatNumero(r.equilibrioRakebackPct, r.equilibrioRakebackPct < 1 ? 3 : 2) + " %");
    }
    form.addEventListener("input", run);
    form.addEventListener("change", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  }

  function wireRollover(form) {
    var scope = form.closest("[data-calc-scope]") || form;
    function run() {
      var p = {
        bono: leer(form, "bono"),
        deposito: valor(form, "deposito") === "" ? 0 : leer(form, "deposito"),
        base: valor(form, "base"),
        multiplo: leer(form, "multiplo"),
        contribucion: leer(form, "contribucion"),
        ventaja: leer(form, "ventaja")
      };
      var bad = [p.bono, p.deposito, p.multiplo, p.contribucion, p.ventaja].some(function (x) { return !isFinite(x) || x < 0; });
      if (bad || p.contribucion <= 0 || p.contribucion > 100 || p.ventaja > 100) {
        error(scope, "Revisa los datos: usa números positivos, con coma decimal. La contribución va de 0 (sin incluir) a 100 y la ventaja de la casa, de 0 a 100.");
        return;
      }
      error(scope, "");
      var r = rolloverBono(p);
      pintar(scope, "requisito", formatNumero(r.requisito));
      pintar(scope, "apuesta", formatNumero(r.apuestaReal));
      pintar(scope, "veces", isFinite(r.vecesBono) ? formatNumero(r.vecesBono, 1) + " veces el bono" : "—");
      pintar(scope, "perdida", formatNumero(r.perdidaEsperada));
      pintar(scope, "valor", formatNumero(r.valorNeto));
      pintar(scope, "equilibrio", isFinite(r.ventajaEquilibrioPct) ? formatNumero(r.ventajaEquilibrioPct) + " %" : "—");
      var lectura;
      if (Math.abs(r.valorNeto) < 0.005) lectura = "Con estos datos, el valor esperado del bono es cero: lo que se espera perder al cumplir el rollover iguala al bono.";
      else if (r.valorNeto < 0) lectura = "Con estos datos, cumplir el rollover cuesta en promedio más que el bono: el valor esperado es negativo.";
      else lectura = "Con estos datos, el valor esperado sale positivo, pero es un promedio teórico bajo los supuestos de abajo, no un resultado: puedes perder el depósito antes de terminar el rollover. Antes de fiarte de la cifra, revisa en los términos la contribución real de ese juego (los juegos de mesa suelen aportar menos que los slots), el max bet, el plazo y el máximo retirable: los términos pueden cambiar.";
      pintar(scope, "lectura", lectura);
    }
    form.addEventListener("input", run);
    form.addEventListener("change", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  }

  function init() {
    var a = document.querySelectorAll('form[data-calc="rakeback-cashback"]');
    for (var i = 0; i < a.length; i++) wireRakeback(a[i]);
    var b = document.querySelectorAll('form[data-calc="rollover"]');
    for (var j = 0; j < b.length; j++) wireRollover(b[j]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})(typeof window !== "undefined" ? window : globalThis);
