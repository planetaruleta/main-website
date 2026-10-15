# EDCOMP gate · Ficha edits 15 OCT 2026 · Shuffle ARS + Rainbet Anjouan line
**Input:** Analyst daily-2026-10-15 C1/I1 (INT S11, R13). **Evidence:** `docs/org/intel/evidence/2026-10-15/edcomp-recheck/` (fetch-log.tsv, MD5SUMS). Live ficha text: `pr-shuffle-text.txt`, `pr-rainbet-text.txt` (planetaruleta.com, 07:00:41–42 IL).

## VERDICT: PASS WITH CHANGES (both edits). Analyst's "VALID on the register" is narrowed (see §2).

## 1. Shuffle accepts ARS
Source: https://help.shuffle.com/en/articles/17596504 · title "How to Deposit and Withdraw with Mercado Pago, NaranjaX and Instant Bank Transfer" · dateModified 2026-10-14T09:25:38Z (= 14 OCT 12:25 IL) · fetched **15 OCT 06:59:39 IL**, HTTP 200.
Exact lines:
- "you deposit, play, and withdraw in ARS with no crypto conversion at any stage."
- Table: Methods: Deposit "Instant Bank Transfer, Mercado Pago, NaranjaX" / Withdrawal "Bank Transfer (CBU/CVU)"; Min "7,500 ARS" / "7,500 ARS"; Max "7,500,000 ARS" / "7,500,000 ARS"; Shuffle fee "None" / "None"; processing "Nearly instant".
- "Send from an account registered under your own CUIT/CUIL."
- "Enter your withdrawal amount along with your 22-digit CBU or CVU. Aliases aren't accepted for withdrawals." "The CBU or CVU must be registered under your own CUIT/CUIL, the same one linked to your Shuffle account."
- "No. Shuffle doesn't charge for ARS deposits or withdrawals."
- "What you'll need: A clear copy of a valid photo ID… Get verified today so your payouts are complete…"
→ **Deposits AND withdrawals.** Deposits: Mercado Pago, NaranjaX, instant bank transfer (to a CBU/CVU or alias shown per deposit). Withdrawals: bank transfer only, to your own 22-digit CBU/CVU (no alias). Help-only source (not on homepage/terms yet): label OFICIAL (help), date it, recheck before ship.

### Shuffle edits (live string → replacement, voseo ES-AR)
| # | Where | Before | After |
|---|---|---|---|
| S1 | «Cómo entra y sale la plata» card, Depósito | `Crypto + fiat` / `tarjeta · Apple Pay · Google Pay` | `Crypto + fiat` / `ARS: Mercado Pago · NaranjaX · transferencia · tarjeta · Apple Pay · Google Pay` |
| S2 | Same card, footer line | `No es un cajero por CBU.` | `Pesos por CBU/CVU ≠ casino regulado en Argentina.` |
| S3 | New paragraph right after «La homepage declara depósitos fiat…» | (none) | `Pesos (ARS): según el artículo de ayuda de Shuffle sobre Mercado Pago, NaranjaX y transferencia (actualizado el 14 OCT 2026, revisado el 15 OCT 2026), depositás en ARS por transferencia inmediata, Mercado Pago o NaranjaX al CBU/CVU o alias que te muestran en cada depósito, y retirás solo por transferencia a un CBU o CVU de 22 dígitos (sin alias) a tu nombre, con el mismo CUIT/CUIL de tu cuenta. Mínimo 7.500 ARS y máximo 7.500.000 ARS por operación, en los dos sentidos. Según ese artículo, Shuffle no cobra comisión por depositar ni retirar en ARS. Antes de cobrar te piden un documento con foto. «Casi instantáneo» es lo que dice la ayuda, no un plazo. Que acepte pesos no cambia la licencia: sigue siendo Curaçao, no una licencia de Argentina. Fuente: oficial (ayuda de Shuffle).` |
| S4 | Paragraph «Antes de retirar…», last sentence | `No es un cajero por CBU de un casino regulado en Argentina.` | `Que el pago en pesos pase por CBU/CVU no lo convierte en un casino regulado en Argentina.` |
| S5 | Comparison cell, Shuffle «Criptos / redes» | `Clase: crypto · fiat/cards. Lista y redes: no verificado · 03 OCT 2026. USDT solo en el ejemplo de rakeback.` | `Clase: crypto · fiat/cards · ARS (Mercado Pago, NaranjaX, transferencia; ayuda 14 OCT 2026). Lista y redes: no verificado · 03 OCT 2026. USDT solo en el ejemplo de rakeback.` |
Why: the old «No es un cajero por CBU» is now false for ARS (H6). CUIT/CUIL framed as a condition, not a selling point. No «legal», «seguro», «ya se puede» (H12). No CTA, no link (H9). Licence line «CGA · OGL/2024/1337/0628» unchanged and stays next to the ARS mention.

