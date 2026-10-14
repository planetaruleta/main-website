# EDCOMP gate · Rainbet ficha caveat (/mesa/rainbet/) · 14 Oct 2026

**Owner:** Editorial & Compliance QA · **Trigger:** Peter decision 14 Oct (Analyst daily-2026-10-14 C1 / O3) · **Status:** gated, ready for Ops PR

## 1. Verdict
**PASS WITH CHANGES** to the Analyst's draft (final text in §2). The ficha also needs 3 line edits (§3).
**Blocker for Ops:** the site source repo is not on the box. Only the live render (`docs/org/operators/_sources/2026-10-08/site-live-rainbet.txt`) and stale 6 Oct render scripts (`/workspace/mesa-verify/render-mesa-fichas-v2.py` L482) exist. Ops must find the strings in §3 in the real source. Anchor on the exact text, not line numbers.

## 2. Final caveat (Spanish, voseo to match the ficha: «Deslizá», «Sumate»; ES-AR; no links)
Placement: directly under the "Bono real vs marketing" block (Camino A / Camino B cards).

> **Rainbet publica dos versiones (rechequeo 14 OCT 2026).** Camino B: la homepage y su página «Promotions Terms and Conditions» muestran dos caminos de welcome (x40 y «No Wager Lock»); el artículo de ayuda «First Deposit Promotion» dice que hay uno solo, el x40. Apuesta máxima con el bono activo: «Promotions Terms and Conditions» y la homepage dicen 2% del depósito; el artículo de ayuda «Deposit Bonus Terms and Conditions» dice 1%. No sabemos cuál aplica a tu cuenta. Antes de depositar, revisá los T&C vigentes y lo que te muestre tu pestaña de promociones. Fuente: oficial (páginas de Rainbet).

Label: OFICIAL (both sides are operator pages; we only report the conflict, not which is right).

## 3. Ficha edits (exact before → after)
Live page text from `site-live-rainbet.txt` (8 Oct capture; Analyst live re-check 14 Oct confirms the same strings). Source file in repo: UNKNOWN (see blocker).

| # | Where | Before | After |
|---|---|---|---|
| E1 | Camino A card | `Apuesta máxima 2% del depósito` | `Apuesta máxima 2% del depósito según T&C · la ayuda dice 1%` |
| E2 | Camino B card, first line | `Camino B 0×` | `Camino B 0× · la ayuda de Rainbet no lo menciona` |
| E3 | New block after the Camino B card | (none) | the §2 caveat verbatim |
| (ref) | Stale render script `/workspace/mesa-verify/render-mesa-fichas-v2.py` L482 (and `render-mesa-fichas.py` L468) | `apuesta máxima 2% del depósito,` | `apuesta máxima 2% del depósito según T&C (la ayuda dice 1%),` (only if this script is still the generator) |

Not changed: the FAQ «o el camino sin ese rollover» and the comparison cell «o camino sin ese rollover». The caveat covers them. Ops can optionally append « (ver aviso: la ayuda muestra un solo camino)», which is pre-approved.
The /senales/ 25 SEP señal «dos caminos» is out of scope (it's a dated observation, which is still true for the homepage). Flag it to Peter if he wants it to cover that too.

## 4. Sources
| Claim | URL | Exact wording | Section | Checked | Evidence |
|---|---|---|---|---|---|
| 2 paths (home) | https://rainbet.com/ | "Welcome bonuses on Rainbet come in two paths" | L147 home text | 14 Oct 06:39 IL | `intel/evidence/2026-10-14/rainbet-path-b/home-text.txt` (INT P1) |
| 2 paths (T&C) | https://rainbet.com/deposit-promotion-terms | sections "Wager Lock Promotion" + "No Wager Lock Promotion" | no clause numbers on page | 14 Oct 06:39 IL | `.../deposit-promotion-terms-text.txt` L37, L55 (INT P2) |
| 2 paths (API) | api.rainbet.com/promotions/list | `wager-locked-1`, `no-wager-lock-1` | n/a | 14 Oct 06:39 IL | `.../api-promotions-list.json` (INT P3) |
| 1 path (help) | https://help.rainbet.com/en/articles/15268657-first-deposit-promotion | "Rainbet has one first-deposit promotion: the 40x Wager Locked bonus" | dateModified 01 Sep 2026 16:44 IL | 14 Oct 06:39 IL | `.../help-15268657-ftd.html` (INT P4) |
| Max bet 2% (T&C) | https://rainbet.com/deposit-promotion-terms | "Max bet when active is 2% of deposit amount." | Wager Lock Promotion, no number | 14 Oct 06:39 IL | `.../deposit-promotion-terms-text.txt` L41 |
| Max bet 2% (home) | https://rainbet.com/ | "Max bet 2% of the deposit while the promotion is active" | L155 | 14 Oct 06:39 IL | `.../home-text.txt` L155 |
| Max bet 1% (help) | https://help.rainbet.com/en/articles/9831951-deposit-bonus-terms-and-conditions | "Bets with a rollover is capped at a maximum of 1% of deposit amount per bet unless stated otherwise." | dateModified 01 Sep 2026 16:14 IL | 14 Oct 06:39 IL | `.../help-9831951-deposit-bonus-terms-text.txt` L30 (INT P5) |
| No help article on No Wager Lock | help search | 0 results | n/a | 14 Oct 06:39 IL | INT P6 |

"Path B" = Rainbet's "No Wager Lock" welcome (unlock = wager × 1% × 20%), our «Camino B 0×». Background: `intel/pending/done/rainbet-path-b-2026-10-08.md`.

## 5. Analyst draft → final
Draft: *"Rainbet publica dos versiones: la home y los T&C muestran dos caminos y apuesta máx. 2%; su centro de ayuda muestra solo el x40 y apuesta máx. 1%. Confirmá en tu pestaña de promociones antes de depositar."*

| Change | Why |
|---|---|
| Added «(rechequeo 14 OCT 2026)» | H6: perishable fact needs a date folio |
| «su centro de ayuda» → the two named help articles | Brief: name both sources. These are two different articles (15268657 = paths, 9831951 = 1%) |
| «los T&C» → «su página "Promotions Terms and Conditions"» | It's the page's real title. It has no § numbers, so none is cited |
| «apuesta máx.» → «Apuesta máxima con el bono activo» | Scope fidelity: both sources limit it to while the promo/rollover is active |
| Added «No sabemos cuál aplica a tu cuenta.» | H12: no conclusion on which is right |
| «Confirmá en tu pestaña de promociones» → «revisá los T&C vigentes y lo que te muestre tu pestaña de promociones» | Point to the binding doc plus the account view. Voseo kept (matches the ficha) |
| Added «Fuente: oficial (páginas de Rainbet).» | Claim label. No link added (H9; the ficha's Fuentes list already links rainbet.com/Terms) |
| No accusatory verb (no «se contradice», «engaña») | H8 |

Checks: H6 ✓ all figures sourced · H8 ✓ · H9 ✓ no new links · H12 ✓ · register ✓ voseo, consistent · format ✓ «2%» matches the existing ficha style.
