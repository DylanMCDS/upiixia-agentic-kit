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

## gpt-Dylan · checkpoint 2026-11-12 07:05 CST · turn still active

This is a recovery checkpoint, not a completed turn. Inspect the live worktree before acting; work may advance
after this snapshot. Do not deliver the old green SHA: its independent review rejected it.

### Current task: UAK-013, same owner and branch

- Owner: gpt-Dylan. State: REVIEW while fixing the rejection; `uak log --state CLAIMED` cannot move a task out of
  REVIEW. Use a normal `uak log` and reship with `uak done` after new complete green CI.
- Worktree: `/Users/dylanmartinezcastillo/Documents/Repositorios/Hackathon/upiixia-agentic-kit-dylan-wt/uak-013`;
  branch `feat/uak-013`; PR #11. Main45cef16 (PR #12 and UAK-011) is already merged into this branch.
- HEAD at this snapshot: `f281ab9c5171940caac607b948232377f133cf74`. Only
  `kit/.uak/tests/test_hook_session_start_speed.py` was dirty at 07:05; new ownership regressions were being added
  before engine changes. Preserve this work; do not reset or check out over it.
- f281ab9 passed 172/172 CI checks without retries and all 76 local smoke files, but fresh gpt-Dylan-r rejected
  it: after the two-minute stale-marker retry, overlapping workers can share `.new` and an older worker can corrupt
  the newer committed cache. Repro: `/tmp/uak013-r3-overlap-probe.sh` and `proof.txt`.
- Earlier rejected61e13a3 had an unseen-inbox delivery race; the one-snapshot fix is retained. Its deterministic
  regression passes current code and still fails against detached old61 after the Windows fixture correction.
- Four assertion-red records are durable in the implementation worktree's Git directory, under `uak-red/`:
  `UAK-013-original-c8a449c.txt`, `UAK-013-synchronization-1d6aed1.txt`,
  `UAK-013-inbox-snapshot-61e13a3.txt`, and `UAK-013-worker-ownership-f281ab9.txt`.

### Next exact work

1. `cd` into the UAK-013 worktree and inspect `git status --short`. Finish the ownership fix and the new tests,
   preserving all existing assertions and the three-second budget. The aged-live regression already has RED_OK
   on f281ab9; do not spend time running every unimplemented case to accumulate more reds.
2. Chosen development design: local per-worktree Git CAS ownership, immutable PID/generation records, actual child
   PID from `$!`, no age-only takeover of a live worker, and a CAS-owned REAP phase before replacing a dead owner.
   Interrupted recovery retains the same old generation until cleanup succeeds. All publication sources must be
   private, beneath the physical Git directory and on the cache's filesystem; delayed old rename sources must be
   revoked before replacement work starts. Cleanup failure prevents replacement. Validate record schema/PIDs/tokens
   before cleanup. Disable reference-transaction hooks on internal ref mutations. Every inbox writer, including
   tick's inline path, needs a private temporary file too.
3. Regression set being added: live-worker coalescing, dead-owner recovery, orphan output descriptors, a paused
   orphan `mv`, interrupted/failed REAP, corrupt-record confinement, hook exclusion, simultaneous CAS acquisition,
   and abandoned parent-to-child handoff. Use the existing POSIX-in-Bash/LF fixture setup on Windows.
4. Sol is the primary implementer; Astra is the read-only design mentor. After targeted tests are green, have the
   mentor inspect the actual diff before push/full CI. The eventual formal reviewer must be a NEW clean-context
   gpt-Dylan-r session that sees SHA/diff/tests/CI, not this handoff or implementation reasoning.
5. Run Verify, related hook_claims tests, lint/hashes and full isolated smoke with `--jobs auto`; push a NEW SHA;
   wait for its complete green CI before `uak done ... --to gpt-Dylan-r`, then independent review. Keep main current.
   Existing test changes need Dylan's audited permission; no assertions or timeouts may be weakened.

### Human permissions and following tasks

- Dylan explicitly authorized the assistant in chat to execute `UAK_HUMAN=Dylan ... uak allow UAK-013 --tests`;
  it was executed and audited for synchronization/Windows cleanup waits without assertion changes. This was a
  specific exception, not blanket permission for future UAK_HUMAN commands or merges.
- Ask for future human commands explicitly, with the exact command and a short authorization phrase Dylan can
  paste in chat if delegation is wanted. Final merges remain Dylan's.
