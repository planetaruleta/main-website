# EDCOMP gate · Fichas: pagos en moneda local LatAm · 15 OCT 2026
**Trigger:** Peter. **Source:** Intelligence `docs/org/intel/latam-fiat-2026-10-15.md` (raw: `evidence/2026-10-15/latam-fiat/`, captured 08:14–08:16 IL).
**My live re-curl:** `docs/org/intel/evidence/2026-10-15/edcomp-latam-fiat/` (`fetch-log.tsv`, `MD5SUMS`; help pages and live fichas, 08:18:03–08:18:13 IL, all HTTP 200).
**Live ficha strings:** planetaruleta.com/mesa/{stake,rainbet,roobet,cloudbet,shuffle}/ (curl 08:18:08–13 IL; `pr-*-text.txt`).

## VERDICT: PASS WITH CHANGES. Use the replacement blocks below, not Intelligence's 5×5 table wording. Two Intelligence claims are cut and one is corrected (§1).

## 1. Intelligence claims: verdict
| # | Claim | Verdict | Basis |
|---|---|---|---|
| I1 | Stake CLP · Visa deposit and withdrawal · 5,000–1,000,000 · Mastercard X · back to the same card · up to 3 business days | **HOLDS** | help 8222435 (24 Aug 2026) L81–85, help 13903305 (22 Aug 2026) L51–57, L70–74; live re-curl 08:18:03 |
| I2 | Stake MXN / ARS (and CLP) "listed as local currency" | **CUT as a payment claim** | help 9895505 is a *betting-limits* table for Stake Originals («when using local currencies»). It names no payment method, so it doesn't show you can pay in MXN/ARS. Ficha says «no encontramos un método» for MX/AR. |
| I3 | Rainbet AstroPay withdrawal in AR, CL, CO, MX · min $50 · 0.5% · Peru absent | **HOLDS, extended** | help 15254950 (29 May 2026) L41–47; live 08:18:04 shows the same list. The list also has **Ecuador and Uruguay**, which Intelligence's table left out. «$50» carries no currency code, so we say that. |
| I4 | Roobet AR Bank Transfer · DNI · up to 1 h · currency/limits not stated | **HOLDS** | help 11541692 (18 Jun 2025) L37–43; live 08:18:05 |
| I5 | Roobet 1% fee on all successful fiat deposits; 2% per fiat withdrawal from the 10th in 30 days | **HOLDS (exact text below)** | T&C 9.7, 10.8 in the headless capture `render-roobet-com-terms-and-conditions-text.txt` (Intel, 08:16). My curl of /terms-and-conditions (08:18:06) is a JS shell with no text, so this rests on Intel's rendered capture (**flag: not re-verified by me**). 10.8 says «including the tenth withdrawal». |
| I6 | Roobet game-provider geo-blocks name AR, CL, CO, PE | **HOLDS, extended** | help 6610575 (1 Sep 2026); live 08:18:05. Mexico (11 hits), Ecuador, Uruguay and Brazil appear too. Per provider/game, not per account; Argentina sometimes only by province. |
| I7 | Roobet account-level restricted list: no MX/CL/CO/PE/AR; Nicaragua listed | **HOLDS** | help 13686927 (25 Aug 2026) L33 |
| I8 | Roobet AstroPay cash withdrawal by phone (no country list) | **HOLDS** | help 6053949 (24 Jul 2026) L34–40; live 08:18:06 |
| I9 | Roobet bank-account deposit 6391955 (min $10, National ID) | **CUT from ficha** | The example bank is Brazilian («Caixa»), and the article says options «vary by location». It names no Spanish-speaking LatAm country. |
| I10 | **Cloudbet "crypto-only"** | **CORRECTED** | Help 103244 lists only cryptocurrencies, but **T&C §7.3.1 says "…and in fiat currency (each depending on your jurisdiction and the payment methods available to you)"** (Intel capture L106). The live ficha also has card purchase via Swapped. So: no local LatAm method found. Never call it «solo cripto». |
| I11 | Shuffle: no MX/CL/CO/PE article; ARS only; ToS 8.3 names no LatAm country | **HOLDS** | help searches 08:14; ToS 8.3 L145. Shuffle also has a BRL/PIX article (help 17333109, prior capture). |
| I12 | Restricted-country clauses (Shuffle 8.3, Rainbet §4.1.3, Cloudbet §7.1.3) name no MX/CL/CO/PE/AR | **HOLDS, internal only** | We don't publish «tu país está permitido»: an absence in a list isn't a permission (H12). Not in ficha copy. |
| I13 | Stake terms | **unreadable** (403 / Cloudflare) | Ficha says so. |

