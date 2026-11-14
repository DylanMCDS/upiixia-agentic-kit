## The visual setup: install, get ready, plan and start the team from a local page

Twenty-four tasks from DylanMCDS/upiixia-agentic-kit, built with the kit's own flow. Every task had:
- its tests first (`uak red`);
- an independent reviewer (a second identity with a clean context);
- CI on the exact SHA (ubuntu, Windows, and macOS when GitHub had runners);
- the human's merge.

**Why.** The human of the project found the terminal-only setup hard to follow. He asked to keep the terminal in the background, with almost everything a person does in a local page. A hackathon simulation then showed where people got stuck. The evidence for each rule is recorded in `kit/.uak/docs/WHY.md`.

### The setup page

| Task | What it adds | Fork PR |
|---|---|---|
| UI-001 | `bash install.sh --wizard [PROJECT] [--no-open]` serves a loopback-only page (127.0.0.1, random port, session token, Host, Origin and JSON checks) for a 5-step setup. Nothing is written before Install. Configuration and Dashboard share one workspace, in Spanish/English and light/dark. | #1 |
| UI-002 | A guided Beginner profile: one step at a time from the readiness gate, why it matters, and what is already done. It re-checks automatically. "Your app" shows the deploy link from a new `Live-URL:` key. | #2 |
| UI-003 | Journey tests (clean setup, interrupted install, missing prerequisites), browser evidence at 1280x720 and 390x844, `docs/DASHBOARD.md`. | #5 |
| UI-004 | Planning in the page. Claude Code or Codex plans headless with a fixed argv and a constant prompt. The server verifies that only TASKS.md and OWNERS.md changed and runs `uak lint` itself. A typed approval bound to a digest of the reviewed files commits exactly those files and pushes the verified SHA. | #3 |
| UI-005 | Preparation from the page. The page:<br>• writes the event schedule (Freeze-Epoch);<br>• publishes the kit as a human act from an installer-written manifest, never the unapproved plan files, checking the whole committed tree before the push;<br>• shows a "Do this in a terminal" box for anything else;<br>• offers planning only once the kit is on main. | #9 |
| UI-006 | Start your team. The page registers the reviewer `NAME-r` as the page's third human act: main checkout only, claims read before and after, self-grant and retired identities refused. It shows one exact Copy command per agent: Claude Code claims and starts in its worktree, and Codex reviews as `NAME-r`. The commands are built only from server values, start with `UAK_HUMAN=`, and were verified on Windows Git Bash. | #16 |
| UI-007 | The journey bar (Install → Prepare → Plan → Start the team → Follow progress) stays visible, and focus moves to the next step. The typed approval says what to type. In Spanish, the gate lines and the whole Advanced dashboard are translated. A warning appears when someone else's Git or GitHub identity would sign the work. | #17 |
| UI-008 | Claude Code ignores a new folder's permissions until it is trusted once: the page shows the exact `cd 'FOLDER' && claude` command before planning, names that cause when a run fails on it, and the planner reads with its Read tool. Found in user-simulation test rounds. | #19 |
| UI-010 | A planning run that wrote no TASKS.md is a failed plan, never a passing one; the page shows elapsed time and the last output while planning; the event schedule is never guessed (empty fields, confirm when the freeze is near). Tool runs never leave a process in the project folder (Windows Job Object). | #21 |
| UI-009 | The team step for every person: pick the role of each coding tool you have (Claude Code alone can implement and review with two identities); reviewer state per project and name, read from claims; the Codex reviewer gets write access to `.git`; the step survives the first claim; network Git runs outside the server lock; offline and unrelated-history ways out. | #23 |
| UI-012 | The identity warning checks the Git name/email and the GitHub login separately and only matches the person's whole name (case and accents ignored); no English left in the Spanish journey; a never-seen human shows "never"; the Agents tab lists the registered reviewer. | #24 |
| UI-015 | Windows follow-ups of UI-010 found on a real Windows machine: one grace period for both pipe readers, tests read Git output as UTF-8, the symlink case is skipped without symlink privilege. | #26 |
| UI-016 | A 74 s demo video (English and Spanish) from zero to a finished project ships with the kit (`.uak/media`) and is shown in the README. | #25 |
| UI-017 | The setup page's welcome screen offers the demo video in the page's language (no autoplay, captions, keyboard). | #27 |
| UI-018 | The setup page always says what it is doing, why a button is blocked and what changed: busy state and a result line next to every action, blocked buttons explain themselves (and a toast on out-of-order clicks), no layout shift while polling, and the page points to its own control when the gate's next step is something it can do. | #29 |

### Engine, tests and CI

| Task | What it fixes | Fork PR |
|---|---|---|
| UAK-009 | `test_tokens_coverage` waits for the hooks' background publish (Windows WinError 32). | #4 |
| UAK-010 | A partial install is never reported as installed (`.uak/INSTALLING` marker). | #6 |
| UAK-011 | Claude-only shared skills stay in sync. | #10 |
| UAK-012 | Tests no longer depend on the machine's usage pace or a global `core.hooksPath`. | #13 |
| UAK-013 | The session-start hook answers within 3 s; slow work runs in the background. | #11 |
| UAK-068 | Session start launches 15 processes instead of 41 (Windows stays under 3 s). | #14 |
| UAK-067 | CI runs the full matrix once per SHA: pull_request, push to main, and workflow_dispatch. Newer pushes cancel older PR runs. A `kit_lint` check keeps the duplication from coming back. | #15 |
| UAK-069 | `uak next` never offers implementation work to a registered reviewer identity; `claims_diff.py` asserts the new reviewer output instead of dropping the step. | #20 |
| UAK-090 | Pull requests run a light CI (Ubuntu + Windows); `main` and workflow_dispatch keep the full matrix with macOS, whose arm64 runners kept approved PRs waiting for hours. | #22 |

**Note on IDs.** Fork task IDs UAK-009..013 and UAK-067..069 collide with different upstream tasks of the same numbers. The owners should agree on a prefix before more fork work lands.

**Tests.** New test files: `test_setup_prepare.py`, `test_setup_team.py`, `test_setup_guide.py`, `test_ci_once.py`, `test_hook_session_start_speed.py`, `test_setup_trust.py`, `test_next_reviewer.py`, `test_ci_light.py`, `test_setup_roles.py`, `test_setup_feedback.py`, and the earlier UI files. Results:
- kit_lint shows 0 findings; gen_harness and known-files are current.
- Every task's own PR CI passed (ubuntu and Windows; macOS when GitHub had runners). On the fork's `main`, Windows HTTP tests occasionally time out (a known intermittent, rerun green); it is tracked as a follow-up.

**Status of this PR.** Ready for review. The fork's `main` contains all twenty-four tasks above, its CI is green on the full matrix, and it is synced with this repository's `main` (up to UAK-082, fork PR #30), so this PR merges without conflicts.

**Not yet verified.** A real Codex run as the reviewer inside Windows Git Bash (the commands were verified with Claude Code on Windows and with Codex on macOS). The project's human accepted shipping without it; it is listed as a follow-up.
