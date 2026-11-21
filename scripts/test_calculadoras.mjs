#!/usr/bin/env node
// Checks the math in js/calculadoras.js against hand-computed cases.
// Usage: node scripts/test_calculadoras.mjs
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const C = require("../js/calculadoras.js");

let fails = 0, n = 0;
function eq(name, got, want, tol = 1e-9) {
  n++;
  const ok = typeof want === "number" ? Math.abs(got - want) <= tol : got === want;
  if (!ok) fails++;
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}: got ${got}, want ${want}`);
}

// Formato y lectura
eq("format 1234567.891", C.formatNumero(1234567.891), "1.234.567,89");
eq("format 25.92", C.formatNumero(25.92), "25,92");
eq("format -40", C.formatNumero(-40), "−40,00");
eq("format 0.135 (3 dec)", C.formatNumero(0.135, 3), "0,135");
eq("format -0.001 -> 0,00 sin signo", C.formatNumero(-0.001), "0,00");
eq("parse '2,70'", C.parseNumero("2,70"), 2.7);
eq("parse '1.000'", C.parseNumero("1.000"), 1000);
eq("parse '1.234,56'", C.parseNumero("1.234,56"), 1234.56);
eq("parse '2.7'", C.parseNumero("2.7"), 2.7);
eq("parse '5 %'", C.parseNumero("5 %"), 5);
eq("parse 'abc' is NaN", Number.isNaN(C.parseNumero("abc")), true);

// Rakeback vs cashback — R1: ejemplo de la guía (1.000, 2,70 %, 4 % de la ventaja, cashback 5 %)
let r = C.rakebackVsCashback({ volumen: 1000, ventaja: 2.7, rakebackPct: 4, baseRakeback: "ventaja", cashbackPct: 5, topeCashback: 0 });
eq("R1 pérdida esperada", r.perdidaEsperada, 27);
eq("R1 rakeback", r.rakeback, 1.08);
eq("R1 cashback", r.cashback, 1.35);
eq("R1 costo con rakeback", r.costoConRakeback, 25.92);
eq("R1 costo con cashback", r.costoConCashback, 25.65);
eq("R1 equilibrio (r = c)", r.equilibrioRakebackPct, 5);
// R2: rakeback sobre lo apostado 0,1 %, cashback 5 %, ruleta europea
r = C.rakebackVsCashback({ volumen: 1000, ventaja: 2.7, rakebackPct: 0.1, baseRakeback: "apostado", cashbackPct: 5, topeCashback: 0 });
eq("R2 rakeback sobre apostado", r.rakeback, 1);
eq("R2 equilibrio (c × h) = 0,135 %", r.equilibrioRakebackPct, 0.135);
// R3: tope de cashback
r = C.rakebackVsCashback({ volumen: 10000, ventaja: 5.26, rakebackPct: 10, baseRakeback: "ventaja", cashbackPct: 10, topeCashback: 20 });
eq("R3 pérdida esperada", r.perdidaEsperada, 526);
eq("R3 cashback con tope", r.cashback, 20);
eq("R3 tope aplicado", r.cashbackTopeAplicado, true);
eq("R3 rakeback", r.rakeback, 52.6);
// R4: igualdad r = c sobre la ventaja
r = C.rakebackVsCashback({ volumen: 2500, ventaja: 4, rakebackPct: 7, baseRakeback: "ventaja", cashbackPct: 7, topeCashback: 0 });
eq("R4 diferencia cero", r.diferencia, 0);
// R5: volumen cero
r = C.rakebackVsCashback({ volumen: 0, ventaja: 2.7, rakebackPct: 4, baseRakeback: "ventaja", cashbackPct: 5, topeCashback: 0 });
eq("R5 todo cero", r.perdidaEsperada + r.rakeback + r.cashback, 0);

// Rollover — W1: 100, x35 sobre bono, 4 %
let w = C.rolloverBono({ bono: 100, deposito: 100, base: "bono", multiplo: 35, contribucion: 100, ventaja: 4 });
eq("W1 requisito", w.requisito, 3500);
eq("W1 apuesta real", w.apuestaReal, 3500);
eq("W1 pérdida esperada", w.perdidaEsperada, 140);
eq("W1 valor neto", w.valorNeto, -40);
eq("W1 ventaja de equilibrio", w.ventajaEquilibrioPct, 100 / 35);
// W2: bono + depósito
w = C.rolloverBono({ bono: 100, deposito: 100, base: "bono-deposito", multiplo: 35, contribucion: 100, ventaja: 4 });
eq("W2 requisito", w.requisito, 7000);
eq("W2 pérdida esperada", w.perdidaEsperada, 280);
eq("W2 valor neto", w.valorNeto, -180);
// W3: ruleta con contribución 10 %
w = C.rolloverBono({ bono: 100, deposito: 0, base: "bono", multiplo: 35, contribucion: 10, ventaja: 2.7 });
eq("W3 apuesta real", w.apuestaReal, 35000, 1e-6);
eq("W3 pérdida esperada", w.perdidaEsperada, 945, 1e-6);
eq("W3 valor neto", w.valorNeto, -845, 1e-6);
eq("W3 veces el bono", w.vecesBono, 350, 1e-9);
// W4: valor neto positivo con rollover bajo (x10, 2,70 %)
w = C.rolloverBono({ bono: 50, deposito: 0, base: "bono", multiplo: 10, contribucion: 100, ventaja: 2.7 });
eq("W4 pérdida esperada", w.perdidaEsperada, 13.5, 1e-9);
eq("W4 valor neto", w.valorNeto, 36.5, 1e-9);
// W5: equilibrio exacto (x25 a 4 % -> pérdida = bono)
w = C.rolloverBono({ bono: 200, deposito: 0, base: "bono", multiplo: 25, contribucion: 100, ventaja: 4 });
eq("W5 valor neto cero", w.valorNeto, 0, 1e-9);
eq("W5 ventaja de equilibrio 4 %", w.ventajaEquilibrioPct, 4, 1e-9);

console.log(`\n${n - fails}/${n} passed`);
process.exit(fails ? 1 : 0);
