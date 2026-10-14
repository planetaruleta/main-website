# EDCOMP GATE · Guía A2 «RTP y ventaja de la casa en ruleta» · 14 Oct 2026
**Draft:** docs/drafts/guias/a2-rtp-ventaja-ruleta-2026-10-14.md · **Slug:** /guias/rtp-ventaja-casa-ruleta/
**Gated:** 14 Oct 2026 ~11:55 IL · Source: docs/org/intel/a2-house-edge-2026-10-14.md · raw evidence `docs/org/intel/evidence/2026-10-14/a2-house-edge/` (captured 11:42–11:43 IL, SHA256SUMS all OK).

## VERDICT: PASS WITH CHANGES (1 × P1, 3 × P2)

## Fixes
**G1 · P1 · Dead link dependency (H6 / site QA).** Item 5 links to A1's slug, which doesn't exist until A1 merges. Option A (preferred): merge A1 first (or in the same PR) and keep the line unchanged. Option B, if A2 ships first:
Before: `5. **Retirar también tiene condiciones.** Algunas salas piden apostar el depósito antes de retirarlo: [/guias/antes-de-retirar-rollover-kyc/](/guias/antes-de-retirar-rollover-kyc/).`
After: (line deleted; re-add it verbatim once A1 is live)

**G2 · P2 · Rainbet «Max» interpreted (H6/H8).** The page doesn't explain «Max», so we shouldn't explain it for them.
Before: `Fijate que dice «Max»: es un tope, no necesariamente el de cada apuesta.`
After: `Fijate que dice «Max» y la página no explica a qué apuesta o variante se refiere.`

**G3 · P2 · Roobet absence overclaim (H6).** We only know we didn't find a figure when signed out, not that none is published.
Before: `- **Roobet:** cifra no publicada sin iniciar sesión.`
After: `- **Roobet:** sin iniciar sesión, no encontramos la cifra en la página del juego ni en su ayuda.`

**G4 · P2 · Number format consistency (ES-AR).** The prose is fine (2,70 %, 97,30 %). The English quotes keep the operator's point because they're verbatim, which is OK, but say so once so it doesn't read as a typo.
Before: `Las cifras pueden cambiar. Revisá la ficha del juego en la web oficial antes de decidir.`
After: `Las citas entre comillas van tal cual las publica cada sala (con punto decimal). Las cifras pueden cambiar. Revisá la ficha del juego en la web oficial antes de decidir.`

## Raw-evidence verification (not just the intel summary)
| Claim | Raw | Result |
|---|---|---|
| Shuffle «2.70% fixed house edge» | shuffle-roulette.txt L77 | MATCH |
| Shuffle European → RTP 97.30 % | L162 «The European roulette structure provides an RTP of 97.30%, leaving a 2.70% house edge.» | MATCH; «Originals» confirmed at L69 |
| Rainbet «Max RTP 97.30 %» | rainbet-roulette.txt L51–53 | MATCH; grep for european/american/french/single-zero = 0 hits → the draft's «no dice si la rueda es…» is correct, and there's no «Rainbet = europea» overclaim ✓ |
| Cloudbet conflict, no figures | intel table (eu-joy 97.3 vs 97; am-joy 94.7 vs 97) | ✓ no figures cited |
| Stake unreadable | stake-roulette.txt = Cloudflare «Just a moment...» block page | MATCH; the 2% help example was cut ✓ |
| Roobet | roobet-roulette.txt / roobet-help.txt: 0 hits for rtp or house edge | MATCH → wording G3 |
| 1÷37 = 0,0270… ≈ 2,70 % · 2÷38 = 0,0526… ≈ 5,26 % | recomputed | ✓, labelled EDITORIAL «matemática de manual» |
| «casi duplica» | 5,26 ÷ 2,70 = 1,95 | ✓ EDITORIAL |

## Checklist
- H4 ✓ RTP is «teórico… en el largo plazo»; «por qué ese promedio no es tu resultado de esta noche»; «Ningún número de esta guía predice tu sesión».
- H5 ✓ no income framing. H8 ✓ no «mejor sala» or ranking. Shuffle «coincide con el cálculo» is factual, and nothing implies that higher RTP means winning.
- H9 ✓ internal links only, no codes. H10 ✓ «Stake» with no stake.bet.ar reference or link. H12 ✓ none. H1/H2/H3/H7/H11 ✓.
- Cuts honoured: no Evolution French Gold, no Stake 2%, no payout ratios.
- Sources dated ✓ «revisado 14 oct 2026» on §3. Meta title/description ✓ scoped (names only Shuffle and Rainbet, «alfabetización», +18).
- RG ✓ A1 G1 line verbatim; +18 ✓ ×4.
- Register ✓ voseo consistent (querés, fijate, leé, revisá, preguntate, estás, cancelás, pará, buscá); no tú/usted mixing.
- Facts table: strip before publish.

No re-gate needed if G1–G4 are applied verbatim (G1 by either option).
