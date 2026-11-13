# Backlog published on claims (uak plan)

Append-only; added to .uak/TASKS.md from main. Why: adding tasks never waits for a PR.
## UI-001 · Configure a new project in a local browser from step zero

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_wizard.py
- **Acceptance:** An explicit wizard entry point opens a local browser before asking for installation choices; existing scripted installs and updates remain compatible., Guide repository selection, prerequisites, an explicit sprint or marathon decision, coding tools, installation review, installation progress, and subsequent project configuration in one interface., Reuse the existing installer with literal argument arrays and no shell interpolation; validate options before running it. Prevent duplicate concurrent installs., Distinguish installation success from readiness to claim a task. Reuse uak start checks; show blockers and the next corrective action. Do not manufacture approvals, credentials, tasks, or agent identities., Serve only explicit assets on 127.0.0.1. Validate Host, Origin, session token, JSON schema, and body size for mutations. Do not expose repository files, environment variables, or arbitrary command execution., Persist only explicitly allowed project settings atomically, preserving unrelated content. Approval and review authority are outside the browser write API., The UI renders offline with actionable empty, loading, and error states. Keep technical output in an expandable details panel.
- **Tests:** wizard_starts_before_installation, legacy_install_remains_noninteractive, invalid_requests_cannot_mutate, installer_arguments_are_literal, duplicate_install_is_rejected, setup_preserves_unrelated_settings, installed_is_not_ready
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py`
- **Next step:** write failing behavior tests and record uak red before implementation; agree the wizard contract with the reviewer.

## UI-002 · Make the dashboard approachable with a beginner profile

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/tests/test_dashboard_profiles.py
- **Acceptance:** Offer Beginner and Advanced presentation profiles with a persistent, reversible choice. Neither profile changes permissions, operational mode, or coordination gates., Beginner presents project status, one next action, tasks in plain language, and a short explanation of the workflow. Advanced preserves access to the existing detailed dashboard., The welcome screen explains the kit and first action without requiring knowledge of claims, worktrees, or command names., Use consistent visual tokens, visible system status, recognition rather than recall, progressive disclosure, inline error recovery, and explicit action outcomes., Keyboard navigation, visible focus, labelled controls, reduced motion, readable contrast, and 390px layouts work. Render all untrusted content as text., Preserve offline static dashboard export, dark/light themes, task/review information, and existing dashboard contracts.
- **Tests:** beginner_profile_persists, advanced_profile_preserves_details, next_action_matches_real_state, hostile_content_is_text, static_dashboard_remains_offline
- **Verify:** `python kit/.uak/tests/test_dashboard_profiles.py`
- **Next step:** inspect existing dashboard rendering and collect baseline screenshots; write failing profile tests.

## UI-003 · Verify the full visual setup journey and document it

- **Type:** integration
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001, UI-002
- **Paths:** kit/.uak/tests/test_dashboard_journey.py, docs/specs/dashboard-onboarding/, docs/DASHBOARD.md, README.md, CHANGELOG.md, kit/.uak/docs/WHY.md, kit/.uak/settings/known-files.txt
- **Acceptance:** Exercise clean setup, existing installation, interrupted/failed installation, missing prerequisites, and readiness blockers using disposable local Git fixtures., Capture real browser evidence at 1280x720 and 390x844 for welcome, wizard, beginner dashboard, advanced dashboard, and an error state; include keyboard and reduced-motion checks., Document the visual entry point, prerequisites, terminal fallback, Beginner versus Advanced, and the difference between Installed and Ready., Record the user's usability problem as evidence in WHY.md and add a changelog entry. Regenerate known-file hashes after payload changes., Run kit lint, generation checks, the complete package smoke, and relevant MCP regression tests. Report platform verification honestly; CI verifies other operating systems., claude-Dylan independently runs Verify and records a verdict on the exact pushed SHA. A later code change requires review of the new SHA. Dylan retains the final merge decision.
- **Tests:** new_project_visual_setup_journey, interrupted_install_can_recover, missing_prerequisites_remain_actionable
- **Verify:** `python kit/.uak/tests/test_dashboard_journey.py`
- **Next step:** review the dependent task evidence and implement end-to-end tests before declaring the journey complete.
## UI-004 · Plan the project in the local interface, with the human's approval there

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001
- **Paths:** kit/.uak/bin/lib/planning.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_planning.py, kit/.uak/docs/WHY.md
- **Acceptance:** A "What are you building?" form collects the one-line idea, who it is for, the judging rubric (sprint) or the spec goal (marathon), the event length and the team size. It saves `IDEA.md` as plain text, preserving an existing file only after an explicit overwrite confirmation., "Create the plan" starts the project's own coding tool in the background with a fixed, allowlisted argument array per harness (no user text in the argument list; the agent reads IDEA.md). Only harnesses installed in the project and found on the machine are offered. Never pass permission-bypass flags; the project's harness settings apply. One planning run at a time; output stays in Technical details., The planner prompt is a constant: run /uak-plan, write `.uak/TASKS.md` and `.uak/OWNERS.md`, run `uak graph` and `uak lint`, then stop. It never sets Backlog-Approved, commits or pushes., The proposed plan renders as readable cards (ID, title, priority, wave, dependencies, tests in plain words) plus the lint result. "Ask for changes" sends the human's note through a file and reruns the planner; untrusted plan text renders as text., "Approve and publish" is the human's act inside the interface: a two-step confirmation that requires typing the project name; it sets `Backlog-Approved: yes`, commits only the plan files (IDEA.md, .uak/TASKS.md, .uak/OWNERS.md, .uak/PROJECT.md) as the local Git identity with the approver recorded in the message, and pushes to the base branch. It refuses when lint fails, other files are staged or dirty in those paths, or the push is rejected, with the exact recovery., The approval endpoint keeps every UI-001 protection (loopback, Host, Origin, session token, JSON schema, body limit) and is the only browser write that touches human authority. WHY.md records the rule and its evidence (the human asked to keep the terminal in the background, Nov 2026)., After approval, readiness is rechecked with `uak start`, and the interface moves to project progress with the next action.
- **Tests:** idea_is_saved_as_plain_text, planner_command_is_fixed_and_literal, planner_never_approves_or_pushes, duplicate_planning_is_rejected, approval_requires_typed_confirmation, approval_commits_only_plan_files, approval_refuses_failing_lint
- **Verify:** `python kit/.uak/tests/test_setup_planning.py`
- **Next step:** write the failing tests with a fake planner and a local bare remote; agree the planner prompt and the approval contract with the reviewer.
## UAK-009 · test_tokens_coverage waits for the hooks' background publish before cleaning up

- **Type:** bug
- **Priority:** P1
- **Estimate:** 45 min
- **Depends on:** None
- **Paths:** kit/.uak/tests/test_tokens_coverage.py
- **Acceptance:** `hooks_publish_from_session_start_and_codex` does not return while the `nohup bash .uak/bin/tokens --publish` started by `hook session-start` and the Codex `hook tick` (`.uak/bin/hook` `tokens_publish`) is still running in the fixture's worktree: it waits, bounded (60 s at most), for that publish to finish and fails with a clear message if it never does., The temporary folder is removed only after every background publisher has exited; no test is weakened, skipped or retried to pass., Evidence: Windows CI failed twice on PR #3 with `PermissionError: [WinError 32]` and `[WinError 5]` on `uak-tokens-coverage-*\tk-hooks\worktree-1` during `TemporaryDirectory` cleanup (runs 43030820800 and 43036311089); a rerun passed with the same code. The background publish is intentional (hook.sh: a Mac that never reached Stop never published), so the fix belongs in the test., `bash .uak/bin/smoke --package-only` exits 0, and the Windows job `test_tokens_coverage` passes on three consecutive runs of the same SHA.
- **Test-First:** no (the change is the test itself; the failure is a Windows-only timing race that macOS and Linux cannot reproduce on demand)
- **Verify:** `python kit/.uak/tests/test_tokens_coverage.py`
- **Next step:** in hooks_publish_from_session_start_and_codex, after each hook call wait until the background `tokens --publish` has finished (its result on the fixture's claims remote, or no publisher left) before returning.
## UAK-010 · A partial install is never reported as installed

- **Type:** bug
- **Priority:** P1
- **Estimate:** 1.5 h
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/tests/test_setup_wizard.py
- **Acceptance:** Reproduction (found by UI-003's journey tests, Nov 2026): a file named `.claude` blocks a folder the kit needs; `install.sh` copies `.uak/` and `.uak/VERSION` early (line 129) and fails later writing `.claude/`. The running setup server says installed=false only because it remembers the failed target in memory; a new `install.sh --wizard` (or any fresh setup server) inspects the same folder and reports it installed, because `kit_present` only checks `.uak/PROJECT.md`, `.uak/bin/uak` and `.uak/VERSION`., The installer marks an install complete only after every step succeeded (for example, `.uak/VERSION` written last, or a completion stamp the installer removes at start and writes at the end); an interrupted or failed install, including `--update`, leaves the project visibly incomplete on disk., A fresh setup server on that folder reports installed=false, offers Repair or update with the reason, and `/api/check` refuses with the same actionable message; after the blocking file is moved, Repair reaches installed and the person's file is unchanged., A complete install and an `--update` of an older complete install are still reported installed (no regression for existing projects, including ones installed before this change)., `bash .uak/bin/smoke --package-only` exits 0; known-files are regenerated if an installed file changes.
- **Tests:** partial_install_is_not_installed_after_restart, failed_update_stays_incomplete, complete_install_is_still_installed
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py`
- **Next step:** in test_setup_wizard.py, install with a `.claude` file blocking the folder, then inspect the target with a NEW server (make_server) and assert installed is false; see it fail (uak red), then make the installer mark completion last.
## UI-005 · Prepare the project from the page, never only in a terminal