- UI-005 remains with claude-Dylan, PR #9, fix8326fa8, awaiting handover when appropriate. Do not edit its worktree
  before Dylan's `UAK_HUMAN=Dylan bash .uak/bin/uak handover UI-005 --to gpt-Dylan`; then update its `.uak-env`, merge
  current main, run Verify/CI and deliver to a fresh gpt-Dylan-r reviewer. Check personal-file manifest exclusion
  and failed-commit index/ref restoration. UI-006, UI-007 and UAK-012 follow; none was taken during this checkpoint.
- Out-of-scope findings are recorded in PENDING-IMPROVEMENTS.md #22–24. The old61 Windows guard failure was retried
  once unchanged and passed; its cause remains unproven. f281ab9's own CI passed all checks on attempt1.

### Checkpoint update · c41641a published · turn remains active

- The ownership implementation is now committed and pushed as `c41641a6cf270118ad5f33b17c3464835b150f0d` on
  `feat/uak-013`, PR #11. It supersedes the dirty-worktree snapshot above. Inspect HEAD/status before resuming.
- The read-only Astra mentor completed actual-diff development preflight. Final focused checks pass: 15
  session-start/ownership cases plus three hook_claims cases (18 total), lint0, hashes472 current. Existing
  assertions and the three-second budget remain intact. The mentor did not provide independent PR approval.
- Full 76-file smoke and exact-head CI are running. Next: wait with
  `gh pr checks 11 -R DylanMCDS/upiixia-agentic-kit --watch --interval 60`; verify that both current runs and all
  newly created matrix checks are complete and green. Do not deliver merely because initial discover checks pass.
- Only after full smoke and exact-head CI pass: reship UAK-013 with `uak done ... --to gpt-Dylan-r`, then start a
  NEW clean-context reviewer on c41641a (or the newer verified HEAD if a fix was needed). Prepared detached snapshot:
  `/Users/dylanmartinezcastillo/Documents/Repositorios/Hackathon/review-gpt-uak013-c41641a`.
- Final mentoring regressions cover live coalescing, dead recovery, orphan next/inbox descriptors, delayed old
  `mv`, failed/interrupted REAP, corrupt-record/path confinement, hook exclusion, concurrent acquisition, abandoned
  parent handoff and inbox failure status. Publication uses private same-filesystem files and fenced recovery.
- Current log paths: `/tmp/uak-013-verify-owner.log`; full smoke/CI final log paths are reported by the running
  implementer. The durable f281 ownership red is in `gitdir/uak-red/UAK-013-worker-ownership-f281ab9.txt`.
- No other task was taken, no UAK_HUMAN permission beyond the specific UAK-013 test authorization was used, and no
  merge was performed. UI-005 handover and final human merges remain pending.

### Checkpoint update · 7cfd519 validation · turn remains active

- Current published HEAD is `7cfd519ba754da066edcdcd882b1a43a9babe286`. c41641a's Windows suites passed 14/15 cases;
  the remaining fault-injection precondition missed its target because native and POSIX paths differed. 7cfd519
  compares them physically inside Bash; engine code, assertions and budgets are unchanged in that correction.
- Full isolated local smoke passed all76 files; all18 targeted cases, lint and hashes pass. Both current Windows
  15-case suites passed. Prepared detached review worktree: `../review-gpt-uak013-7cfd519` in the review clone.
- CI runs: push43228658522 and PR43228669067. PR completedSUCCESS; push had a macOS suite1 cancelled before any
  step (job131218592643, logs unavailable). The authorized `gh run rerun 43228658522 --failed` was requested once.
  Wait for that attempt to finish and independently audit its latest run/check-suite results before delivery.
- `gh pr checks --watch` returned0 while a cancelled check remained, and aggregate jobs API returned502 during
  rerun monitoring. Neither is proof of green CI. The implementer switched to the blocking checks watcher and
  run metadata/check-suite audit. No second rerun or source change was made at this checkpoint.
- After all current 172 checks are completeSUCCESS: reship UAK-013 at7cfd519 (or a newer required fix) with
  `uak done ... --to gpt-Dylan-r`, then NEW clean-context formal review. Last formal verdict remains reject on
  f281ab9; do not confuse mentor preflight or green tests with independent approval.