Summary-only items: none in the replacement copy. Every line below is traced to a raw help/T&C capture.

## 2. Shared style rules applied
- Every payment line: operator page + its date + «revisada el 15 OCT 2026».
- Order: country by country (México · Chile · Colombia · Perú · Argentina, plus other countries the source names).
- Per operator, closing line: «Pagar en moneda local no es una licencia local.»
- Card line «Offshore no es un casino regulado en Argentina.» → «Offshore no es un casino regulado en tu país.» (Stake, Roobet, Cloudbet, Shuffle; Rainbet uses its own string, R2).
- No «legal en», «habilitado en», «disponible en tu país» (H12). Geo-blocks only in the operator's own terms; no workaround (H2). Fees quoted, never compared (no «la más barata»).

## 3. Replacement blocks (live string → replacement; voseo, ES-AR)

### STAKE (/mesa/stake/) · Stake.com only (H10)
| # | Before (live) | After |
|---|---|---|
| ST1 | card Depósito: `Crypto + fiat` / `sin lista de monedas` | `Crypto + fiat` / `Chile: CLP con Visa` |
| ST2 | `No es un cajero por CBU.` | `Moneda local ≠ licencia local.` |
| ST3 | `Offshore no es un casino regulado en Argentina.` | `Offshore no es un casino regulado en tu país.` |
| ST4 | new paragraph after «El help declara retiros crypto y reglas de apuesta para moneda local / FIAT…» | `Moneda local, país por país (ayuda de Stake.com: artículos de depósito y de retiro con tarjeta, del 24 y el 22 AGO 2026, revisados el 15 OCT 2026). Chile: pesos chilenos (CLP) con Visa, para depositar y para retirar, de 5.000 a 1.000.000 CLP por operación; Mastercard no figura para Chile. El retiro vuelve solo a la tarjeta con la que depositaste y, según la ayuda, puede tardar hasta 3 días hábiles en llegar a tu banco. La opción aparece solo si está disponible para tu moneda y tu ubicación. México, Colombia, Perú y Argentina: no encontramos un método de pago en moneda local en la ayuda (búsqueda del 15 OCT 2026). La misma tabla lista otras monedas de la región: Costa Rica, Guatemala, Honduras, Jamaica, Nicaragua, Trinidad y Tobago, y dólares en Ecuador, Panamá, Paraguay, República Dominicana, El Salvador y Uruguay. Los Terms de Stake.com no se pudieron leer (HTTP 403), así que no citamos su lista de países restringidos. Pagar en moneda local no es una licencia local: que acepte pesos chilenos no hace a Stake.com un casino con licencia de Chile. Fuente: oficial (ayuda de Stake.com).` |
| ST5 | `…El retiro de la mesa sigue en sin dato. No es un cajero por CBU de un casino regulado en Argentina.` | `…El retiro de la mesa sigue en sin dato. Pagar en moneda local no es una licencia local.` |
| ST6 | comparison cell `Clase: crypto · fiat. Lista y redes: no verificado · 03 OCT 2026. BTC solo en el ejemplo de rakeback.` | `Clase: crypto · fiat · Chile: CLP con Visa (ayuda 24 AGO 2026). Lista y redes: no verificado · 03 OCT 2026. BTC solo en el ejemplo de rakeback.` |
H10 ✓: only help.stake.com; no stake.bet.ar or AR-licence angle. The «licencia de Chile» sentence is the explicit H12 guard Peter asked for.

