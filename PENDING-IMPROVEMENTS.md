# Pending improvements (not planned yet)

Ideas found while building and testing the visual setup. None is a task yet: Dylan decides which become one
(`UAK_HUMAN=Dylan bash .uak/bin/uak plan FILE`). Ask claude-Dylan "¿hay mejoras pendientes?" to review this list.

| # | Improvement | Why / evidence | Found |
|---|---|---|---|
| 1 | A command to reopen the setup page from an installed project (e.g. `bash .uak/bin/uak setup`) | Today the page only starts from the kit's clone (`install.sh --wizard`); an installed project has `.uak/bin/lib/setup.py` but no command for it. A teammate (Joahan) asked whether the kit must be installed to run the installer. | 2026-11-11, PR review chat |
| 2 | Translate the Advanced dashboard and remove the repeated status text | In Spanish, parts of the detailed panel stay in English ("Agents online", "0 of 4 tasks integrated"), and the notice under the title repeats "Tu proyecto de un vistazo". | 2026-11-11, demo video |
| 3 | Make `test_v3::guard_subagent_budget` hermetic | It reads the machine's real usage pace ("pace critical" lowers Max-Parallel-Subagents to 1), so it fails on Dylan's Mac and on main alike. | 2026-11-11, UI-002 smoke on macOS |
| 4 | Local test runs under a global `core.hooksPath` | `test_tokens_coverage::publish_failure_is_recorded` fails when `~/.gitconfig` sets `core.hooksPath` (the test remote's pre-receive hook is skipped). Tests could pin `core.hooksPath` in their fixtures. | 2026-11-11, UI-002 smoke on macOS |

## From the hackathon simulation (2026-11-11, project turno-cafeteria)

**Goal (Dylan):** a new user installs, configures and starts a hackathon with the kit without reading the README and
without asking anyone. In the simulation Dylan needed help at almost every transition: what to do after installing,
which terminal runs what, whether terminal 2 is for Claude or Codex, what to type in the confirmation, how to start
the agents, and why the page "looked like it was loading" while nothing ran. Each row below is one of those moments.

### P0 · The page must never leave the person without the next action

| # | Improvement | Evidence in the simulation |
|---|---|---|
| 5 | Do the gate's terminal steps from the page: an "Event schedule" form (start, end, time zone) that writes Freeze-Epoch (what `uak clock --write` does), and a "Publish the kit to main" button (a human act with confirmation) that commits the kit WITHOUT IDEA.md, .uak/TASKS.md, .uak/OWNERS.md and pushes. | Dylan saw the TODO lines in Technical details, thought the page was still working, and asked "is it running in some terminal?". The gate's own command (`git add -A && …`) would also have pushed the unapproved plan files: we had to hand-write a `git add` that excludes them. |
| 6 | When a step can only happen outside the browser, show a clear "Do this in a terminal" box: which terminal, the `cd` into the project, the exact command with Copy, and "come back and press Check again". Never only text inside Technical details. | The next action was only visible in Technical details (TODO 3/4); nothing told him to open a terminal. |
| 7 | Show the whole journey on the welcome screen and keep it visible: Install → Prepare (schedule, publish kit) → Plan → Start the team → Follow progress, each marked "in this page", "in a terminal" or "your agents do it", with the current one highlighted. | He could not anticipate the steps or know how far he was. |
| 8 | Planning waits for the earlier gate steps (kit published to main), or does them first. Planning before that fails lint with no explanation. | Planned before the push: lint failed with `GIT_ERROR: … couldn't find remote ref refs/heads/main`. |
| 9 | Show the real reason when lint fails: lint output that is not a `LINT:` line (GIT_ERROR, network, missing main) must reach the page in plain words with how to fix it. | The page said "the kit's checks found problems" with an empty list. |
| 10 | "Check the plan again" without rerunning the planner (re-run the server's verification and lint on the current files). | After pushing the kit he had to create the plan again: minutes and quota for a lint that only needed main to exist. |
| 11 | A "Start your team" step after Ready, inside the page: (a) register the reviewer with one button (human act; no `UAK_HUMAN=… UAK_AGENT= …` to type), (b) one Copy command per agent that does everything (claim, cd into the worktree, start Claude Code with the right first prompt; start Codex as the reviewer with its identity and `$uak-review`), (c) which terminal each goes in, and that setup steps need no agent. | He asked "in terminal 2 should I run claude or codex?" and needed the worktree `cd`, the MCP approval, the first prompt, the reviewer env vars and `$uak-review` explained. |
| 12 | Ask once for the human's name in the page and use it everywhere a human act needs it (UAK_HUMAN, reviewer names such as `name-r`), instead of env vars in commands. | The reviewer registration and freeze exceptions need `UAK_HUMAN=…`; a new user does not know what to put. |

### P1 · Remove guesswork from each screen

| # | Improvement | Evidence in the simulation |
|---|---|---|
| 13 | Typed approval: a placeholder with the exact folder name, and a line under the disabled button saying "Type turno-cafeteria to enable publishing". | He asked "what do I have to put here?". |
| 14 | Show the next step and its Copy button in the Advanced view too (today only Beginner shows the next-step box). | After publishing the plan the page opened in Advanced, with no visible next action. |
| 15 | Explain the roles when choosing coding tools: one implements, one reviews (a second identity); recommend Claude Code + Codex and say what each will do. | The tool choice did not say why two tools matter. |
| 16 | Explain "I'm the only human on this repository" in plain words (what changes: reviews between agent identities on claims). | The meaning was unclear. |
| 17 | After a step completes, move the person to where the next one happens (for example, scroll to "Plan your project" when the gate says "a plan: no tasks yet"). | The planning form sits far below the checklist and preferences. |
| 18 | Translate the readiness gate's lines (`uak start` output: TODO/OK, preflight, push…) in the Spanish UI, or show a translated summary above them. | The Spanish page showed the gate in English. |
| 19 | Make clear on the welcome screen that the page installs the kit INTO the project, and that the kit itself is only cloned (downloaded) once. | Joahan asked: "do I install the kit to run this, and then it helps me install the kit?". |
| 20 | Warn when the person uses another person's machine/identity: commits and PRs will carry the logged-in Git and GitHub identity. | In the simulation the participant would commit as Dylan. |

### Suggested order

Start with 5, 6, 7 and 11: together they remove every terminal moment of setup except launching the agents, and turn
that one into a single Copy per agent. Then 8 to 10 (planning reliability), then the P1 rows.

### Found while building UI-005

| # | Improvement | Evidence |
|---|---|---|
| 21 | A fresh install with only Claude Code makes `doctor` fail with ".agents/skills is a stale copy of .claude/skills" (install.sh creates .agents/skills, doctor compares it); with Claude Code + Codex it passes. A new user picking only Claude Code is blocked at preflight until `bash .uak/bin/doctor --fix`. | Reproduced on main 2026-11-11 (`install.sh --mode sprint --harness claude .` then `bash .uak/bin/doctor`). UI-005's terminal box shows the fix meanwhile. |

### Found during package verification

| # | Improvement | Evidence |
|---|---|---|
| 22 | Include installer/scanner and retry-hook fixtures when making tests independent of the machine's global `core.hooksPath` (related to #4 and UAK-012). | During UAK-011, `test_v51::a_smaller_root` and `test_v54::a_retry_reuses_the_base` failed unchanged on baseline a90e820 as well as the task branch. The global hook path bypassed fixture hooks. Both passed unchanged in the complete smoke with a command-scoped isolated global Git configuration. Evidence: `/tmp/uak-011-v51-baseline.log`, `/tmp/uak-011-v54-baseline.log`, `/tmp/uak-011-smoke-isolated.log`. No out-of-scope test edits were made. |
| 23 | Add actionable diagnostics for an intermittent Windows `test_v592::guard_runs_on_builtins` failure; establish its cause before choosing a fix. | UAK-013 SHA 61e13a33cd41c13b671ac33f2f602228db57c837: [PR Windows job 130966060868](https://github.com/DylanMCDS/upiixia-agentic-kit/actions/runs/43150579787/job/130966060868) failed the forced-push assertion with `still blocked:` and empty stderr; the same file passed in the matching push run. Guard and test_v592 are byte-identical to main45cef16 and the failing call does not source the changed hook. The cause is unproven, rather than a confirmed baseline defect. Preserve return code/stdout/stderr on failure in a separately authorized task. Initial evidence: `/tmp/uak-013-ci-windows-v592-failure.log`; 171 of 172 checks passed before a single unchanged failed-job retry. |
| 24 | Avoid duplicate full CI for the same feature SHA and automatically cancel obsolete runs of that branch, while retaining complete cross-platform validation of the current SHA. | UAK-013 f281ab9 ran the same 86-check matrix twice: [push 43160279752](https://github.com/DylanMCDS/upiixia-agentic-kit/actions/runs/43160279752) and [PR 43160285307](https://github.com/DylanMCDS/upiixia-agentic-kit/actions/runs/43160285307), 172 successful checks total. Four obsolete queued UAK-013 runs had to be cancelled manually during an earlier iteration. This is avoidable duplicate work; its contribution to runner queue delays has not been established. Workflow changes are outside UAK-013 Paths and were not made. |