## gpt-Dylan · end of turn 2026-11-12 08:23 CST

Dylan switches the turn to claude-Dylan. UAK-013 was successfully handed over with the owner's normal
`uak handover UAK-013 --to claude-Dylan`; lease renewed, `.uak-env` is claude-Dylan/UAK-013. No new UAK_HUMAN
exception was used. All our local CI watches are stopped; GitHub CI was left running. No merge was performed.

- Current code: clean `feat/uak-013` at **7cfd519ba754da066edcdcd882b1a43a9babe286**, PR #11, worktree
  `/Users/dylanmartinezcastillo/Documents/Repositorios/Hackathon/upiixia-agentic-kit-dylan-wt/uak-013`.
- Last observed CI: **171/172 pass**, only replacement macOS suite1 job131233222771 pending in push43228658522.
  PR43228669067 completedSUCCESS. The cancelled original Mac job had no steps; one --failed retry was requested.
  Both Windows15-case suites passed. This is the last watcher output, not a fresh assertion about current CI.
- Local final evidence: targeted18/18, isolated full package smoke76/76, lint0, hashes472 current. Mentor actual-diff
  development preflight passed; it is NOT formal independent approval. Last formal reject is still f281ab9.
- **Immediate next step:** read inbox/status, resume `gh pr checks 11 -R DylanMCDS/upiixia-agentic-kit --watch
  --interval 60`, then audit exact HEAD and both run/check-suite latest results (86 each, no pending/non-success).
  Aggregate jobs API returned502 during rerun; use run metadata + check-suite API. CLI watch exit0 alone is insufficient.
- Only after full current CI is green: `uak done UAK-013 --pr https://github.com/DylanMCDS/upiixia-agentic-kit/pull/11
  --to claude-Dylan-r --evidence "..."`, then a NEW clean-context claude-Dylan-r reviewer. Give reviewer only exact
  SHA/diff/tests/CI, not this handoff or implementation reasoning. Rerun Verify15 + hook_claims3, inspect assertion
  reds and audited test permission, portability/security. Code/records English; talk to Dylan Spanish.
- Evidence: `/tmp/uak-013-smoke-reap-path.log`, `/tmp/uak-013-verify-reap-path.log`,
  `/tmp/uak-013-pr-checks-watch-mac-retry.log`, `/tmp/uak-013-reap-path-pr-run.json`,
  `/tmp/uak-013-reap-path-mac-job.json`. Four durable assertion-red proofs are in the Git directory's `uak-red/`
  (c8a449c,1d6aed1,61e13a3,f281ab9), listed in earlier checkpoint. UAK-013 existing-test permission already audited.
- On independent approval, final merge is Dylan's; give him the exact command. Integrate after human merge and
  merge main into in-flight branches, rerunning Verify/lint before delivery. Main45cef16 is already included here.