- **Type:** feature
- **Priority:** P0
- **Estimate:** 1 day
- **Depends on:** UI-004
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/planning.py, kit/.uak/tests/test_setup_prepare.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (hackathon simulation, 2026-11-11, notes/handoff:PENDING-IMPROVEMENTS.md #5, #6 and #8 to #10, plus #12): the next action lived only in Technical details, the person thought the page was still loading, and the gate's own push command would have published the unapproved plan files., An "Event schedule" form (start, end, time zone, with sensible defaults) writes Freeze-Epoch exactly as `uak clock START DEADLINE ZONE --write` does, and shows the computed freeze and the first-claim time., "Publish the kit to main" is a human act in the page with a confirmation that lists the files: it commits the installed kit and configuration WITHOUT IDEA.md, .uak/TASKS.md and .uak/OWNERS.md, as the local Git identity, on a branch equal to origin/main (or an empty remote), and pushes the verified commit; it refuses with the exact recovery otherwise. It keeps every UI-001 protection., Any step that can only happen outside the browser is shown as a clear "Do this in a terminal" box: which terminal, the `cd` into the project, the exact command with Copy, and "come back and press Check again". The next action is never only in Technical details., Planning is offered only once the kit is on main; before that, the planning section says why and points to the publish step., When lint fails for a reason that is not a `LINT:` line (GIT_ERROR, missing main, network), the page shows that reason in plain words with how to fix it., "Check the plan again" reruns the server's verification and lint on the current files without running the planner., The page asks once for the human's name and uses it for every human act that needs one (UAK_HUMAN); it is never typed into a command., WHY.md records the new human acts (publishing the kit from the page) with the simulation as evidence; docs/DASHBOARD.md is updated.
- **Tests:** schedule_form_writes_freeze_epoch, publish_kit_excludes_unapproved_plan_files, publish_kit_pushes_only_the_verified_commit, terminal_step_is_shown_with_its_command, planning_waits_for_the_kit_on_main, lint_failure_reason_reaches_the_page, plan_can_be_rechecked_without_the_planner, human_name_is_asked_once
- **Verify:** `python kit/.uak/tests/test_setup_prepare.py`
- **Next step:** write the named tests with a local bare remote (empty, then with main) and the real `uak clock` and `uak lint`; see them fail (uak red); then add the schedule and publish endpoints to setup.py.

## UI-006 · Start the team from the page

- **Type:** feature
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UI-005
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_team.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (hackathon simulation, notes/handoff:PENDING-IMPROVEMENTS.md #11 and #14 to #16): the person asked which terminal runs Claude or Codex, and needed the worktree `cd`, the MCP approval, the first prompt, the reviewer env vars and `$uak-review` explained., After Ready, a "Start your team" step in the page: (a) "Register the reviewer" is one button (a human act using the name from UI-005; it runs `uak register-reviewer NAME-r`), (b) one Copy command per agent that claims, enters the worktree and starts the tool with its first prompt (Claude Code implements; Codex reviews as NAME-r with `$uak-review`), each labelled with the terminal it goes in, (c) a line saying setup steps need no agent., Commands are exact and literal: only allowlisted task IDs and names validated by the server; no user text is interpolated unchecked., The Advanced view also shows the next step and its Copy button., Choosing coding tools explains the roles (one implements, one reviews as a second identity) and recommends Claude Code + Codex; "I'm the only human on this repository" says in plain words what it changes., WHY.md records the reviewer registration from the page; docs/DASHBOARD.md is updated.
- **Tests:** reviewer_is_registered_from_the_page, agent_launch_commands_are_exact, advanced_view_shows_the_next_step, tool_roles_are_explained
- **Verify:** `python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests against a ready fixture project; see them fail; then add the team step.

## UI-007 · A guided journey a new user can follow without the README

- **Type:** feature
- **Priority:** P1
- **Estimate:** 4 h
- **Depends on:** UI-006
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html, kit/.uak/tests/test_setup_guide.py, docs/DASHBOARD.md, CHANGELOG.md
- **Acceptance:** Evidence (hackathon simulation and PR chat, notes/handoff:PENDING-IMPROVEMENTS.md #2, #7, #13 and #17 to #20)., The welcome screen shows the whole journey and keeps it visible: Install → Prepare → Plan → Start the team → Follow progress, each marked "in this page", "in a terminal" or "your agents do it", with the current one highlighted. It says the page installs the kit INTO the project and that the kit itself is only downloaded once., The typed approval shows the exact folder name as a placeholder and, under the disabled button, "Type NAME to enable publishing"., When a step completes, the page moves the person to where the next one happens (for example, to "Plan your project")., In Spanish, the readiness gate's lines are translated (or a translated summary is shown above them), and the Advanced dashboard has no English labels left; the notice under the title no longer repeats the heading., The page warns when the logged-in Git/GitHub identity will sign the commits and PRs (another person's machine)., Keyboard, visible focus, reduced motion and 390px layouts keep working; docs/DASHBOARD.md and CHANGELOG.md are updated.
- **Tests:** journey_is_visible_from_welcome, approval_field_says_what_to_type, gate_lines_are_translated, advanced_dashboard_is_translated, shared_identity_is_warned
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests (markup and catalog contracts plus HTTP checks); see them fail; then build the journey stepper.
## UAK-011 · A Claude-only install passes doctor

- **Type:** bug
- **Priority:** P1
- **Estimate:** 1 h
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/doctor, kit/.uak/tests/test_install_claude_only.py
- **Acceptance:** Reproduction (notes/handoff:PENDING-IMPROVEMENTS.md #21, reproduced on main 2026-11-11): `install.sh --mode sprint --harness claude .` in a fresh repo, then `bash .uak/bin/doctor` fails with ".agents/skills is a stale copy of .claude/skills"; with `--harness claude,codex` it passes. A new user who picks only Claude Code is blocked at the readiness gate's preflight., After a Claude-only install, doctor reports no stale-skills failure (either .agents/skills is not created when no harness reads it, or it is a faithful copy; doctor and install.sh agree on which)., A multi-harness install (claude,codex and claude,cursor) still keeps .agents/skills in sync, and doctor still reports a copy that is really stale., `bash .uak/bin/smoke --package-only` exits 0.
- **Tests:** claude_only_install_passes_doctor_skills_check, multi_harness_install_keeps_agents_skills_in_sync, really_stale_copy_is_still_reported
- **Verify:** `python kit/.uak/tests/test_install_claude_only.py`
- **Next step:** reproduce in the test with install.sh into a temp repo with `--harness claude`, assert doctor has no stale-skills FAIL, see it fail (uak red).

## UAK-012 · Two tests stop depending on the machine they run on

- **Type:** bug
- **Priority:** P2
- **Estimate:** 1 h
- **Depends on:** None
- **Paths:** kit/.uak/tests/test_v3.py, kit/.uak/tests/test_tokens_coverage.py, kit/.uak/tests/test_hack.py
- **Acceptance:** Evidence (notes/handoff:PENDING-IMPROVEMENTS.md #3 and #4, Dylan's Mac, 2026-11-11): `test_v3::guard_subagent_budget` reads the machine's real usage pace ("pace critical" lowers Max-Parallel-Subagents to 1) and fails on main; `test_tokens_coverage::publish_failure_is_recorded` fails when `~/.gitconfig` sets `core.hooksPath`, because the test remote's pre-receive hook is skipped., Both tests pass on a machine with a critical pace and a global core.hooksPath, without weakening any assertion: the fixtures pin the pace input and the hooks path (for example through the test runner's environment), they do not skip or relax the checks., The tests still fail when the guard or the publish-failure path is broken.
- **Tests:** guard_budget_ignores_the_machine_pace, publish_failure_is_recorded_under_a_global_hooks_path
- **Verify:** `python kit/.uak/tests/test_v3.py`
- **Next step:** write each new test so it sets a critical pace / a global core.hooksPath for its own fixture and see it fail on main; then pin those inputs in the fixtures.

## UAK-013 · The session-start hook answers within 3 seconds

- **Type:** bug
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/hook, kit/.uak/tests/test_hook_session_start_speed.py
- **Acceptance:** Evidence (Claude Code /doctor on Dylan's Mac, 22 sessions over 18 days, 2026-11-11): the kit's SessionStart hook took about 9.5 s typical on startup, 12.6 s typical on resume and up to 28 s, blocking the start of every session in a project with the kit., `hook session-start` returns within 3 s on a fixture with a local bare remote; network or slow work (publishing tokens, black box flush, map build, inbox reads) runs in the background or is skipped when fresh, as tick already does., What session-start shows the agent (identity, task, inbox summary) stays correct and complete., `bash .uak/bin/smoke --package-only` exits 0.
- **Tests:** session_start_returns_within_budget, session_start_output_is_unchanged
- **Verify:** `python kit/.uak/tests/test_hook_session_start_speed.py`
- **Next step:** measure `hook session-start` on a fixture, find the synchronous slow steps, write the timing test (budget 3 s) and see it fail.
## UAK-067 · CI validates each SHA once and cancels obsolete runs

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1.5 h
- **Depends on:** None
- **Paths:** .github/workflows/test.yml, scripts/kit_lint.py, kit/.uak/tests/test_ci_once.py, kit/.uak/docs/WHY.md
- **Acceptance:** Evidence (notes/handoff:PENDING-IMPROVEMENTS.md #24; 2026-11-12): every feature SHA ran the full 86-check matrix twice (push and pull_request, 172 checks, 8 macOS jobs); with GitHub's macOS arm64 capacity short, UAK-013's last macOS job was cancelled about 7 times with 0 steps and a ready task waited ~2 h, and UI-005's PR run the same., The full matrix (discover, the Linux and macOS shards, every Windows file) runs once per feature SHA, on pull_request; pushes to main still run it in full after every merge, and workflow_dispatch can run it on demand. No check is dropped and the matrix is unchanged., A newer push to the same pull request cancels its older in-progress runs (concurrency by pull request number); runs on main are never cancelled., `kit_lint.py` fails when test.yml runs the full suite on both push to any branch and pull_request, or when pull_request runs lack cancel-in-progress concurrency, so the duplication cannot come back unnoticed., WHY.md records the rule and Dylan's decision of 2026-11-12: a SHA whose one complete run is all SUCCESS may be shipped when the other run's only non-success jobs are runner-capacity cancellations (cancelled, 0 steps, "not acquired by Runner"); real failures never ship., `bash .uak/bin/smoke --package-only` exits 0.
- **Tests:** ci_runs_the_matrix_once_per_sha, obsolete_pull_request_runs_are_cancelled, main_keeps_its_full_run
- **Verify:** `python kit/.uak/tests/test_ci_once.py`
- **Next step:** write test_ci_once.py so it reads ../.github/workflows/test.yml (skip when absent, as in an installed project) and calls kit_lint's new check; see it fail on main; then change the triggers and add the concurrency block.

## UAK-068 · Session start launches half as many processes, so Windows stays under 3 seconds

- **Type:** bug
- **Priority:** P0
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/hook, kit/.uak/tests/test_hook_session_start_speed.py
- **Acceptance:** Evidence (notes/handoff:PENDING-IMPROVEMENTS.md #29, 2026-11-12): `session_start_returns_within_budget` failed on GitHub's Windows runners at 3.1-3.2 s against the 3 s budget (main a5f38f1 push run 43258148086; UAK-012 2a8f99f push run) while the same SHAs passed in their pull_request runs; it decides by luck whether a SHA is green. Counted on the test's fixture (slow 3 s remote, one claimed task) with counting shims on PATH, `hook session-start` launched 206 external processes on startup and 139 on resume (45-74 git, 15-33 awk, 11-12 sleep), and a Git Bash process costs 20-50 ms on Windows., The processes launched before `hook session-start` returns are counted deterministically by the test (shims on PATH, independent of runner speed) and are at most half of today's count on both startup and resume; background refreshes still run and still finish., The 3 s wall-clock budget is unchanged, and what session-start shows (identity, task, inbox summary, refresh notes) is unchanged: every existing case of test_hook_session_start_speed and test_hook_claims passes as is., No existing assertion changes; only new tests are added., `bash .uak/bin/smoke --package-only` exits 0.
- **Tests:** session_start_launches_half_the_processes_on_startup, session_start_launches_half_the_processes_on_resume
- **Verify:** `python kit/.uak/tests/test_hook_session_start_speed.py`
- **Next step:** add the counting shims to the test and assert the halved bound on startup and resume; see both fail on main; then remove repeated git/awk calls on the foreground path (batch git reads, use builtins, fewer polling sleeps) until they pass.
## UI-008 · Agents in a new folder do not stall on workspace trust

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/planning.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_trust.py, kit/.uak/docs/WHY.md, README.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (test rounds 2026-11-13, notes/handoff:qa/rounds-2026-11-13/SUMMARY.md #1): in a new folder Claude Code ignores .claude/settings.json allow rules until the folder is trusted interactively ("workspace has not been trusted"); the headless planner failed on its first command (r3 run 1), implementers stopped asking approvals (r1, r3), and the README never says it (r2)., The page and README tell the person, before planning and in the team step, to open Claude Code once in the project folder and accept trust (with the exact command)., When a planning run's output contains the "not been trusted" line, the page shows that cause and the trust step instead of a generic failure., The planner reads project files with its Read tool and a denied read is not fatal to the run., WHY.md records the incident; docs/DASHBOARD.md is updated; Spanish and English texts exist for every new line.
- **Tests:** trust_step_is_shown_before_planning, untrusted_planning_run_names_the_cause, planner_survives_a_denied_read
- **Verify:** `python kit/.uak/tests/test_setup_trust.py`
- **Next step:** write the named tests with a fake planner that prints the trust line; see them fail; then add the trust guidance and detection.

## UI-009 · The team step stays right after the first claim

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** UI-008
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #2, #3, #5): state["reviewer"] is server-wide, so another project, another name or a retired reviewer shows "registered" (r4); the Codex reviewer command lacks the `--add-dir "<repo>/.git"` that wt recommends and `uak next` fails under its sandbox (r1, r3); after the first claim the page leaves "ready", the team commands vanish (r4) or it keeps offering the claimed task (r3)., "Registered" is derived per project and reviewer name from claims (roles/reviewers minus meta/retired), never from a server-wide flag., The Codex reviewer command grants write access to the repository's .git directory, quoted for the folder., After claims exist the team step stays visible: it offers an unclaimed task for a new implementer, a resume command for each claimed one, and the reviewer command.
- **Tests:** reviewer_state_follows_project_and_name, codex_command_can_write_git, team_step_survives_the_first_claim
- **Verify:** `python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests against the ready fixture with a claim on HACK-001; see them fail; then fix the reviewer state and the commands.

## UI-010 · Planning and schedule never pretend

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** UI-009
- **Paths:** kit/.uak/bin/lib/planning.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_planning.py, kit/.uak/tests/test_setup_prepare.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #6, #7): a planning run that wrote no TASKS.md showed a green "plan passes uak lint" and an approve button (r3); planning took 4 to 8 minutes with no progress cue (r1); the event schedule defaults to today and saving it untouched silently froze a next-day hackathon (r1)., A run without .uak/TASKS.md is shown as failed (translated message, retry button, no lint line, no approve button)., While planning runs the page shows elapsed time and the last output line., The schedule fields start empty; saving requires a date, and a freeze time in the past or within the next hour asks for confirmation.
- **Tests:** missing_tasks_file_is_a_failed_plan, planning_shows_progress, schedule_is_never_guessed
- **Verify:** `python kit/.uak/tests/test_setup_planning.py && python kit/.uak/tests/test_setup_prepare.py`
- **Next step:** write the named tests with a fake planner that exits without writing TASKS.md; see them fail; then fix the plan view and the schedule form.

## UI-011 · The page answers while Git talks to the network, and publishing has no dead end

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** UI-010
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_prepare.py, kit/.uak/tests/test_setup_team.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository.
- **Tests:** status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out
- **Verify:** `python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests with a fake runner that blocks on ls-remote; see them fail; then move network calls out of the lock.

## UI-012 · Identity warning compares Git and GitHub separately

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** UI-011
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_guide.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #8; PENDING-IMPROVEMENTS.md #44): one matching word suppressed the warning when Git matched the person but GitHub was someone else (r4); accented names did not match their unaccented form., The warning checks the Git name/email and the GitHub login each against the person's name and says which one belongs to someone else., Names match ignoring case and accents (José = jose).
- **Tests:** github_login_is_checked_on_its_own, accents_do_not_break_the_match
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests with a fake identity (Git = person, gh = other); see them fail; then split the check.

## UI-013 · No English left in the Spanish journey, and small honesty fixes

- **Type:** fix
- **Priority:** P3
- **Estimate:** 3 h
- **Depends on:** UI-012
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/status.sh, kit/.uak/tests/test_setup_guide.py, kit/.uak/tests/test_next_reviewer.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #10)., In Spanish the status heading, the doctor sub-lines, the schedule weekday, the claim progress line ("N commit(s) since the claim · last: …") and "No technical output yet" are translated, and the status heading has no ✓ while TODOs remain., A human never seen shows "never", not "20770 d"; the Agents tab lists the registered reviewer., The plan's Approved-By and the kit's Published-By use the same human name., `uak next` run as a registered reviewer offers reviews only, never implementation work.
- **Tests:** spanish_journey_has_no_english, never_seen_human_is_named, reviewer_is_not_offered_implementation
- **Verify:** `python kit/.uak/tests/test_setup_guide.py && python kit/.uak/tests/test_next_reviewer.py`
- **Next step:** write the named tests (rendered Spanish page text, a uak next run as NAME-r); see them fail; then translate and fix.
## UI-014 · Each person picks the role of each coding tool they have

- **Type:** feature
- **Priority:** P1
- **Estimate:** 4 h
- **Depends on:** UI-009
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_roles.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan, after the test rounds 2026-11-13): the team step always says "Claude Code implements, Codex reviews", but many people have only one subscription (only Claude or only Codex) and could not follow it; the engine already lets any tool take either role (a role is only an identity: UAK_AGENT)., For each coding tool installed in the project and signed in on this computer (the same detection planning uses), the person picks its role: implements, reviews, or both., With one tool, it can do both roles with two identities (TOOL-NAME implements, NAME-r reviews), and the page says the reviewer never reviews its own identity's work., With two tools, any combination works (for example Codex implements and Claude Code reviews); the choice is per person and remembered for the project (not shared with teammates)., The Copy commands follow the choice: the implement command opens the chosen tool in the task worktree with its first prompt, the review command starts the chosen tool as NAME-r with its review prompt (Claude Code: /uak-review; Codex: $uak-review, with --add-dir for .git); commands stay built only from server values., A tool not installed or not signed in is never offered, and the page says why; WHY.md and docs/DASHBOARD.md are updated, with Spanish for every new line.
- **Tests:** roles_follow_the_tools_you_have, one_tool_does_both_roles, any_tool_can_review, unavailable_tool_is_not_offered
- **Verify:** `python kit/.uak/tests/test_setup_roles.py`
- **Next step:** write the named tests with fake tools (only claude, only codex, both); see them fail; then add the role choice to the team step.
## UAK-069 · uak next never offers implementation work to a reviewer identity

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/status.sh, kit/.uak/tests/test_next_reviewer.py, kit/.uak/docs/WHY.md, CHANGELOG.md
- **Acceptance:** Evidence (test rounds 2026-11-13, notes/handoff:qa/rounds-2026-11-13/r3-REPORT.md P3-6): `UAK_AGENT=luis-r uak next` offered HACK-001 for implementation to the registered reviewer identity., Run as an identity registered on claims roles/reviewers (and not retired), `uak next` offers only tasks waiting for review (or says there is nothing to review and how to wait), never AVAILABLE tasks to claim., An identity that is not a reviewer sees exactly the output it saw before (the protocol suites stay green)., WHY.md records the incident.
- **Tests:** reviewer_is_not_offered_implementation, implementer_output_is_unchanged
- **Verify:** `python kit/.uak/tests/test_next_reviewer.py`
- **Next step:** write the tests with a real Git fixture and bare remote (a registered NAME-r, one AVAILABLE task); see them fail; then filter next by role.
