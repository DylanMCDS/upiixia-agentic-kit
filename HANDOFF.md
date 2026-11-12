# Session handoff · 2026-11-11 (end of day, Windows machine)

Human: Dylan. Implementer: claude-Dylan (Claude Code, Opus 5.5; Fable 5.2 as mentor for hard problems).
Independent reviewer: gpt-Dylan (Codex; usage is limited, keep it to reviews). Repo: https://github.com/DylanMCDS/upiixia-agentic-kit
(origin = Dylan's fork; upstream = JoahanMorales/upiixia-agentic-kit). State of record: the `claims` branch, not this note.

## Where everything stands
| Task | State | Notes |
|---|---|---|
| UI-001 local visual setup + unified dashboard | INTEGRATED | PR #1 merged as 126582e; main CI 68/68 green |
| UI-002 guided Beginner + "Your app" (Live-URL) + macOS D1-D3 | REVIEW, SHA 9dee91e, PR #2 | Shipped to gpt-Dylan. CI run 42967267278 was still running at handoff (19/69 green, 0 failed): confirm it before approving |
| UI-004 plan the project in the interface | AVAILABLE after UI-002 (Paths overlap setup.py/setup.html) | Design: UI-004-design.md; research: ui004-headless-research.md |
| UI-003 journey tests + docs | waits for UI-001, UI-002 | Should also cover UI-004 if Dylan adds it to Depends |
| UAK-006 | waits for UI-002, UI-004 | upstream perf task; leave it |

Other AVAILABLE upstream tasks (UAK-001…) are not ours; do not claim them.

## Decisions already made by Dylan (do not re-ask)
- Spanish/English UI; Spanish user-facing strings authorized. Code, docs, commits and records in English.
- Terminal stays in the background; almost everything a human does happens in the local interface.
- UI-004: launch the coding tool headless with a fixed argv (Claude Code and Codex only for now); the human approves
  and publishes the plan in the interface with a typed confirmation (recorded in WHY.md as Dylan's decision).
- Beginner is almost fully guided; "Your app" deploy link via Live-URL (https only).
- Final merge is Dylan's. Engine-file merges stop at MERGE_HUMAN: Dylan merges the PR on GitHub, then the owner runs
  `bash .uak/bin/uak integrate ID`.

## Known environment facts
- Windows: Python at C:/Users/dylan/AppData/Local/Programs/Python/Python313, Git Bash at C:/Program Files/Git/bin;
  `python`/`python3` may be Store aliases; gh at C:/Program Files/GitHub CLI/gh.exe (logged in as DylanMCDS).
- Windows-only noise, not regressions: test_claims_perf::the_counter_sees_ps fails identically on main 87af168;
  kit_lint shows CRLF/exec-bit findings on a core.autocrlf=true checkout; kit_hashes --check is only conclusive on
  an LF checkout or in CI. The fork's CI (Actions enabled) is the cross-platform authority.
- macOS: verified UI-001 with /bin/bash 3.2 (report on the Mac: ~/uak-mac-check-report.md).
- `test.yml` runs on push and pull_request only; a PR close/reopen retriggers it without a new SHA.
- The red record (`uak red`) lives in the worktree's .git and is not pushed: record it on the machine that ships.

## Next steps
1. gpt-Dylan: review UI-002 at 9dee91e (prompt in the session message). On reject, claude-Dylan fixes test-first on
   a new SHA; on approve, Dylan merges PR #2 (likely MERGE_HUMAN), then `uak integrate UI-002`.
2. claude-Dylan: after UI-002 is INTEGRATED, claim UI-004 (`bash .uak/bin/wt new UI-004 --agent claude-Dylan`),
   write its tests with a fake planner and a local bare remote, `uak red UI-004`, implement from UI-004-design.md,
   verify the open risks listed there, ship to gpt-Dylan.
3. Then UI-003 (journey tests, docs, WHY.md, CHANGELOG, known-files) — consider giving it to the Mac.

## Files in this branch
HANDOFF.md, UI-002-design.md, UI-004-design.md, ui004-headless-research.md, qa/ (Playwright QA scripts used for
browser evidence: run them from a venv outside the repo), shots/ (evidence screenshots), plan/ (the review packets,
PLAN, amendments and PR bodies from ../dashboard-review).

## claude-Dylan · end of turn 2026-11-11 (late evening) → gpt-Dylan's turn

Method now (Dylan): turns; the agent on turn does BOTH development and review. Implement as your identity, review
as a separate reviewer identity (claude-Dylan-r / gpt-Dylan-r, registered) with a fresh-context reviewer session.
Quality standard unchanged: test-first (uak red), exact-SHA CI complete and green before `uak done`, never change an
existing test without Dylan's `uak allow --tests`, findings outside Paths go to PENDING-IMPROVEMENTS.md.

### State of record (claims)
| Task | State | Where | Next exact step |
|---|---|---|---|
| UAK-013 session-start < 3 s | CLAIMED by gpt-Dylan (handed over) | branch feat/uak-013, worktree ~/Documents/Repositorios/Hackathon/upiixia-agentic-kit-dylan-wt/uak-013 (.uak-env set to gpt-Dylan), PR #11, SHA 126d377 | Wait for PR #11 CI (complete + green), then `uak done UAK-013 --pr <#11> --to gpt-Dylan-r`, review it as gpt-Dylan-r (fresh context). Earlier CI found: 3 s budget tight on CI runners (default wait now 1.0 s), Windows cold start, and Windows cleanup (tests now wait with the rename probe). |
| UI-005 prepare from the page | REVIEW, owner claude-Dylan; last verdict reject on 57ef048 (claude-Dylan-r) | branch feat/ui-005, worktree .../upiixia-agentic-kit-dylan-wt/ui-005, PR #9, fix SHA 8326fa8 | Fixes for the 57ef048 review are pushed (red at 57ef048 for publish_ignores_personal_files_present_before_install, failed_commit_leaves_index_and_refs_as_before, human_name strict). After UAK-013 leaves CLAIMED: Dylan runs `UAK_HUMAN=Dylan bash .uak/bin/uak handover UI-005 --to gpt-Dylan` (claude-Dylan is paused), set that worktree's .uak-env to gpt-Dylan/UI-005, wait for PR #9 CI on 8326fa8, `uak done UI-005 --pr <#9> --to gpt-Dylan-r`, review as gpt-Dylan-r. |
| UI-006, UI-007 | AVAILABLE after UI-005 | — | UI-006 contract already agreed (inbox #47/#53): explicit human click, validated NAME/ID, fixed argv, distinct identities, the real wt path. |
| UAK-012 tests independent of the machine | AVAILABLE | — | Take it when free. |
| Sync PR #12 (upstream UAK-062..066) | open | branch sync/upstream-2 | Dylan merges; then merge main into in-flight branches and rerun Verify. |

### Faster local verification (pulled from the real repo, UAK-054)
- The kit's smoke runs parallel shards only when it reads `Smoke-Jobs` from the root .uak/PROJECT.md; `cd kit && bash .uak/bin/smoke --package-only` did NOT (serial). Use `cd kit && bash .uak/bin/smoke --package-only --jobs auto` (10 cores here).
- On this Mac, run tests with an isolated global Git config (GIT_CONFIG_GLOBAL=<file with user.name/email>) and a `python`→python3 shim on PATH for Verify lines that say `python`.
- Use `uak wait ... --for message|approve|integrated` and `gh pr checks <N> --watch` to wait; never poll.