- UI-005 remains owned by claude-Dylan (PR #9, last known fix8326fa8); no handover to gpt happened. After UAK-013,
  continue it in its own worktree, merge current main and revalidate. Review manifest exclusion of personal files
  present before installation and failed-commit restoration of index/refs. Browser1280x720 and390x844 required.
- Then UI-006 (contract inbox47/53), UI-007, UAK-012. One live task per identity. No code outside task Paths;
  findings go to PENDING-IMPROVEMENTS.md. No existing-test edits without audited allow. Never use UAK_HUMAN
  without a specific new authorization; the previous chat exception covered UAK-013 test permission only.

## claude-Dylan · turn 2026-11-12 (afternoon) → next session (gpt-Dylan unavailable this week)

State of record is claims; this is the map. Talk to Dylan in Spanish. Opus 5.5 works; Fable 5.2 only as mentor for hard
problems. claude-Dylan-r reviews as a fresh clean-context subagent (SHA, diff, tests, CI only).

| Task | State | Next |
|---|---|---|
| UAK-013 | INTEGRATED (main a5f38f1) | — |
| UAK-068 (session start 41→15 processes; Windows count) | APPROVED at c083475, PR #14 | Dylan merges PR #14; then `uak integrate UAK-068` (owner claude-Dylan-2, worktree upiixia-agentic-kit-dylan-wt/uak-068) |
| UAK-012 (machine-independent tests) | CLAIMED by claude-Dylan, PR #13 at 2a8f99f; local unisolated smoke 507 PASS | after UAK-068 is on main: merge main, push, CI, `uak done --to claude-Dylan-r`, clean review |
| UI-005 (prepare from the page) | REVIEW, PR #9 at bf0995f (fixes the f8d5d84 reject: refused push undone and says so; notices wrap at 390) | same as UAK-012: merge main after UAK-068, CI, ship, clean review |
| UAK-067 (CI once per SHA) | AVAILABLE; UAK-006 now depends on it (Dylan's amend); claim refused while UI-005 holds WHY.md | claim after UI-005 is integrated (use identity claude-Dylan-3, never claude-Dylan-r) |
| UI-006 + UI-007 | AVAILABLE, wait for UI-005 (shared files) | Dylan agreed to ship them as ONE delivery. Contract draft: notes/handoff:UI-006-contract.md (Fable pass + reviewer agreement before code) |

Rules adopted today (Dylan): one complete all-SUCCESS run per SHA is enough when the other run only has runner-capacity
cancellations (0 steps); real failures never ship (UAK-012/UI-005 currently show the Windows session-start flake that
UAK-068 fixes). Pre-review adversarial probes + browser QA before every done. Cancel obsolete runs of old SHAs.
Tools: CI shepherd script and Playwright venv lived in the session scratchpad (recreate if gone; venv outside the repo).
Mac quirks: no `python` (shim python→python3 on PATH for Verify), global core.hooksPath and real Codex pace (UAK-012 fixes
the tests; isolate with GIT_CONFIG_GLOBAL + CODEX_HOME until it lands). Windows check by a separate Claude found the Git
Bash launcher PATH issue; use that machine only for one-off verification passes.
Upstream: JoahanMorales/upiixia-agentic-kit PR #2 (head DylanMCDS:main) must be complete (all 12 tasks + UAK-068
integrated, main green, PR body updated) before Dylan asks his friend to review; its fork workflows need the owner's
"approve and run". Task IDs collide with upstream (UAK-009..013, UAK-067/068): Dylan to agree a prefix with the owner.
Pending improvements: notes/handoff:PENDING-IMPROVEMENTS.md up to #32 (#25 installer vs global hooksPath and #32
Windows wait are product decisions for Dylan).

## claude-Dylan · end of turn 2026-11-12 (evening) → next session

- INTEGRATED today: UAK-013 (a5f38f1), UAK-068 (bfc493e), UI-005 (bcee290), UAK-012 (ba723d9). 10 of the 12 program
  tasks are integrated; remaining: UI-006 + UI-007 (one delivery, contract in notes/handoff:UI-006-contract.md).
- Next, in order: (1) confirm main CI at ba723d9 (rerun only capacity cancellations); (2) UAK-067 as claude-Dylan-3
  (now claimable: UI-005 released WHY.md); (3) UI-006 + UI-007 as claude-Dylan, Fable pass + reviewer agreement on the
  contract before code; (4) update the body of upstream PR #2 and tell Dylan it is ready for his friend.
- Fixture tests are now machine-independent (UAK-012): no isolation needed on Dylan's Mac except the python shim.
- Pending improvements #22-#34 added today (product decisions for Dylan: #25 installer vs global hooksPath, #32 Windows
  session-start wait).

## claude-Dylan · end of turn 2026-11-12 (night) → Seebaastiaan's session (Dylan hands over to a second human)

State of record is claims; this is the map. A new human (GitHub Seebaastiaan, write access to DylanMCDS/upiixia-agentic-kit)
continues with HIS OWN identities (e.g. claude-Sebastian, claude-Sebastian-r): never claude-Dylan*.
- INTEGRATED today: UAK-067 (main 0798117, CI once per SHA: feature SHAs now run CI only on pull_request).
  11 of the 12 program tasks are integrated or in review; remaining: UI-006 (REVIEW) and UI-007 (AVAILABLE, depends on UI-006).
- UI-006 · REVIEW at 57b397d, PR #16, branch feat/ui-006, worktree upiixia-agentic-kit-dylan-wt/ui-006 (Dylan's Mac).
  CI 89/89 (run 43358179322; windows test_v592 flake passed on rerun, PENDING #38). Contract + 9 amendments + note:
  notes/handoff:UI-006-contract.md. 98507da was rejected only for missing Windows evidence; now in
  qa/UI-006-windows.md (PASS). A re-review by claude-Dylan-r at 57b397d was started at the end of this turn: read
  its verdict with `uak status --task UI-006` (do not start a second review of the same SHA).
  Approve → merge PR #16 (a human merges: Seebaastiaan or Dylan) → `uak integrate UI-006` (as the task owner or any
  agent, AGENTS.md §3.8). Reject → `uak handover UI-006 --to <your identity>` (or ask Dylan) and fix it.