## 2. Rainbet Anjouan line
Live checks (15 OCT, IL):
- **Seal validator** (Analyst's URL with `seal_id`/`stamp`, verification.anjouangamingboard.org) · 06:59:48 · HTTP 200: "Company name Rain Group Ltd · Registered Website(s) rainbet.com · Operating status: VALID · …License No. ALSI-152406029-FI2, issued by the Offshore Finance Authority of the State of Anjouan…". **Banner on the same page:** "This seal validation page has expired since it was generated on: Jun 11, 2025… If the issue persists after refresh, it is an indication of possible misuse or attempted fraud." No issue/expiry dates.
- **Same validator, domain only (no seal params)** · 06:59:40 · HTTP 200: "rainbet.com · Operating status: INVALID · …NOT Licensed…". Likely the validator needs the seal params, but it's unresolved.
- **Public register** (anjouangaming.com/public-register/verify-a-licence/, the "Official Public Register" the validator points to) · 06:59:53 · HTTP 200 but search is client-side; no result retrievable by curl. **GAP.**
- **Entity match:** rainbet.com/terms (06:59:31): "Rain Group Ltd, a limited liability company registered in Anjouan with company registration number 16077 … licensed in Anjouan for the provision of online games of chance." Footer (home + terms): "Rain Group Ltd. Company Address: Hamchako, Mustamudu…". ✓ matches the validator's "Rain Group Ltd". Home JSON-LD/marketing text still says "RBGAMING N.V." (existing ficha line covers this). 16077 = company registration number, not licence number ✓.
→ "VALID on the register" is overstated. It's VALID on the seal-validator page, under an expired-seal warning, not confirmed on the public register. Wording must say exactly that (H6/H8).

### Rainbet edits
| # | Where | Before | After |
|---|---|---|---|
| R1 | Anexo «Licencia.» | `Anjouan, declarada en Terms, AML y footer (25 SEP 2026). El validador de Anjouan no se chequeó. No es una licencia del registro argentino.` | `Anjouan, declarada en Terms, AML y footer (25 SEP 2026). El validador del sello de Anjouan muestra «VALID» para Rain Group Ltd, licencia ALSI-152406029-FI2 (consulta del 15 OCT 2026), aunque la misma página avisa que el sello está vencido desde junio de 2025. No lo pudimos confirmar en el registro público de Anjouan. No es una licencia del registro argentino.` |
| R2 | Comparison cell «Licencia», Rainbet | `Anjouan, declarada en Terms, AML y footer (25 SEP 2026). Validador no chequeado.` | `Anjouan, declarada en Terms, AML y footer (25 SEP 2026). Validador del sello: «VALID», Rain Group Ltd, ALSI-152406029-FI2 (15 OCT 2026), con aviso de sello vencido. Registro público: sin confirmar.` |
No «legal en Argentina», «segura», «licencia válida» as our conclusion (H12); «VALID» is quoted as the page's status. Excluded territories list includes Spain (H1 n/a for us). Upgrade R1/R2 to «registro público: VALID» only after someone captures a public-register result (browser).

## Do not
- Do not add a link to the validator or Shuffle help on the ficha beyond the existing «Fuentes» pattern.
- Shuffle ARS is 1 day old and help-only: recheck 17596504 on the PR day; if it's gone or changes, back to me.
