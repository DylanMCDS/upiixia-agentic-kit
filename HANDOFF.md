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
