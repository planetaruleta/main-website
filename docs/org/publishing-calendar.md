# Publishing calendar

Living ledger of what Planeta Ruleta has live, scheduled, on hold, expired, or removed. Owner: Aviv Abramowitz. Day-to-day ops sit under Peter, Chief of Staff.

Update on every publish/expiry/hold change.

All times are Israel time (IL, Asia/Jerusalem). In October 2026 that is UTC+3.

Statuses used: LIVE, SCHEDULED, HOLD, EXPIRED, REMOVED.

## Ledger

Rows are newest-first. Spanish asset names and terms (señal, ficha, mesa, canal) stay as used on the site and in the canal.

| Date/time (IL) | Channel | Asset | Link / ref | Status | Expiry / next action | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-08 07:37 IL | Telegram canal (@planetaruleta) | Post: Shuffle Gates of Olympus 500x / $40K | https://t.me/planetaruleta/26 | LIVE | — | Publishing & Analytics Ops |
| 2026-10-08 03:26 IL (PR #32 merged) | Website — home page señales + /mesa/shuffle/ lobby chip | Señal `lobby-shuffle-gates-olympus-500x-40k-2026-10-07` (Shuffle Gates of Olympus 2500, $40K split, 500x+) | PR #32, merge commit 277e42a9 | LIVE | Expires Mon 2026-10-12 03:00 IL (= 2026-10-12T00:00Z). No auto-expiry in the renderers; removal PR prepared, Peter merges at/after expiry | Peter (merge) / Publishing & Analytics Ops (prep) |
| 2026-10-04 07:39 IL | Telegram canal (@planetaruleta) | Post: Lobby radar — Rainbet Daily Race (Saturday, 24h leaderboard) | https://t.me/planetaruleta/24 | LIVE | — | Publishing & Analytics Ops |
| — (between 2026-09-25 21:28 IL and 2026-09-28 10:52 IL) | Telegram canal | Message id 16 (content unknown) | https://t.me/planetaruleta/16 | REMOVED | Returns "Post not found" publicly. Telegram ids are sequential, so something got id 16 between #15 (Stake welcome math flash, 25 Sep) and #17 (Sunday digest, 28 Sep) and was then deleted, or it was a non-public service message. It is NOT the Daily Race post, which is live as #24. | — |
| — (date unknown) | Podcast — iVoox, Spotify | EP-01 | — | LIVE | — | Publishing & Analytics Ops |
| — (date unknown) | Podcast — iVoox, Spotify | EP-02 | — | LIVE | — | Publishing & Analytics Ops |
| — | Podcast | EP-03 | — | HOLD | Not approved yet; needs Aviv/Peter approval before publishing | Peter / Aviv |
| — | Video / creative | Theme 1 master | bdc52ea9 | HOLD (KEEP) | Keep the master; NOT approved to publish | Peter / Aviv |

### Telegram id gaps

Checked 8 Oct 2026 against the public channel preview at t.me/s/planetaruleta. The public ids are 1, 5–8, 12–15, 17, 20–26. The ids 2–4, 9–11, 16 and 18–19 don't render publicly (deleted posts or service messages).

## How to update

- Add a row per publish.
- Flip status on expiry or removal (EXPIRED or REMOVED).
- Link the PR or the post in Link / ref.
- Keep rows newest-first.
