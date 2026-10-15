# EDCOMP gate · Rainbet path-B caveat · restatement with 15 OCT fetch
## What's "pending"
Nothing new. The Analyst's daily-2026-10-15 lines («the E&C one-line path-B caveat is still pending», «Still pending from 14 OCT») are stale: the caveat was gated 14 OCT (`EDCOMP-rainbet-ficha-caveat-2026-10-14.md`, PASS WITH CHANGES), merged in PR #35, and is **live** on https://planetaruleta.com/mesa/rainbet/ (curl 15 OCT 07:00:41 IL, `pr-rainbet-text.txt` L51, L55, L60–61: E1, E2 and the full §2 caveat verbatim). No newer path-B draft or request found in docs/org/gates, docs/drafts or the intel pending folder (Intel: "pending/ has no staged files").

## Live recheck (curl, HTTP 200, 15 OCT IL; `docs/org/intel/evidence/2026-10-15/edcomp-recheck/`)
| Source | Fetched | Text | vs 14 OCT |
|---|---|---|---|
| rainbet.com home | 06:59:31 | "Welcome bonuses on Rainbet come in two paths." (L152) · "Max bet 2% of the deposit while the promotion is active" (L160) | unchanged |
| /deposit-promotion-terms | 06:59:32 | "No Wager Lock Promotion" (L60) · "Max bet when active is 2% of deposit amount." (L46) | unchanged |
| api /promotions/list | 06:59:32 | `wager-locked-1`, `no-wager-lock-1` | unchanged |
| help 15268657 | 06:59:33 | "Rainbet has one first-deposit promotion: the 40x Wager Locked" · dateModified 01 SEP 16:44 IL | unchanged |
| help 9831951 | 06:59:33 | "…capped at a maximum of 1% of deposit amount per bet unless stated otherwise." · dateModified 01 SEP 16:14 IL | unchanged |

## VERDICT: PASS (restated). Live caveat text stays as is.
Optional date-folio refresh only (no other change):
- before: `Rainbet publica dos versiones (rechequeo 14 OCT 2026).` → after: `Rainbet publica dos versiones (rechequeo 15 OCT 2026).`
Path-B assets other than the ficha caveat and V1 (gated separately) remain on hold. The conflict still stands, so do not say which version applies (H12).