### RAINBET (/mesa/rainbet/)
| # | Before (live) | After |
|---|---|---|
| R1 | card Retiro: `1× depósito` / `Mín. 15 USD citados` | `1× depósito` / `AstroPay en 6 países LatAm` |
| R2 | `Bank transfer ≠ CBU argentino.` / `Offshore no es registro AR.` | `Bank transfer ≠ transferencia local.` / `Moneda local ≠ licencia local.` |
| R3 | `Ese “bank transfer” es una frase del operador. No es un depósito por CBU ni un cajero de casino regulado en Argentina.` | `Ese “bank transfer” es una frase del operador; no encontramos a qué bancos o países aplica.` |
| R4 | new paragraph after R3 | `Moneda local, país por país (ayuda de Rainbet «How to Make a Fiat Withdraw», 29 MAY 2026, revisada el 15 OCT 2026). Para retirar, AstroPay figura en Argentina, Chile, Colombia, Ecuador, México y Uruguay. Mínimo $50 (la ayuda no aclara la moneda) y una comisión del 0,5% de la operación. Necesitás una cuenta activa de AstroPay y estar en una región donde AstroPay opere. Perú no figura en esa lista. Para depositar en moneda local no encontramos un artículo en la ayuda (búsqueda del 15 OCT 2026). Pagar o cobrar en moneda local no es una licencia local. Fuente: oficial (ayuda de Rainbet).` |
| R5 | comparison cell `FAQ 25 SEP 2026: BTC, ETH, LTC, XRP, SOL, TRX, BNB, USDT, USDC. Redes: no verificado · 03 OCT 2026.` | `FAQ 25 SEP 2026: BTC, ETH, LTC, XRP, SOL, TRX, BNB, USDT, USDC. Retiro AstroPay: AR, CL, CO, EC, MX, UY (ayuda 29 MAY 2026). Redes: no verificado · 03 OCT 2026.` |
«Mín. 15 USD citados» moves out of the card only; the paragraph line «mínimo de retiro de 15 USD» stays (homepage).

### ROOBET (/mesa/roobet/)
| # | Before (live) | After |
|---|---|---|
| RB1 | card Depósito: `Crypto + fiat` / `compra vía Swapped` | `Crypto + fiat` / `Swapped · AR: transferencia con DNI` |
| RB2 | `No es un cajero por CBU.` / `Offshore no es un casino regulado en Argentina.` | `Moneda local ≠ licencia local.` / `Offshore no es un casino regulado en tu país.` |
| RB3 | new paragraph after «El help declara fiat y crypto, y compra de cripto vía Swapped…» | `Moneda local, país por país (ayuda y T&C de Roobet, revisados el 15 OCT 2026). Argentina: depósito por «Bank Transfer» desde la opción «Cash», con tu número de DNI. Transferís el monto exacto a los datos bancarios que te muestran, y la acreditación puede tardar hasta 1 hora (ayuda «Bank Transfer Argentina Deposit», 18 JUN 2025). Ese artículo no dice moneda ni límites. Retiro con AstroPay: se pide desde «Cash» con el número de teléfono de tu cuenta AstroPay (ayuda, 24 JUL 2026). Ese artículo no lista países. México, Chile, Colombia y Perú: no encontramos un artículo de moneda local (búsqueda del 15 OCT 2026). Comisiones fiat, según los T&C: «1% de comisión en todos los depósitos FIAT exitosos», descontado del monto depositado (9.7); y si llegás a 10 o más retiros fiat en 30 días corridos, pagás un 2% por cada retiro adicional, «incluido el décimo» (10.8). Además, el proveedor de pago puede cobrar lo suyo (9.3). Nicaragua figura entre los territorios restringidos de Roobet (T&C 3.5 y ayuda del 25 AGO 2026). Aparte, varios proveedores de juegos bloquean países de la región según el proveedor o el juego: Argentina (a veces solo algunas provincias), Chile, Colombia, Ecuador, México, Perú y Uruguay aparecen en esa lista (ayuda «Regional restrictions by game provider», 1 SEP 2026). Eso limita juegos, no la cuenta. Pagar en moneda local no es una licencia local. Fuente: oficial (ayuda y T&C de Roobet).` |
| RB4 | `El retiro de la fila sigue sin dato. No es un cajero por CBU de un casino regulado en Argentina.` | `El retiro de la fila sigue sin dato. Pagar en moneda local no es una licencia local.` |
| RB5 | comparison cell `Clase: crypto · fiat+Swapped. Lista y redes: no verificado · 03 OCT 2026.` | `Clase: crypto · fiat+Swapped · AR: transferencia con DNI (ayuda 18 JUN 2025) · fiat: 1% por depósito (T&C 9.7). Lista y redes: no verificado · 03 OCT 2026.` |
Before the RB3 T&C quotes ship, someone re-renders /terms-and-conditions in a browser on PR day (my curl gets JS only).