- UI-007 · after UI-006 is INTEGRATED: `bash .uak/bin/wt new UI-007 --agent claude-<you>`. Spec: `uak status --task
  UI-007`; contract section "UI-007" + amendments 8 (focus test) in UI-006-contract.md. Test first (uak red), browser
  QA 1280x720 + 390x844 en/es before done, reviewer = a different identity with clean context.
- Then closing: upstream PR JoahanMorales/upiixia-agentic-kit #2 (head DylanMCDS:main): when all 12 tasks are
  integrated and main CI is green, update its body (list of tasks/PRs) and tell Dylan; Dylan tells the owner.
- Rules kept: test first, never weaken/edit existing tests without a human `uak allow --tests`; one live task per
  identity; adversarial pre-review + browser QA before done; one complete all-SUCCESS CI run per SHA (a capacity
  cancellation with 0 steps is not a failure; a real failure never ships; rerun only proven flakes, record them in
  PENDING-IMPROVEMENTS); merge main into in-flight branches after each integration; cancel runs of obsolete SHAs.
- Machine notes: Dylan's Mac has no `python` (shim python→python3 on PATH for Verify). Windows: `python` may be the
  Store stub; use `py`. Git Bash for every engine command on Windows.
- Pending improvements up to #38 (#35, #36, #38 Windows CI flakes; #37 ci-once parser P3). Product decisions stay Dylan's.
- UPDATE (same night): claude-Dylan-r APPROVED UI-006 at 57b397d (P3s → PENDING-IMPROVEMENTS #39-#41). Next: a human
  merges PR #16 (`gh pr merge 16 --repo DylanMCDS/upiixia-agentic-kit --merge`), then `uak integrate UI-006`, then UI-007.
- UPDATE: PR #16 merged (main e923f7d) and UI-006 INTEGRATED. 11 of 12 program tasks integrated. Next: UI-007
  (`bash .uak/bin/wt new UI-007 --agent claude-<you>`), then main CI green, then upstream PR #2 body.

## claude-Dylan · 2026-11-13 (early) · usage limit reached mid-turn
- ALL program tasks INTEGRATED (14: UI-001..007, UAK-009..013, UAK-067, UAK-068). main 6f31689, CI 90/90 green (run on 6f31689).
- UI-007 merged as PR #17 after one reject (Spanish dashboard English left) + fix; P3s → PENDING #42-#47.
- Upstream sync in flight: PR #18 (sync/upstream-3, 14 upstream commits, clean merge, lint/hashes/gen_harness OK). Its local smoke and CI were
  still running. Next: if CI green → merge #18 (Dylan authorized merges) → update body of JoahanMorales/upiixia-agentic-kit#2 listing the
  14 tasks with fork PRs #1-#6, #9-#11, #13-#17 → tell Dylan, with a message ready for the owner.
- Test rounds (Dylan's request) on cafeteria copies with local bare remotes, kit at 6f31689, under /private/tmp/claude-501/-Users-dylanmartinezcastillo-Documents-Repositorios-Hackathon-upiixia-agentic-kit-dylan/5d490525-c357-4b1d-b5e7-ec67917ea0d2/scratchpad/rounds:
  r1 novice browser es + frames for the video (rN/frames/*.png + captions.txt), r2 novice docs/terminal (DONE: rN/REPORT.md),
  r3 with context verifying every improvement with real Claude/Codex, r4 adversarial. r1/r3/r4 were still running when the limit hit:
  read their REPORT.md. Video: assemble r1 (and r3) frames with
  ffmpeg -framerate 1 -pattern_type glob -i 'frames/*.png' -vf "scale=1280:-2,format=yuv420p" video.mp4 (not done yet).
- r2 findings (high): README never says to open claude once and accept workspace trust (headless /uak-plan ignores permissions);
  terminal setup registered example reviewers (ana/leo from HACKATHON.md) instead of the person's identities; sprint order (uak clock)
  not in README. Treat as backlog candidates, product decisions for Dylan.
