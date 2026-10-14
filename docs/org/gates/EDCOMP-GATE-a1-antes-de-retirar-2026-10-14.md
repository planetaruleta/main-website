# EDCOMP GATE · Guía A1 «Antes de retirar» · 14 Oct 2026
**Draft:** docs/drafts/guias/a1-antes-de-retirar-2026-10-14.md · **Slug:** /guias/antes-de-retirar-rollover-kyc/
**Gated:** 14 Oct 2026 ~11:50 IL (Ed&Comp QA) · Sources: ep04-FACTS-LEDGER.md, EDCOMP-GATE-EP04-2026-10-08 (C1–C12), EDCOMP-REGATE-EP04-2026-10-14 (X1–X4), EDCOMP-rainbet-ficha-caveat-2026-10-14, raw evidence re-read.

## VERDICT: PASS WITH CHANGES (2 × P1, 3 × P2)

## Fixes
**G1 · P1 · RG line missing (C9 / rulebook §3.2).** Closing paragraph has generic RG only.
Before: `+18. Jugá con responsabilidad: si el juego deja de ser entretenimiento, pará y pedí ayuda.`
After: `+18. Si estás persiguiendo pérdidas, o cancelás un retiro para seguir jugando, pará y buscá ayuda.`

**G2 · P1 · Meta description overclaim (H6/X1).** It says we report what Stake and Roobet *terms* say; their terms were unreadable (8 & 14 Oct), and most Stake/Roobet/Cloudbet claims are from help pages/homes.
Before: `Qué dicen los términos de Rainbet, Shuffle, Cloudbet, Stake y Roobet sobre apostar el depósito y verificar identidad antes de retirar. Alfabetización, no consejo de apuesta. +18.`
After: `Qué dicen las páginas oficiales de Rainbet, Shuffle, Cloudbet, Stake y Roobet sobre apostar el depósito y verificar identidad antes de retirar. Alfabetización, no consejo de apuesta. +18.`

**G3 · P2 · Meta title / H1 scope (H6).** «según los términos» → «según las páginas oficiales».
Before (meta title): `Antes de retirar: rollover del depósito y KYC según los términos — Planeta Ruleta`
After: `Antes de retirar: rollover del depósito y KYC según las páginas oficiales — Planeta Ruleta`
Before (H1): `# Antes de retirar: rollover del depósito y verificación KYC, según los términos`
After: `# Antes de retirar: rollover del depósito y verificación KYC, según las páginas oficiales`

**G4 · P2 · Rainbet terms «no plazo» scope (H6/H8).** §20.1 does state 24hrs for KYC document review; make clear the absence is about withdrawal processing.
Before: `sus términos no dan plazo de procesamiento de retiros.`
After: `sus términos no dan plazo de procesamiento de retiros (el «24hrs» de §20.1 es para revisar documentos de KYC, ver arriba).`

**G5 · P2 · Facts table (internal) line ref.** Cloudbet home 90 % <2 min is at L18 of the 14 Oct capture, not L17 (file captured 14 Oct 06:39 IL). Also ledger F4 still says "not re-fetched 14 Oct"; the 14 Oct capture exists, so Content Director should update F4's row.
Before: `evidence/2026-10-14/cloudbet/home-en-text.txt` L17` → After: `… L18`.

## Checklist
| Check | Result |
|---|---|
| Stake/Roobet terms unreadable, no claims on them (X1, H6) | ✓ body; meta → G2 |
| §8.2 direction (X2) | ✓ verbatim X2 wording; matches LIVE terms L113 |
| Rainbet 24hrs vs 7 días hábiles (X3) | ✓ both as written, «no explica cómo se combinan», no pick (H12) |
| Cloudbet estimate | ✓ «es una estimación, no una garantía»; §7.5.11 matches 14 Oct terms-text L136–140 |
| «confiscation of funds» attributed | ✓ quoted + «Palabras de Rainbet» (H8); LIVE L186 byte-match |
| Rainbet max bet 2 % vs 1 % | N/A — not stated; links to bono guide. If added, use caveat wording. |
| USD | ✓ «Montos en dólares estadounidenses (USD)»; 15 USD, 2.200 USD |
| No absolute «ninguno de los cinco» | ✓ absent |
| RG + +18 | +18 ✓ ×4; RG → G1 |
| H2 KYC evasion | ✓ none; guide pushes verifying, own-name payment |
| H12 legal conclusions | ✓ none («a su criterio» is Rainbet's) |
| H9 links/codes | ✓ internal links only |
| H1/H3/H4/H5/H7/H10/H11 | ✓ |
| ES-AR numbers | ✓ 2.200, «90 %», «100 %» |
| Dates per source | ✓ every bullet dated; consistent with ledger (Stake 8 oct; Roobet 8 y 14; Rainbet/Shuffle §7.2 14 oct; Cloudbet help 8 oct) |
| Register | ✓ voseo consistent throughout (tenés, leé, pasás, mirá, recordá, revisá, jugá); no tú/usted mixing. Voseo OK for site (OPEN; matches /guias/). |

Evidence spot-checks (re-read 14 Oct ~11:50 IL): Rainbet LIVE terms L113 (§8.2), L115 (§8.4), L186 (§20.1), home L105 (min $15 + commission line w/o promo condition); Cloudbet 14 Oct home-en L18, terms L136–140, help-wd-limit «$2,200 USD». All MATCH.

Next: CD applies G1–G2 (mandatory), G3–G5 recommended → Ops PR → Aviv's OK. Facts table must be stripped before publish. No re-gate needed if applied verbatim.
