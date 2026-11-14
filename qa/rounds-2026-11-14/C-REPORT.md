# Round C · two humans, real Claude agents end to end · kit 4df3acb · saved by the lead from the tester's reply

Setup: local bare remote C/origin.git; clones C/ana and C/beto; real Claude Code 2.1.325 headless with the page's own prompts. Install → 2 INTEGRATED tasks (CAF-001, CAF-003) in 12.5 min, ~4.73 USD over 12 sessions (planner 1.12). Logs: C/logs/ (timeline.txt, 01..24 logs, stream-json per run).

Worked: test-first (RED_OK first), parallel review CONFLICT handled, reviewer rotation, parallel merges clean, followup, agents filed black-box frictions, no review loop.

| # | Sev | Finding | Proposed fix |
|---|---|---|---|
| 1 | P1 | Nothing on the onboarding path creates .uak/bin/smoke-project; `uak start` says READY, then first /uak-ship and the merge gate fail PRODUCT_UNVERIFIED. | start/page TODO with per-stack init-smoke; planner's setup task owns the adapter. |
| 2 | P1 | Non-GitHub remote: `wt pr` "Not a GitHub remote" and `done --pr file://` says "use wt pr" — dead loop; Review-Mode: claims needs no PR. | Accept `--pr none`/branch with Review-Mode claims; both messages name it. |
| 3 | P1 | Integrated main does not boot (ImportError Queue vs QueueStore); tests force a fake store so tests, reviews and gates were green. | Default smoke boots web stacks and hits one route; skeleton test uses the real store. |
| 4 | P2 | `uak start` "update the kit 6.2.0 vs 6.3.0" points at ~/.uak-kit (other checkout) and blocks START READY for a fresh teammate clone (only UAK_KIT_PIN=1). | Record install source; update is a NOTE once the kit is on main. |
| 5 | P2 | Planner says `uak deploy --write` made a Dockerfile; deploy has no stdlib-Python stack; agent hand-wrote a broken Dockerfile. | Plain-Python deploy stack, or plan lint warns. |
| 6 | P2 | Every headless run: "Ignoring 51 permissions.allow entries … not trusted" (main checkout and each worktree); proceeded only thanks to user-level settings. | `wt new` prints/offers the trust step; document the headless workaround. |
| 7 | P2 | Contract message cites a SHA only on an unmerged feature branch; consumer can't find it (fed #3). | `msg --kind contract` resolves SHA → branch and prints `git show origin/BRANCH:path`. |
| 8 | P2 | Files outside Paths pushed with no warning; only /uak-ship discipline caught them. | Warn in pre-push hook or checkpoint. |
| 9 | P2 | Clone kept global core.hooksPath; kit pre-commit never ran; doctor only warns; second clone needed manual config. | `start --fix` sets local hooksPath on clones. |
| 10 | P3 | init-smoke leaves an empty scripts/ dir. | Remove the mkdir. |
| 11 | P3 | `uak dash` tar DeprecationWarning (dash.py:97). | filter="data". |
| 12 | P3 | Dashboard data `mode: ""` (reads claims meta/config.md). | Fall back to PROJECT.md on main. |
| 13 | P3 | `tokens --team` "no transcripts found" though local ones exist. | Explain "no machine reported; this machine has N; run tok". |
| 14 | P3 | stats lists normal queue waits as human-queue reasons. | Count only escalations. |
| 15 | P3 | `next` "= unchanged" cache keyed by session, not identity. | Add UAK_AGENT to the key. |
| 16 | P3 | Board shows "PR#001" for a non-numeric URL. | Show URL tail. |
| 17 | P3 | /uak-start stops after the first green criterion: 4 prompts per task headless. | Offer a headless "run to REVIEW" prompt. |