### CLOUDBET (/mesa/cloudbet/)
| # | Before (live) | After |
|---|---|---|
| CB1 | `No es un cajero por CBU.` / `Offshore no es un casino regulado en Argentina.` | `Moneda local ≠ licencia local.` / `Offshore no es un casino regulado en tu país.` |
| CB2 | new paragraph after «Ese artículo nombra monedas de la compra…» | `Moneda local, país por país (ayuda y T&C de Cloudbet, revisados el 15 OCT 2026). La ayuda «What currencies are accepted on Cloudbet?» lista solo criptomonedas. Los T&C (7.3.1) dicen que pueden aceptar «fiat currency» según tu jurisdicción y los métodos disponibles. Para México, Chile, Colombia, Perú y Argentina no encontramos un método en moneda local (búsqueda del 15 OCT 2026). La compra con tarjeta pasa por Swapped (ver arriba). Pagar en moneda local no es una licencia local. Fuente: oficial (ayuda y T&C de Cloudbet).` |
| CB3 | `…El marketing de velocidad de retiro no entra como SLA. No es un cajero por CBU de un casino regulado en Argentina.` | `…El marketing de velocidad de retiro no entra como SLA. Pagar en moneda local no es una licencia local.` |
| CB4 | comparison cell `Clase: crypto · buy card (Swapped). Lista y redes: no verificado · 03 OCT 2026.` | `Clase: crypto · buy card (Swapped) · moneda local LatAm: no encontramos (15 OCT 2026). Lista y redes: no verificado · 03 OCT 2026.` |
Not «solo cripto» (I10).

### SHUFFLE (/mesa/shuffle/): S1–S5 are already LIVE (curl 08:18:13). Additions only:
| # | Before (live) | After |
|---|---|---|
| SH1 | `Offshore no es un casino regulado en Argentina.` (card) | `Offshore no es un casino regulado en tu país.` |
| SH2 | end of the S3 paragraph `…no una licencia de Argentina. Fuente: oficial (ayuda de Shuffle).` | `…no una licencia de Argentina. Otros países: en la ayuda de Shuffle no encontramos artículos de moneda local para México, Chile, Colombia o Perú (búsqueda del 15 OCT 2026); Brasil tiene uno propio (BRL con PIX). Pagar en moneda local no es una licencia local. Fuente: oficial (ayuda de Shuffle).` |
Live 17596504 re-curl (08:18:07): same bytes as 06:59 (102.251 B); S3 holds.

## 4. Checks
H1: no Spain targeting (Spain only inside operator lists; not quoted). H2: geo-blocks verbatim as the operator wrote them, no VPN or «workaround». H6: every figure has page + date. H8: no intent («no encontramos», never «oculta»). H9: no links, codes or cashier URLs (Roobet help's cashier links are not reproduced). H10 ✓. H12: «licencia local» guard per operator; no «legal en X». Fees not ranked. Numbers ES-AR (5.000, 1.000.000, 0,5%).

## 5. Before merge
- Re-render Roobet T&C (browser) for 9.7/10.8/3.5.
- Recheck Stake 8222435/13903305 and Rainbet 15254950 on the PR day (help-only sources).
- The card-line change «…en tu país» is site-wide style: apply it to all five fichas in one PR so they stay consistent.
