# Amended tasks (uak plan --amend)

Append-only; the last section of an ID replaces its section in the backlog. Why: Paths can grow before review.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-001 · Configure a new project in a local browser from step zero

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_wizard.py, kit/.uak/tests/test_unified_workspace.py
- **Acceptance:** An explicit wizard entry point opens a local browser before asking for installation choices; existing scripted installs and updates remain compatible., Guide repository selection, prerequisites, an explicit sprint or marathon decision, coding tools, installation review, installation progress, and subsequent project configuration in one interface., Reuse the existing installer with literal argument arrays and no shell interpolation; validate options before running it. Prevent duplicate concurrent installs., Distinguish installation success from readiness to claim a task. Reuse uak start checks; show blockers and the next corrective action. Do not manufacture approvals, credentials, tasks, or agent identities., Serve only explicit assets on 127.0.0.1. Validate Host, Origin, session token, JSON schema, and body size for mutations. Do not expose repository files, environment variables, or arbitrary command execution., Persist only explicitly allowed project settings atomically, preserving unrelated content. Approval and review authority are outside the browser write API., The UI renders offline with actionable empty, loading, and error states. Keep technical output in an expandable details panel.
- **Acceptance (human clarification):** Spanish/English can be switched without losing input; configuration and the existing dashboard share one local application and persistent preferences; Back is available after Welcome, preserving inputs and preventing duplicate writes during active operations. User-facing Spanish translations are explicitly authorized; source code and contributor documentation remain English.
- **Tests:** wizard_starts_before_installation, legacy_install_remains_noninteractive, invalid_requests_cannot_mutate, installer_arguments_are_literal, duplicate_install_is_rejected, setup_preserves_unrelated_settings, installed_is_not_ready
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py`
- **Next step:** write failing behavior tests and record uak red before implementation; agree the wizard contract with the reviewer.

## UI-001 · Configure a new project in a local browser from step zero

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_wizard.py, kit/.uak/tests/test_unified_workspace.py
- **Acceptance:** An explicit wizard entry point opens a local browser before asking for installation choices; existing scripted installs and updates remain compatible., Guide repository selection, prerequisites, an explicit sprint or marathon decision, coding tools, installation review, installation progress, and subsequent project configuration in one interface., Reuse the existing installer with literal argument arrays and no shell interpolation; validate options before running it. Prevent duplicate concurrent installs., Distinguish installation success from readiness to claim a task. Reuse uak start checks; show blockers and the next corrective action. Do not manufacture approvals, credentials, tasks, or agent identities., Serve only explicit assets on 127.0.0.1. Validate Host, Origin, session token, JSON schema, and body size for mutations. Do not expose repository files, environment variables, or arbitrary command execution., Persist only explicitly allowed project settings atomically, preserving unrelated content. Approval and review authority are outside the browser write API., The UI renders offline with actionable empty, loading, and error states. Keep technical output in an expandable details panel.
- **Acceptance (human clarification):** Spanish/English can be switched without losing input; configuration and the existing dashboard share one local application and persistent preferences; Back is available after Welcome, preserving inputs and preventing duplicate writes during active operations. User-facing Spanish translations are explicitly authorized; source code and contributor documentation remain English.
- **Tests:** wizard_starts_before_installation, legacy_install_remains_noninteractive, invalid_requests_cannot_mutate, installer_arguments_are_literal, duplicate_install_is_rejected, setup_preserves_unrelated_settings, installed_is_not_ready
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py && python kit/.uak/tests/test_unified_workspace.py`
- **Next step:** write failing behavior tests and record uak red before implementation; agree the wizard contract with the reviewer.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)


## UI-002 · Make the dashboard approachable with a guided beginner profile

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/templates/PROJECT.sprint.md, kit/.uak/templates/PROJECT.marathon.md, kit/.uak/docs/CLI.md, kit/.uak/tests/test_dashboard_profiles.py
- **Acceptance:** Offer Beginner and Advanced presentation profiles with a persistent, reversible choice. Neither profile changes permissions, operational mode, or coordination gates., Beginner is almost fully guided for someone who never used the kit: one step per screen, one primary action, one sentence on why it matters, and the completed steps as a short checklist., The current step comes only from the readiness gate (`uak start`) until the project is ready, and from its ready line afterwards; Beginner never contradicts Configuration., A step that happens outside the browser shows the exact command with a Copy button and where to paste it; the browser never approves or publishes on the human's behalf outside the approval flow of UI-004., The state is rechecked automatically (on an interval and when the tab regains focus); a completed step advances and is announced politely to assistive technology., When the project becomes ready, the interface opens project progress: percentage, tasks in plain language, and the next action., No jargon (claims, worktree, command names) outside the copy block; an unavoidable term has a one-line explanation. Advanced and Technical details stay one click away from every step., Keyboard navigation, visible focus, labelled controls, reduced motion, readable contrast, and 390px layouts work. Render all untrusted content as text., A "Your app" section links to the deployed application when one exists. The URL lives in a new `Live-URL:` key of `.uak/PROJECT.md` (read with `uak_cfg`, documented in CLI.md and both templates), editable in the interface as an allowlisted setting: only an absolute `https://` URL with no credentials, saved atomically. The link opens in a new tab with `rel="noopener noreferrer"`. Without a URL, the section says the app is not deployed yet and points to the deploy step; it never guesses a URL., Preserve offline static dashboard export, dark/light themes, task/review information, and existing dashboard contracts.
- **Tests:** beginner_profile_persists, advanced_profile_preserves_details, next_action_matches_real_state, hostile_content_is_text, static_dashboard_remains_offline, beginner_shows_one_action, copy_command_is_exact, ready_opens_progress, live_url_is_https_only, live_url_link_is_shown_when_set
- **Verify:** `python kit/.uak/tests/test_dashboard_profiles.py`
- **Next step:** reuse UI-001's guidance contract (/api/status and /api/dashboard `guidance`); write failing profile tests.
## UI-002 · Make the dashboard approachable with a guided beginner profile

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/templates/PROJECT.sprint.md, kit/.uak/templates/PROJECT.marathon.md, kit/.uak/docs/CLI.md, kit/.uak/bin/lib/workspace.js, kit/.uak/settings/known-files.txt, kit/.uak/tests/test_dashboard_profiles.py
- **Acceptance:** Offer Beginner and Advanced presentation profiles with a persistent, reversible choice. Neither profile changes permissions, operational mode, or coordination gates., Beginner is almost fully guided for someone who never used the kit: one step per screen, one primary action, one sentence on why it matters, and the completed steps as a short checklist., The current step comes only from the readiness gate (`uak start`) until the project is ready, and from its ready line afterwards; Beginner never contradicts Configuration., A step that happens outside the browser shows the exact command with a Copy button and where to paste it; the browser never approves or publishes on the human's behalf outside the approval flow of UI-004., The state is rechecked automatically (on an interval and when the tab regains focus); a completed step advances and is announced politely to assistive technology., When the project becomes ready, the interface opens project progress: percentage, tasks in plain language, and the next action., No jargon (claims, worktree, command names) outside the copy block; an unavoidable term has a one-line explanation. Advanced and Technical details stay one click away from every step., Keyboard navigation, visible focus, labelled controls, reduced motion, readable contrast, and 390px layouts work. Render all untrusted content as text., A "Your app" section links to the deployed application when one exists. The URL lives in a new `Live-URL:` key of `.uak/PROJECT.md` (read with `uak_cfg`, documented in CLI.md and both templates), editable in the interface as an allowlisted setting: only an absolute `https://` URL with no credentials, saved atomically. The link opens in a new tab with `rel="noopener noreferrer"`. Without a URL, the section says the app is not deployed yet and points to the deploy step; it never guesses a URL., Preserve offline static dashboard export, dark/light themes, task/review information, and existing dashboard contracts.
- **Tests:** beginner_profile_persists, advanced_profile_preserves_details, next_action_matches_real_state, hostile_content_is_text, static_dashboard_remains_offline, beginner_shows_one_action, copy_command_is_exact, ready_opens_progress, live_url_is_https_only, live_url_link_is_shown_when_set
- **Verify:** `python kit/.uak/tests/test_dashboard_profiles.py`
- **Next step:** reuse UI-001's guidance contract (/api/status and /api/dashboard `guidance`); write failing profile tests.
## UI-003 · Verify the full visual setup journey and document it

- **Type:** integration
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001, UI-002, UI-004
- **Paths:** kit/.uak/tests/test_dashboard_journey.py, docs/specs/dashboard-onboarding/, docs/DASHBOARD.md, README.md, CHANGELOG.md, kit/.uak/docs/WHY.md, kit/.uak/settings/known-files.txt
- **Acceptance:** Exercise clean setup, existing installation, interrupted/failed installation, missing prerequisites, and readiness blockers using disposable local Git fixtures., Capture real browser evidence at 1280x720 and 390x844 for welcome, wizard, beginner dashboard, advanced dashboard, and an error state; include keyboard and reduced-motion checks., Document the visual entry point, prerequisites, terminal fallback, Beginner versus Advanced, the difference between Installed and Ready, and planning the project in the interface (UI-004: idea, planner run, review, typed approval)., Record the user's usability problem as evidence in WHY.md and add a changelog entry. Regenerate known-file hashes after payload changes., Run kit lint, generation checks, the complete package smoke, and relevant MCP regression tests. Report platform verification honestly; CI verifies other operating systems., gpt-Dylan independently runs Verify and records a verdict on the exact pushed SHA (claude-Dylan implements; amended by Dylan, Nov 2026). A later code change requires review of the new SHA. Dylan retains the final merge decision.
- **Tests:** new_project_visual_setup_journey, interrupted_install_can_recover, missing_prerequisites_remain_actionable
- **Verify:** `python kit/.uak/tests/test_dashboard_journey.py`
- **Next step:** review the dependent task evidence and implement end-to-end tests before declaring the journey complete.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)


## UAK-010 · A partial install is never reported as installed

- **Type:** bug
- **Priority:** P1
- **Estimate:** 1.5 h
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/tests/test_setup_wizard.py, kit/.uak/tests/test_dashboard_journey.py
- **Acceptance:** Reproduction (found by UI-003's journey tests, Nov 2026): a file named `.claude` blocks a folder the kit needs; `install.sh` copies `.uak/` and `.uak/VERSION` early (line 129) and fails later writing `.claude/`. The running setup server says installed=false only because it remembers the failed target in memory; a new `install.sh --wizard` (or any fresh setup server) inspects the same folder and reports it installed, because `kit_present` only checks `.uak/PROJECT.md`, `.uak/bin/uak` and `.uak/VERSION`., The installer marks an install complete only after every step succeeded (for example, `.uak/VERSION` written last, or a completion stamp the installer removes at start and writes at the end); an interrupted or failed install, including `--update`, leaves the project visibly incomplete on disk., A fresh setup server on that folder reports installed=false, offers Repair or update with the reason, and `/api/check` refuses with the same actionable message; after the blocking file is moved, Repair reaches installed and the person's file is unchanged., A complete install and an `--update` of an older complete install are still reported installed (no regression for existing projects, including ones installed before this change)., `bash .uak/bin/smoke --package-only` exits 0; known-files are regenerated if an installed file changes.
- **Tests:** partial_install_is_not_installed_after_restart, failed_update_stays_incomplete, complete_install_is_still_installed
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py`
- **Next step:** in test_setup_wizard.py, install with a `.claude` file blocking the folder, then inspect the target with a NEW server (make_server) and assert installed is false; see it fail (uak red), then make the installer mark completion last.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)


## UI-005 · Prepare the project from the page, never only in a terminal

- **Type:** feature
- **Priority:** P0
- **Estimate:** 1 day
- **Depends on:** UI-004
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/planning.py, kit/.uak/tests/test_setup_prepare.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (hackathon simulation, 2026-11-11, notes/handoff:PENDING-IMPROVEMENTS.md #5, #6 and #8 to #10, plus #12): the next action lived only in Technical details, the person thought the page was still loading, and the gate's own push command would have published the unapproved plan files., An "Event schedule" form (start, end, time zone, with sensible defaults) writes Freeze-Epoch exactly as `uak clock START DEADLINE ZONE --write` does, and shows the computed freeze and the first-claim time., "Publish the kit to main" is a human act in the page with a confirmation that lists the files: it commits the installed kit and configuration WITHOUT IDEA.md, .uak/TASKS.md and .uak/OWNERS.md, as the local Git identity, on a branch equal to origin/main (or an empty remote), and pushes the verified commit; it refuses with the exact recovery otherwise. It keeps every UI-001 protection., Any step that can only happen outside the browser is shown as a clear "Do this in a terminal" box: which terminal, the `cd` into the project, the exact command with Copy, and "come back and press Check again". The next action is never only in Technical details., Planning is offered only once the kit is on main; before that, the planning section says why and points to the publish step., When lint fails for a reason that is not a `LINT:` line (GIT_ERROR, missing main, network), the page shows that reason in plain words with how to fix it., "Check the plan again" reruns the server's verification and lint on the current files without running the planner., The page asks once for the human's name and uses it for every human act that needs one (UAK_HUMAN); it is never typed into a command., Review of 0386bec (gpt-Dylan, three P1): publishing uses an installer-written manifest of the files it placed (never a directory prefix), verifies the whole committed tree (blob, type, mode, and absence for deletions) before pushing, and the schedule never follows a symlinked or out-of-project .uak/PROJECT.md nor a predictable temporary file., WHY.md records the new human acts (publishing the kit from the page) with the simulation as evidence; docs/DASHBOARD.md is updated.
- **Tests:** schedule_form_writes_freeze_epoch, publish_kit_excludes_unapproved_plan_files, publish_kit_pushes_only_the_verified_commit, terminal_step_is_shown_with_its_command, planning_waits_for_the_kit_on_main, lint_failure_reason_reaches_the_page, plan_can_be_rechecked_without_the_planner, human_name_is_asked_once
- **Verify:** `python kit/.uak/tests/test_setup_prepare.py`
- **Next step:** write the named tests with a local bare remote (empty, then with main) and the real `uak clock` and `uak lint`; see them fail (uak red); then add the schedule and publish endpoints to setup.py.
## UAK-013 · The session-start hook answers within 3 seconds

- **Type:** bug
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/hook, kit/.uak/tests/test_hook_session_start_speed.py, kit/.uak/tests/test_hook_claims.py
- **Acceptance:** Evidence (Claude Code /doctor on Dylan's Mac, 22 sessions over 18 days, 2026-11-11): the kit's SessionStart hook took about 9.5 s typical on startup, 12.6 s typical on resume and up to 28 s, blocking the start of every session in a project with the kit., `hook session-start` returns within 3 s on a fixture with a local bare remote; network or slow work (publishing tokens, black box flush, map build, inbox reads) runs in the background or is skipped when fresh, as tick already does., What session-start shows the agent (identity, task, inbox summary) stays correct and complete., Background refreshes outlive the hook by design (like tokens --publish): tests that end right after a session start wait for them before cleaning up, so Windows can remove the worktree (CI on PR #11: test_hook_claims WinError 32). Only waits are added; no assertion changes., `bash .uak/bin/smoke --package-only` exits 0.
- **Tests:** session_start_returns_within_budget, session_start_output_is_unchanged
- **Verify:** `python kit/.uak/tests/test_hook_session_start_speed.py`
- **Next step:** measure `hook session-start` on a fixture, find the synchronous slow steps, write the timing test (budget 3 s) and see it fail.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UAK-067
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-007 · A guided journey a new user can follow without the README

- **Type:** feature
- **Priority:** P1
- **Estimate:** 4 h
- **Depends on:** UI-006
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html, kit/.uak/tests/test_setup_guide.py, docs/DASHBOARD.md, CHANGELOG.md, kit/.uak/bin/lib/setup.py
- **Acceptance:** Evidence (hackathon simulation and PR chat, notes/handoff:PENDING-IMPROVEMENTS.md #2, #7, #13 and #17 to #20)., The welcome screen shows the whole journey and keeps it visible: Install → Prepare → Plan → Start the team → Follow progress, each marked "in this page", "in a terminal" or "your agents do it", with the current one highlighted. It says the page installs the kit INTO the project and that the kit itself is only downloaded once., The typed approval shows the exact folder name as a placeholder and, under the disabled button, "Type NAME to enable publishing"., When a step completes, the page moves the person to where the next one happens (for example, to "Plan your project")., In Spanish, the readiness gate's lines are translated (or a translated summary is shown above them), and the Advanced dashboard has no English labels left; the notice under the title no longer repeats the heading., The page warns when the logged-in Git/GitHub identity will sign the commits and PRs (another person's machine)., Keyboard, visible focus, reduced motion and 390px layouts keep working; docs/DASHBOARD.md and CHANGELOG.md are updated.
- **Tests:** journey_is_visible_from_welcome, approval_field_says_what_to_type, gate_lines_are_translated, advanced_dashboard_is_translated, shared_identity_is_warned
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests (markup and catalog contracts plus HTTP checks); see them fail; then build the journey stepper.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-011, UI-012, UI-013
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-011, UI-012, UI-013, UI-014
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-009 · The team step stays right after the first claim

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #2, #3, #5): state["reviewer"] is server-wide, so another project, another name or a retired reviewer shows "registered" (r4); the Codex reviewer command lacks the `--add-dir "<repo>/.git"` that wt recommends and `uak next` fails under its sandbox (r1, r3); after the first claim the page leaves "ready", the team commands vanish (r4) or it keeps offering the claimed task (r3)., "Registered" is derived per project and reviewer name from claims (roles/reviewers minus meta/retired), never from a server-wide flag., The Codex reviewer command grants write access to the repository's .git directory, quoted for the folder., After claims exist the team step stays visible: it offers an unclaimed task for a new implementer, a resume command for each claimed one, and the reviewer command.
- **Tests:** reviewer_state_follows_project_and_name, codex_command_can_write_git, team_step_survives_the_first_claim
- **Verify:** `python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests against the ready fixture with a claim on HACK-001; see them fail; then fix the reviewer state and the commands.

## UI-010 · Planning and schedule never pretend

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/planning.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_planning.py, kit/.uak/tests/test_setup_prepare.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #6, #7): a planning run that wrote no TASKS.md showed a green "plan passes uak lint" and an approve button (r3); planning took 4 to 8 minutes with no progress cue (r1); the event schedule defaults to today and saving it untouched silently froze a next-day hackathon (r1)., A run without .uak/TASKS.md is shown as failed (translated message, retry button, no lint line, no approve button)., While planning runs the page shows elapsed time and the last output line., The schedule fields start empty; saving requires a date, and a freeze time in the past or within the next hour asks for confirmation.
- **Tests:** missing_tasks_file_is_a_failed_plan, planning_shows_progress, schedule_is_never_guessed
- **Verify:** `python kit/.uak/tests/test_setup_planning.py && python kit/.uak/tests/test_setup_prepare.py`
- **Next step:** write the named tests with a fake planner that exits without writing TASKS.md; see them fail; then fix the plan view and the schedule form.

## UI-011 · The page answers while Git talks to the network, and publishing has no dead end

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** UI-009
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_prepare.py, kit/.uak/tests/test_setup_team.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository.
- **Tests:** status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out
- **Verify:** `python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests with a fake runner that blocks on ls-remote; see them fail; then move network calls out of the lock.

## UI-012 · Identity warning compares Git and GitHub separately

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_guide.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #8; PENDING-IMPROVEMENTS.md #44): one matching word suppressed the warning when Git matched the person but GitHub was someone else (r4); accented names did not match their unaccented form., The warning checks the Git name/email and the GitHub login each against the person's name and says which one belongs to someone else., Names match ignoring case and accents (José = jose).
- **Tests:** github_login_is_checked_on_its_own, accents_do_not_break_the_match
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests with a fake identity (Git = person, gh = other); see them fail; then split the check.

## UI-013 · No English left in the Spanish journey, and small honesty fixes

- **Type:** fix
- **Priority:** P3
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/status.sh, kit/.uak/tests/test_setup_guide.py, kit/.uak/tests/test_next_reviewer.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #10)., In Spanish the status heading, the doctor sub-lines, the schedule weekday, the claim progress line ("N commit(s) since the claim · last: …") and "No technical output yet" are translated, and the status heading has no ✓ while TODOs remain., A human never seen shows "never", not "20770 d"; the Agents tab lists the registered reviewer., The plan's Approved-By and the kit's Published-By use the same human name., `uak next` run as a registered reviewer offers reviews only, never implementation work.
- **Tests:** spanish_journey_has_no_english, never_seen_human_is_named, reviewer_is_not_offered_implementation
- **Verify:** `python kit/.uak/tests/test_setup_guide.py && python kit/.uak/tests/test_next_reviewer.py`
- **Next step:** write the named tests (rendered Spanish page text, a uak next run as NAME-r); see them fail; then translate and fix.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-011, UI-012, UI-013, UI-014, UAK-069
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-013 · No English left in the Spanish journey, and small honesty fixes

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/setup.py, kit/.uak/tests/test_setup_guide.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #10)., In Spanish the status heading, the doctor sub-lines, the schedule weekday, the claim progress line ("N commit(s) since the claim · last: …") and "No technical output yet" are translated, and the status heading has no ✓ while TODOs remain., A human never seen shows "never", not "20770 d"; the Agents tab lists the registered reviewer., The plan's Approved-By and the kit's Published-By use the same human name.
- **Tests:** spanish_journey_has_no_english, never_seen_human_is_named
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests (rendered Spanish page text); see them fail; then translate and fix.

## UAK-069 · uak next never offers implementation work to a reviewer identity

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/status.sh, kit/.uak/tests/test_next_reviewer.py, CHANGELOG.md
- **Acceptance:** Evidence (test rounds 2026-11-13, notes/handoff:qa/rounds-2026-11-13/r3-REPORT.md P3-6): `UAK_AGENT=luis-r uak next` offered HACK-001 for implementation to the registered reviewer identity., Run as an identity registered on claims roles/reviewers (and not retired), `uak next` offers only tasks waiting for review (or says there is nothing to review and how to wait), never AVAILABLE tasks to claim., An identity that is not a reviewer sees exactly the output it saw before (the protocol suites stay green)., the incident is cited in a comment next to the filter in status.sh and in CHANGELOG.md (a fix, not a new rule).
- **Tests:** reviewer_is_not_offered_implementation, implementer_output_is_unchanged
- **Verify:** `python kit/.uak/tests/test_next_reviewer.py`
- **Next step:** write the tests with a real Git fixture and bare remote (a registered NAME-r, one AVAILABLE task); see them fail; then filter next by role.
## UAK-069 · uak next never offers implementation work to a reviewer identity

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/status.sh, kit/.uak/tests/test_next_reviewer.py, scripts/claims_diff.py, CHANGELOG.md
- **Acceptance:** Evidence (test rounds 2026-11-13, notes/handoff:qa/rounds-2026-11-13/r3-REPORT.md P3-6): `UAK_AGENT=luis-r uak next` offered HACK-001 for implementation to the registered reviewer identity., Run as an identity registered on claims roles/reviewers (and not retired), `uak next` offers only tasks waiting for review (or says there is nothing to review and how to wait), never AVAILABLE tasks to claim., An identity that is not a reviewer sees exactly the output it saw before (the protocol suites stay green)., the incident is cited in a comment next to the filter in status.sh and in CHANGELOG.md (a fix, not a new rule).
- **Tests:** reviewer_is_not_offered_implementation, implementer_output_is_unchanged
- **Verify:** `python kit/.uak/tests/test_next_reviewer.py`
- **Next step:** write the tests with a real Git fixture and bare remote (a registered NAME-r, one AVAILABLE task); see them fail; then filter next by role.
## UI-011 · The page answers while Git talks to the network, and publishing has no dead end

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_prepare.py, kit/.uak/tests/test_setup_team.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository.
- **Tests:** status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out
- **Verify:** `python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_team.py`
- **Next step:** write the named tests with a fake runner that blocks on ls-remote; see them fail; then move network calls out of the lock.

## UI-014 · Each person picks the role of each coding tool they have

- **Type:** feature
- **Priority:** P1
- **Estimate:** 4 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_roles.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan, after the test rounds 2026-11-13): the team step always says "Claude Code implements, Codex reviews", but many people have only one subscription (only Claude or only Codex) and could not follow it; the engine already lets any tool take either role (a role is only an identity: UAK_AGENT)., For each coding tool installed in the project and signed in on this computer (the same detection planning uses), the person picks its role: implements, reviews, or both., With one tool, it can do both roles with two identities (TOOL-NAME implements, NAME-r reviews), and the page says the reviewer never reviews its own identity's work., With two tools, any combination works (for example Codex implements and Claude Code reviews); the choice is per person and remembered for the project (not shared with teammates)., The Copy commands follow the choice: the implement command opens the chosen tool in the task worktree with its first prompt, the review command starts the chosen tool as NAME-r with its review prompt (Claude Code: /uak-review; Codex: $uak-review, with --add-dir for .git); commands stay built only from server values., A tool not installed or not signed in is never offered, and the page says why; WHY.md and docs/DASHBOARD.md are updated, with Spanish for every new line.
- **Tests:** roles_follow_the_tools_you_have, one_tool_does_both_roles, any_tool_can_review, unavailable_tool_is_not_offered
- **Verify:** `python kit/.uak/tests/test_setup_roles.py`
- **Next step:** write the named tests with fake tools (only claude, only codex, both); see them fail; then add the role choice to the team step.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UI-013, UAK-069
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-009 · The team step, right for every person: reviewer state, tools and roles, network and publishing (absorbs UI-011 and UI-014)

- **Type:** fix
- **Priority:** P1
- **Estimate:** 8 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md, kit/.uak/tests/test_setup_prepare.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_roles.py, kit/.uak/docs/WHY.md
- **Acceptance:** Dylan merged UI-011 and UI-014 into this task (one delivery, one review, one CI) on 2026-11-13. From UI-009: Evidence (test rounds 2026-11-13, SUMMARY.md #2, #3, #5): state["reviewer"] is server-wide, so another project, another name or a retired reviewer shows "registered" (r4); the Codex reviewer command lacks the `--add-dir "<repo>/.git"` that wt recommends and `uak next` fails under its sandbox (r1, r3); after the first claim the page leaves "ready", the team commands vanish (r4) or it keeps offering the claimed task (r3)., "Registered" is derived per project and reviewer name from claims (roles/reviewers minus meta/retired), never from a server-wide flag., The Codex reviewer command grants write access to the repository's .git directory, quoted for the folder., After claims exist the team step stays visible: it offers an unclaimed task for a new implementer, a resume command for each claimed one, and the reviewer command. From UI-011: Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository. From UI-014: Evidence (Dylan, after the test rounds 2026-11-13): the team step always says "Claude Code implements, Codex reviews", but many people have only one subscription (only Claude or only Codex) and could not follow it; the engine already lets any tool take either role (a role is only an identity: UAK_AGENT)., For each coding tool installed in the project and signed in on this computer (the same detection planning uses), the person picks its role: implements, reviews, or both., With one tool, it can do both roles with two identities (TOOL-NAME implements, NAME-r reviews), and the page says the reviewer never reviews its own identity's work., With two tools, any combination works (for example Codex implements and Claude Code reviews); the choice is per person and remembered for the project (not shared with teammates)., The Copy commands follow the choice: the implement command opens the chosen tool in the task worktree with its first prompt, the review command starts the chosen tool as NAME-r with its review prompt (Claude Code: /uak-review; Codex: $uak-review, with --add-dir for .git); commands stay built only from server values., A tool not installed or not signed in is never offered, and the page says why; WHY.md and docs/DASHBOARD.md are updated, with Spanish for every new line.
- **Tests:** reviewer_state_follows_project_and_name, codex_command_can_write_git, team_step_survives_the_first_claim, status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out, roles_follow_the_tools_you_have, one_tool_does_both_roles, any_tool_can_review, unavailable_tool_is_not_offered
- **Verify:** `python kit/.uak/tests/test_setup_team.py && python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_roles.py`
- **Next step:** contract first (a Fable mentor pass and the reviewer's agreement), then the named tests, red, and the implementation.
## UI-013 · No English left in the Spanish journey, and small honesty fixes

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/tests/test_setup_guide.py
- **Acceptance:** Evidence (test rounds 2026-11-13, SUMMARY.md #10)., In Spanish the status heading, the doctor sub-lines, the schedule weekday, the claim progress line ("N commit(s) since the claim · last: …") and "No technical output yet" are translated, and the status heading has no ✓ while TODOs remain., A human never seen shows "never", not "20770 d"; the Agents tab lists the registered reviewer., The plan's Approved-By and the kit's Published-By use the same human name.
- **Tests:** spanish_journey_has_no_english, never_seen_human_is_named
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests (rendered Spanish page text); see them fail; then translate and fix.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-012 · Identity warning per account, and no English left in the Spanish journey (absorbs UI-013)

- **Type:** fix
- **Priority:** P2
- **Estimate:** 4 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_guide.py, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/dash.html
- **Acceptance:** Dylan merged UI-013 into this task (one delivery, one review, one CI) on 2026-11-13. From UI-012: Evidence (test rounds 2026-11-13, SUMMARY.md #8; PENDING-IMPROVEMENTS.md #44): one matching word suppressed the warning when Git matched the person but GitHub was someone else (r4); accented names did not match their unaccented form., The warning checks the Git name/email and the GitHub login each against the person's name and says which one belongs to someone else., Names match ignoring case and accents (José = jose). From UI-013: Evidence (test rounds 2026-11-13, SUMMARY.md #10)., In Spanish the status heading, the doctor sub-lines, the schedule weekday, the claim progress line ("N commit(s) since the claim · last: …") and "No technical output yet" are translated, and the status heading has no ✓ while TODOs remain., A human never seen shows "never", not "20770 d"; the Agents tab lists the registered reviewer., The plan's Approved-By and the kit's Published-By use the same human name.
- **Tests:** github_login_is_checked_on_its_own, accents_do_not_break_the_match, spanish_journey_has_no_english, never_seen_human_is_named
- **Verify:** `python kit/.uak/tests/test_setup_guide.py`
- **Next step:** write the named tests (fake identity: Git = person, gh = other; rendered Spanish page text); see them fail; then split the identity check and translate.
## UI-009 · The team step, right for every person: reviewer state, tools and roles, network and publishing (absorbs UI-011 and UI-014)

- **Type:** fix
- **Priority:** P1
- **Estimate:** 8 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md, kit/.uak/tests/test_setup_prepare.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_roles.py, kit/.uak/docs/WHY.md, kit/.uak/settings/known-files.txt, CHANGELOG.md, README.md
- **Acceptance:** Dylan merged UI-011 and UI-014 into this task (one delivery, one review, one CI) on 2026-11-13. From UI-009: Evidence (test rounds 2026-11-13, SUMMARY.md #2, #3, #5): state["reviewer"] is server-wide, so another project, another name or a retired reviewer shows "registered" (r4); the Codex reviewer command lacks the `--add-dir "<repo>/.git"` that wt recommends and `uak next` fails under its sandbox (r1, r3); after the first claim the page leaves "ready", the team commands vanish (r4) or it keeps offering the claimed task (r3)., "Registered" is derived per project and reviewer name from claims (roles/reviewers minus meta/retired), never from a server-wide flag., The Codex reviewer command grants write access to the repository's .git directory, quoted for the folder., After claims exist the team step stays visible: it offers an unclaimed task for a new implementer, a resume command for each claimed one, and the reviewer command. From UI-011: Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository. From UI-014: Evidence (Dylan, after the test rounds 2026-11-13): the team step always says "Claude Code implements, Codex reviews", but many people have only one subscription (only Claude or only Codex) and could not follow it; the engine already lets any tool take either role (a role is only an identity: UAK_AGENT)., For each coding tool installed in the project and signed in on this computer (the same detection planning uses), the person picks its role: implements, reviews, or both., With one tool, it can do both roles with two identities (TOOL-NAME implements, NAME-r reviews), and the page says the reviewer never reviews its own identity's work., With two tools, any combination works (for example Codex implements and Claude Code reviews); the choice is per person and remembered for the project (not shared with teammates)., The Copy commands follow the choice: the implement command opens the chosen tool in the task worktree with its first prompt, the review command starts the chosen tool as NAME-r with its review prompt (Claude Code: /uak-review; Codex: $uak-review, with --add-dir for .git); commands stay built only from server values., A tool not installed or not signed in is never offered, and the page says why; WHY.md and docs/DASHBOARD.md are updated, with Spanish for every new line.
- **Tests:** reviewer_state_follows_project_and_name, codex_command_can_write_git, team_step_survives_the_first_claim, status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out, roles_follow_the_tools_you_have, one_tool_does_both_roles, any_tool_can_review, unavailable_tool_is_not_offered
- **Verify:** `python kit/.uak/tests/test_setup_team.py && python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_roles.py`
- **Next step:** follow notes/handoff:UI-009-contract.md (Fable contract + the reviewer's 11 binding amendments); named tests, red, implement; a real Codex run as NAME-r on macOS and Windows Git Bash before done.
## UI-009 · The team step, right for every person: reviewer state, tools and roles, network and publishing (absorbs UI-011 and UI-014)

- **Type:** fix
- **Priority:** P1
- **Estimate:** 8 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md, kit/.uak/tests/test_setup_prepare.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_roles.py, kit/.uak/docs/WHY.md, kit/.uak/settings/known-files.txt, README.md
- **Acceptance:** Dylan merged UI-011 and UI-014 into this task (one delivery, one review, one CI) on 2026-11-13. From UI-009: Evidence (test rounds 2026-11-13, SUMMARY.md #2, #3, #5): state["reviewer"] is server-wide, so another project, another name or a retired reviewer shows "registered" (r4); the Codex reviewer command lacks the `--add-dir "<repo>/.git"` that wt recommends and `uak next` fails under its sandbox (r1, r3); after the first claim the page leaves "ready", the team commands vanish (r4) or it keeps offering the claimed task (r3)., "Registered" is derived per project and reviewer name from claims (roles/reviewers minus meta/retired), never from a server-wide flag., The Codex reviewer command grants write access to the repository's .git directory, quoted for the folder., After claims exist the team step stays visible: it offers an unclaimed task for a new implementer, a resume command for each claimed one, and the reviewer command. From UI-011: Evidence (test rounds 2026-11-13, SUMMARY.md #4, #9; PENDING-IMPROVEMENTS.md #40): network git (ls-remote, fetch) ran under the server lock and blocked /api/status (r4); offline, the team step said "publish the kit" (r4); a GitHub repository created with a .gitignore left publish advising "git pull", a dead end (r4)., Network Git runs outside the server lock with a timeout; /api/status answers within 1 s while it runs., Offline, the team step says the remote cannot be reached and offers retry, not publish., When the remote has unrelated history the page explains it and gives one exact command that keeps both histories, or offers to publish to a new empty repository. From UI-014: Evidence (Dylan, after the test rounds 2026-11-13): the team step always says "Claude Code implements, Codex reviews", but many people have only one subscription (only Claude or only Codex) and could not follow it; the engine already lets any tool take either role (a role is only an identity: UAK_AGENT)., For each coding tool installed in the project and signed in on this computer (the same detection planning uses), the person picks its role: implements, reviews, or both., With one tool, it can do both roles with two identities (TOOL-NAME implements, NAME-r reviews), and the page says the reviewer never reviews its own identity's work., With two tools, any combination works (for example Codex implements and Claude Code reviews); the choice is per person and remembered for the project (not shared with teammates)., The Copy commands follow the choice: the implement command opens the chosen tool in the task worktree with its first prompt, the review command starts the chosen tool as NAME-r with its review prompt (Claude Code: /uak-review; Codex: $uak-review, with --add-dir for .git); commands stay built only from server values., A tool not installed or not signed in is never offered, and the page says why; WHY.md and docs/DASHBOARD.md are updated, with Spanish for every new line.
- **Tests:** reviewer_state_follows_project_and_name, codex_command_can_write_git, team_step_survives_the_first_claim, status_answers_during_network_git, offline_team_step_says_offline, unrelated_remote_history_has_a_way_out, roles_follow_the_tools_you_have, one_tool_does_both_roles, any_tool_can_review, unavailable_tool_is_not_offered
- **Verify:** `python kit/.uak/tests/test_setup_team.py && python kit/.uak/tests/test_setup_prepare.py && python kit/.uak/tests/test_setup_roles.py`
- **Next step:** follow notes/handoff:UI-009-contract.md (Fable contract + the reviewer's 11 binding amendments); named tests, red, implement; a real Codex run as NAME-r on macOS and Windows Git Bash before done.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-016 · A short demo video on the kit's landing (README): from zero to a finished, deployed product

- **Type:** feature
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** docs/media/tutorial.mp4, docs/media/tutorial-en.srt, docs/media/tutorial-es.srt, docs/media/tutorial-poster.gif, docs/video/, README.md, kit/.uak/tests/test_tutorial_video.py
- **Acceptance:** Evidence (Sebastián and Dylan, 2026-11-13; test rounds SUMMARY.md: novices did not know which steps happen in the page, in a terminal or by the agents). Dylan narrowed the scope: demonstration only, small, on the landing., One video under 90 seconds that walks through the kit from zero to a complete product: install the kit into an empty project, prepare and plan in the local page, start the team (Claude Code implements, a second identity reviews), agents claim, build, review and merge tasks, the board shows progress, and the product ends deployed (a simulated hackathon app, e.g. a cafeteria queue board, with its live URL). It may be a simulation (scripted screens and terminal), labelled as a demonstration., Source in docs/video/ (Remotion or another scripted tool, pinned versions), rendered with one documented command; the MP4 is H.264, at most 3 MB, with English and Spanish .srt captions and an animated poster at most 1.5 MB., The README (the kit's landing on GitHub) shows the poster near the top, linking to the MP4, with a line naming the captions in both languages; nothing is added to the installed kit.
- **Tests:** video_is_short_and_small, readme_shows_the_demo, captions_exist_in_both_languages
- **Verify:** `python kit/.uak/tests/test_tutorial_video.py`
- **Next step:** write the tests (ffprobe duration < 90 s when available, file sizes, README markup, both .srt files parse); see them fail; then script and render the video.
## UI-016 · A short demo video, from zero to a finished deployed product, shipped with the kit for its setup page

- **Type:** feature
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/media/, docs/video/, kit/.uak/tests/test_tutorial_video.py, kit/.uak/settings/known-files.txt, README.md
- **Acceptance:** Evidence (Sebastián and Dylan, 2026-11-13; test rounds SUMMARY.md: novices did not know which steps happen in the page, in a terminal or by the agents). Dylan: demonstration only, small, shown in the interface the kit opens (the local setup page; UI-017 wires it in)., One video under 90 seconds that walks through the kit from zero to a complete product: install the kit into an empty project, prepare and plan in the local page, start the team (Claude Code implements, a second identity reviews), agents claim, build, review and merge tasks, the board shows progress, and the product ends deployed (a simulated hackathon app, e.g. a cafeteria queue board, with its live URL). A simulation (scripted screens and terminal) is fine, labelled as a demonstration., Source in docs/video/ (Remotion or another scripted tool, pinned versions), rendered with one documented command., Shipped files in kit/.uak/media/: tutorial.mp4 (H.264, at most 3 MB), tutorial-en.vtt and tutorial-es.vtt (WebVTT captions with the same cues), tutorial-poster.jpg (at most 150 KB); all listed by kit_hashes in known-files.txt; the installed kit grows by at most 3.5 MB., README may link the MP4 (optional).
- **Tests:** video_is_short_and_small, captions_exist_in_both_languages, media_ships_with_the_kit
- **Verify:** `python kit/.uak/tests/test_tutorial_video.py`
- **Next step:** write the tests (ffprobe duration < 90 s when available, file sizes, both .vtt parse with the same cue count, install.sh copies kit/.uak/media); see them fail; then script and render the video.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-016 · A short demo video, from zero to a finished deployed product, shipped with the kit for its setup page

- **Type:** feature
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/media/, docs/video/, kit/.uak/tests/test_tutorial_video.py, kit/.uak/settings/known-files.txt, README.md, install.sh
- **Acceptance:** Evidence (Sebastián and Dylan, 2026-11-13; test rounds SUMMARY.md: novices did not know which steps happen in the page, in a terminal or by the agents). Dylan: demonstration only, small, shown in the interface the kit opens (the local setup page; UI-017 wires it in)., One video under 90 seconds that walks through the kit from zero to a complete product: install the kit into an empty project, prepare and plan in the local page, start the team (Claude Code implements, a second identity reviews), agents claim, build, review and merge tasks, the board shows progress, and the product ends deployed (a simulated hackathon app, e.g. a cafeteria queue board, with its live URL). A simulation (scripted screens and terminal) is fine, labelled as a demonstration., Source in docs/video/ (Remotion or another scripted tool, pinned versions), rendered with one documented command., Shipped files in kit/.uak/media/: tutorial.mp4 (H.264, at most 3 MB), tutorial-en.vtt and tutorial-es.vtt (WebVTT captions with the same cues), tutorial-poster.jpg (at most 150 KB); all listed by kit_hashes in known-files.txt; the installed kit grows by at most 3.5 MB., README may link the MP4 (optional).
- **Tests:** video_is_short_and_small, captions_exist_in_both_languages, media_ships_with_the_kit
- **Verify:** `python kit/.uak/tests/test_tutorial_video.py`
- **Next step:** write the tests (ffprobe duration < 90 s when available, file sizes, both .vtt parse with the same cue count, install.sh copies kit/.uak/media); see them fail; then script and render the video.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-018 · The setup page always says what it is doing, why a button is blocked, and what changed

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/setup.py, kit/.uak/tests/test_setup_feedback.py, kit/.uak/docs/WHY.md, docs/DASHBOARD.md, CHANGELOG.md
- **Acceptance:** Evidence (Dylan's real run, 2026-11-13, turno-cafeteria-2, Spanish, macOS): (1) at the plan step the layout jumps — the page renders narrow/cut and then expands, and in "Project preferences" the https input and its hint wrap into one broken line; (2) hovering a disabled "Create the plan" shows the spinning wait cursor (CSS `button:disabled { cursor: wait }`), so a BLOCKED button looks BUSY and nothing says why it is blocked; (3) "Check what's next" seems to do nothing: no visible progress near the button, no "checked at HH:MM" result, the outcome only lands in places the person is not looking. Dylan asked for usability heuristics (visibility of system status, feedback on every action)., Visibility of status: every action button shows an in-button busy state while its request runs (label "Checking…" / "Installing…" etc., aria-busy, a small spinner), and when it ends a short result line appears right next to the button ("Checked at 21:04 · 2 things to do" / error text), announced to screen readers; a check that changes nothing still says so., Blocked vs busy: disabled-because-blocked buttons use `cursor: not-allowed` and show their reason in text next to them (e.g. Create the plan: "Publish the kit to main first (step 3)"; no idea saved; no tool selected); the wait cursor is used only while a request is running., No layout shift: polling/re-render never collapses or resizes sections (stable container width, reserved space for status lines, no re-creating DOM that changes height for unchanged data); the preferences row (input, hint, button) lays out cleanly at 1280x720 and 390x844., When the readiness gate's next step is something the page can do (e.g. "push the kit to main" → the Publish button), the page points to that button (scroll/focus + highlight) instead of leaving the raw terminal text as the only guidance., Clicking a button out of order or before its prerequisites shows a small notification (toast) on the right with exactly what to do next and a way to jump there (aria-disabled instead of native disabled so the click can explain itself; translated, aria-live, dismissible, auto-hides but pauses on hover/focus, one at a time, full-width bottom on mobile, reduced motion respected)., Spanish for every new string; reduced motion respected; WHY.md cites this run; docs/DASHBOARD.md updated.
- **Tests:** blocked_buttons_say_why, actions_show_busy_and_result, check_reports_even_when_nothing_changed, no_wait_cursor_on_blocked_buttons, layout_is_stable_across_refresh, out_of_order_click_explains_the_next_step
- **Verify:** `python kit/.uak/tests/test_setup_feedback.py`
- **Next step:** reproduce with Playwright (Spanish, 1280x720): the plan step before the kit is on main, a Check press, a refresh cycle (measure section heights/offsets across polls); write the tests; see them fail; fix.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-022, UI-023, UI-024
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-094 · Engine messages and caches that misled agents

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/lib/status.sh, kit/.uak/bin/lib/messages.sh, kit/.uak/bin/stats, kit/.uak/bin/board, kit/.uak/bin/dash, kit/.uak/bin/lib/dash.py, kit/.uak/tests/test_engine_messages_qa14.py
- **Acceptance:** Evidence (QA round C, notes/handoff:qa/rounds-2026-11-14 C-7, C-11..C-16): a contract message cited a SHA only on an unmerged branch; `next`'s "= unchanged" cache is keyed by session not identity (beto-r saw "Nothing new" after ana-r); stats lists normal queue waits as human-queue reasons; board shows "PR#001" for a non-numeric URL; dash prints a tar DeprecationWarning and reports mode "" ., A contract message's SHA is resolved to its branch and the message shows `git show origin/BRANCH:path`; the next cache key includes UAK_AGENT; stats counts only real escalations; board shows the URL tail when there is no number; dash extracts with filter="data" (when supported) and falls back to PROJECT.md for Mode.
- **Tests:** contract_message_names_the_branch, next_cache_is_per_identity, stats_counts_only_escalations, board_pr_label_without_number, dash_reports_the_mode
- **Verify:** `python kit/.uak/tests/test_engine_messages_qa14.py`
- **Next step:** one fixture per item; see them fail; fix each in its file.

## UI-019 · Coming back to a project: the page restores where you were

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** UI-018
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_resume.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-14: "se me borró todo al refrescar", stuck "Comprobar siguiente paso"; QA notes/handoff:qa/rounds-2026-11-14 A-F2, A-F3, A-F4, A-F8, A-F11, B-04, B-05, B-14, D-6.1): after a refresh, a restart or re-picking the project the page landed on Welcome/Prepare with empty forms, offered publish and "Crear el plan" for an approved plan, forgot the human name (team step silently hidden by a 400), and the old tab after a restart showed raw "Failed to fetch" while polling forever., The server re-inspects its target on start and the page lands on the furthest real step (derived from the repo: installed, kit on main, schedule, idea, plan approved, reviewer registered); completed steps are shown done and collapsed; the human name persists per project (in the Git dir, never committed) and the team step asks for it inline if missing; the check runs automatically after inspect; re-picking keeps state; the active tab survives reloads; when the server is gone the page shows a translated banner ("Setup se cerró: vuelve a ejecutar el comando y abre el nuevo enlace") and backs off polling.
- **Tests:** restart_lands_on_the_team_step, refresh_keeps_the_step_and_values, name_persists_per_project, repick_keeps_state, server_gone_banner
- **Verify:** `python kit/.uak/tests/test_setup_resume.py`
- **Next step:** fixture of an installed+approved project; restart; assert landing step; tests fail; fix.

## UAK-091 · A newer kit release never blocks a working project; update hints name the kit that installed it

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/start, kit/.uak/bin/doctor, install.sh, kit/.uak/tests/test_start_version_gate.py
- **Acceptance:** Evidence (QA rounds 2026-11-14, notes/handoff:qa/rounds-2026-11-14: A-F1, B-02, C-4; and Dylan's live turno-cafeteria-2): when the kit's GitHub released 6.3.0, every `uak start` on a 6.2.0 project became "TODO update the kit", READY never came, the setup page hid the team step, and the hint pointed at ~/.uak-kit (another clone); `UAK_KIT_PIN=1` is the only escape., Once the kit is on the project's main (or Freeze-Epoch is set), a newer release is a NOTE, never a TODO; READY is unaffected., The update hint names the folder that installed this project when known (recorded at install), else says how to find it; it never names a different clone as fact., A fresh teammate clone of a READY project is READY without any env var., The setup page path is unaffected by stripped UAK_* variables (the decision is in start, not the environment).
- **Tests:** newer_release_is_a_note_after_publish, update_hint_names_the_installing_kit, teammate_clone_is_ready
- **Verify:** `python kit/.uak/tests/test_start_version_gate.py`
- **Next step:** fixture with a local bare "kit GitHub" tagged above the project's VERSION; see start TODO; tests fail; then change start.

## UI-019 · Coming back to a project: the page restores where you were

- **Type:** fix
- **Priority:** P1
- **Estimate:** 3 h
- **Depends on:** UI-018
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_resume.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-14: "se me borró todo al refrescar", stuck "Comprobar siguiente paso"; QA notes/handoff:qa/rounds-2026-11-14 A-F2, A-F3, A-F4, A-F8, A-F11, B-04, B-05, B-14, D-6.1): after a refresh, a restart or re-picking the project the page landed on Welcome/Prepare with empty forms, offered publish and "Crear el plan" for an approved plan, forgot the human name (team step silently hidden by a 400), and the old tab after a restart showed raw "Failed to fetch" while polling forever., The server re-inspects its target on start and the page lands on the furthest real step (derived from the repo: installed, kit on main, schedule, idea, plan approved, reviewer registered); completed steps are shown done and collapsed; the human name persists per project (in the Git dir, never committed) and the team step asks for it inline if missing; the check runs automatically after inspect; re-picking keeps state; the active tab survives reloads; when the server is gone the page shows a translated banner ("Setup se cerró: vuelve a ejecutar el comando y abre el nuevo enlace") and backs off polling.
- **Tests:** restart_lands_on_the_team_step, refresh_keeps_the_step_and_values, name_persists_per_project, repick_keeps_state, server_gone_banner
- **Verify:** `python kit/.uak/tests/test_setup_resume.py`
- **Next step:** fixture of an installed+approved project; restart; assert landing step; tests fail; fix.

## UAK-095 · Plain Python projects deploy, and the planner only promises what the kit can do

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** None
- **Paths:** kit/.uak/bin/deploy, kit/.uak/stacks/python-stdlib/, kit/.uak/tests/test_deploy_python_stdlib.py, kit/.uak/settings/known-files.txt
- **Acceptance:** Evidence (QA round C, notes/handoff:qa/rounds-2026-11-14 C-5): the planner wrote "uak deploy --write has produced Dockerfile" but deploy says "no known stack here" for a stdlib Python app, and the agent hand-wrote a broken Dockerfile., `uak deploy --write` recognises a stdlib Python web app (python3 -m <module> or a server.py) and writes a working Dockerfile + Render Blueprint; when no stack matches, the message says what to add.
- **Tests:** deploy_recognises_stdlib_python, deploy_says_what_is_missing
- **Verify:** `python kit/.uak/tests/test_deploy_python_stdlib.py, kit/.uak/settings/known-files.txt`
- **Next step:** fixture app; see "no known stack"; add the stack.

## UI-022 · Spanish all the way and plain words for beginners

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** None
- **Paths:** kit/.uak/tests/test_setup_language.py
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F10, B-11, D-4.1, D-2.1, D-2.2, D-2.4, A-F20): English left in the Spanish UI (gate lines like "the kit's GitHub", FREEZE line, git stderr when offline with a misleading "check your connection", violation list, CLAIMED/all/human tokens, publish refusals); jargon for novices; ustedes/tú mix; one control with three labels; the plan written in English for a Spanish idea., Every engine line the page shows has a Spanish pattern or a plain Spanish summary; common git failures (not a repo, auth, DNS, timeout) map to one plain sentence with stderr under Technical details; Beginner view explains jargon (abbr/tooltip); tú throughout; one label per action; the planner writes titles and criteria in the idea's language.
- **Tests:** spanish_page_has_no_engine_english, git_failures_are_plain, planner_follows_the_idea_language, one_label_per_action
- **Verify:** `python kit/.uak/tests/test_setup_language.py`
- **Next step:** collect every English string from the QA screenshots; tests fail; translate.

## UI-021 · Forms say what is wrong next to the field, and the page speaks plain Spanish all the way (absorbs UI-022)

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3.5 h
- **Depends on:** UI-020
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_forms.py, kit/.uak/bin/lib/planning.py, kit/.uak/tests/test_setup_language.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Dylan merged UI-022 into this task (one delivery, one review, one CI) on 2026-11-17 to save a cycle. From UI-021: Evidence (QA notes/handoff:qa/rounds-2026-11-14 D-9.1, D-5.1, D-5.2, D-5.3, A-F13, A-F14): name/schedule/idea errors went to a global box ~2,900 px away with focus on body; "Mars/Base" accepted as a time zone; event times as weekdays without dates in reversed order; relative paths said "does not exist"; schedule inputs overlap 8 px; no gap above "Guardar la idea"; native English validation bubbles., Per-field errors under the field with aria-invalid/aria-describedby and focus moved to it; server validates time zones against zoneinfo (datalist prefilled with the browser zone); schedule confirmations show dates in chronological order; relative paths get "use the full path"; layout fixes; page messages instead of native bubbles (translated). From UI-022: Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F10, B-11, D-4.1, D-2.1, D-2.2, D-2.4, A-F20): English left in the Spanish UI (gate lines like "the kit's GitHub", FREEZE line, git stderr when offline with a misleading "check your connection", violation list, CLAIMED/all/human tokens, publish refusals); jargon for novices; ustedes/tú mix; one control with three labels; the plan written in English for a Spanish idea., Every engine line the page shows has a Spanish pattern or a plain Spanish summary; common git failures (not a repo, auth, DNS, timeout) map to one plain sentence with stderr under Technical details; Beginner view explains jargon (abbr/tooltip); tú throughout; one label per action; the planner writes titles and criteria in the idea's language.
- **Tests:** field_errors_sit_next_to_the_field, invalid_time_zone_is_refused, schedule_shows_dates_in_order, relative_path_says_so, spanish_page_has_no_engine_english, git_failures_are_plain, planner_follows_the_idea_language, one_label_per_action
- **Verify:** `python kit/.uak/tests/test_setup_forms.py && python kit/.uak/tests/test_setup_language.py`
- **Next step:** reproduce with the QA round D/A scripts; tests fail; fix forms first, then language.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-020 · Branches and publishing never leave a dead end

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2.5 h
- **Depends on:** UI-019
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_branches.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan's live turno-cafeteria-2: GitHub default branch became claims; QA notes/handoff:qa/rounds-2026-11-14 B-01, B-03, B-09, B-16): a teammate clone landed on claims and the kit was installed there; after the way-out pull, publish refused in English with no command; "El comando de abajo…" shown with no command; a quote in the path blocked the way-out., Inspect/install warn and stop when HEAD is not the base branch (with "git switch main"); the page warns when the remote's default branch is claims and says how to change it on GitHub; the way-out includes the push step and the publish refusal is translated with the exact command; the "command below" sentence only appears with a command; paths with a quote mark get a correctly quoted command.
- **Tests:** install_refuses_a_non_base_branch, warns_when_remote_default_is_claims, way_out_includes_the_push, no_promise_without_a_command, quote_in_path_gets_a_command
- **Verify:** `python kit/.uak/tests/test_setup_branches.py`
- **Next step:** fixtures from QA round B; tests fail; fix.

## UI-023 · The dashboard tells the truth and is accessible

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** UI-021
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_dashboard_truth.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F9, B-06, B-07, B-08, B-12, B-13, B-15, D WCAG 1.4.3/2.5.3/2.5.8/1.3.1, D-4.3/4.4/8.3/1.3): dependency-blocked tasks shown as available; frozen project shown as "team working"; a merge needing a human missing from setup's next step (raw English reason with an absolute path); offline shows the local plan as all available; plural labels on single rows; approved reviews have no mark; muted text contrast 3.26–4.45:1; "View" label vs accessible name; 53x19 px task buttons; missing headings; tabs not ARIA tabs ("Board2"); tab strip cut at 390; green dot at 0 agents., "Esperando dependencias" bucket and "aprobada" badge; FREEZE shown as frozen everywhere; needs-human items first in setup's next step, translated, no paths; offline falls back to the last known claims marked stale; singular/plural labels; contrast ≥ 4.5:1 in light and dark; label-in-name; targets ≥ 24 px; headings per view; ARIA tabs with arrow keys; tabs wrap at 390; grey dot at 0.
- **Tests:** blocked_tasks_are_not_available, frozen_is_frozen, needs_human_comes_first, offline_uses_last_claims, dashboard_meets_contrast_and_targets
- **Verify:** `python kit/.uak/tests/test_dashboard_truth.py`
- **Next step:** fixtures with hand-made claims states (QA round B scripts); tests fail; fix.

## UI-024 · The team step leads a beginner through the first run

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** UI-023
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_first_run.py, kit/.uak/settings/known-files.txt, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F6, A-F7, A-F15, A-F16, A-F19, B-10, D-3.2, D-6.1, D-7.1, D-10.1, D-10.2, D-1.1, D-1.2, D-9.2): Claude Code's trust dialog defaults to "No, exit" and shows an English 51-permissions warning the page never mentions; launch commands copyable before the reviewer is registered; "Comprobar siguiente paso" redraws the list and jumps 1,014 px; a hanging remote makes the check take 75 s with every view 409; blocked reasons shown 3 times; two 1–5 numberings; two humans never addressed; "Set up my project" below the fold; busy-disabled buttons without a reason; after a planner rule break the page says "Done" with a green lint box and conflicting undo advice., Trust step says "press ↓ then Enter" and that the warning is expected, and detects trust (Claude's own config) to show ✓/✗; launch commands stay locked until the reviewer is registered; the check keeps the old list dimmed until the new result (no jump) and network steps are bounded (results stay viewable during a check); one place per blocked reason; one step model; a two-person note (who runs what); CTA above the fold; every disabled button has a reason; a rule break reads "Terminó con problemas" with one undo instruction and its command.
- **Tests:** trust_step_is_explicit, commands_wait_for_the_reviewer, check_does_not_jump, views_answer_during_a_check, rule_break_is_not_done
- **Verify:** `python kit/.uak/tests/test_setup_first_run.py`
- **Next step:** reproduce with QA round A/D scripts; tests fail; fix.

## UI-020 · Branches and publishing never leave a dead end

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2.5 h
- **Depends on:** UI-019
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_branches.py, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan's live turno-cafeteria-2: GitHub default branch became claims; QA notes/handoff:qa/rounds-2026-11-14 B-01, B-03, B-09, B-16): a teammate clone landed on claims and the kit was installed there; after the way-out pull, publish refused in English with no command; "El comando de abajo…" shown with no command; a quote in the path blocked the way-out., Inspect/install warn and stop when HEAD is not the base branch (with "git switch main"); the page warns when the remote's default branch is claims and says how to change it on GitHub; the way-out includes the push step and the publish refusal is translated with the exact command; the "command below" sentence only appears with a command; paths with a quote mark get a correctly quoted command.
- **Tests:** install_refuses_a_non_base_branch, warns_when_remote_default_is_claims, way_out_includes_the_push, no_promise_without_a_command, quote_in_path_gets_a_command
- **Verify:** `python kit/.uak/tests/test_setup_branches.py`
- **Next step:** fixtures from QA round B; tests fail; fix.

## UI-023 · The dashboard tells the truth and is accessible

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** UI-021
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_dashboard_truth.py, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F9, B-06, B-07, B-08, B-12, B-13, B-15, D WCAG 1.4.3/2.5.3/2.5.8/1.3.1, D-4.3/4.4/8.3/1.3): dependency-blocked tasks shown as available; frozen project shown as "team working"; a merge needing a human missing from setup's next step (raw English reason with an absolute path); offline shows the local plan as all available; plural labels on single rows; approved reviews have no mark; muted text contrast 3.26–4.45:1; "View" label vs accessible name; 53x19 px task buttons; missing headings; tabs not ARIA tabs ("Board2"); tab strip cut at 390; green dot at 0 agents., "Esperando dependencias" bucket and "aprobada" badge; FREEZE shown as frozen everywhere; needs-human items first in setup's next step, translated, no paths; offline falls back to the last known claims marked stale; singular/plural labels; contrast ≥ 4.5:1 in light and dark; label-in-name; targets ≥ 24 px; headings per view; ARIA tabs with arrow keys; tabs wrap at 390; grey dot at 0.
- **Tests:** blocked_tasks_are_not_available, frozen_is_frozen, needs_human_comes_first, offline_uses_last_claims, dashboard_meets_contrast_and_targets
- **Verify:** `python kit/.uak/tests/test_dashboard_truth.py`
- **Next step:** fixtures with hand-made claims states (QA round B scripts); tests fail; fix.

## UI-024 · The team step leads a beginner through the first run

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** UI-023
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_first_run.py, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F6, A-F7, A-F15, A-F16, A-F19, B-10, D-3.2, D-6.1, D-7.1, D-10.1, D-10.2, D-1.1, D-1.2, D-9.2): Claude Code's trust dialog defaults to "No, exit" and shows an English 51-permissions warning the page never mentions; launch commands copyable before the reviewer is registered; "Comprobar siguiente paso" redraws the list and jumps 1,014 px; a hanging remote makes the check take 75 s with every view 409; blocked reasons shown 3 times; two 1–5 numberings; two humans never addressed; "Set up my project" below the fold; busy-disabled buttons without a reason; after a planner rule break the page says "Done" with a green lint box and conflicting undo advice., Trust step says "press ↓ then Enter" and that the warning is expected, and detects trust (Claude's own config) to show ✓/✗; launch commands stay locked until the reviewer is registered; the check keeps the old list dimmed until the new result (no jump) and network steps are bounded (results stay viewable during a check); one place per blocked reason; one step model; a two-person note (who runs what); CTA above the fold; every disabled button has a reason; a rule break reads "Terminó con problemas" with one undo instruction and its command.
- **Tests:** trust_step_is_explicit, commands_wait_for_the_reviewer, check_does_not_jump, views_answer_during_a_check, rule_break_is_not_done
- **Verify:** `python kit/.uak/tests/test_setup_first_run.py`
- **Next step:** reproduce with QA round A/D scripts; tests fail; fix.

## UI-021 · Forms say what is wrong next to the field, and the page speaks plain Spanish all the way (absorbs UI-022)

- **Type:** fix
- **Priority:** P2
- **Estimate:** 3.5 h
- **Depends on:** UI-020
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_forms.py, kit/.uak/bin/lib/planning.py, kit/.uak/tests/test_setup_language.py, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Dylan merged UI-022 into this task (one delivery, one review, one CI) on 2026-11-17 to save a cycle. From UI-021: Evidence (QA notes/handoff:qa/rounds-2026-11-14 D-9.1, D-5.1, D-5.2, D-5.3, A-F13, A-F14): name/schedule/idea errors went to a global box ~2,900 px away with focus on body; "Mars/Base" accepted as a time zone; event times as weekdays without dates in reversed order; relative paths said "does not exist"; schedule inputs overlap 8 px; no gap above "Guardar la idea"; native English validation bubbles., Per-field errors under the field with aria-invalid/aria-describedby and focus moved to it; server validates time zones against zoneinfo (datalist prefilled with the browser zone); schedule confirmations show dates in chronological order; relative paths get "use the full path"; layout fixes; page messages instead of native bubbles (translated). From UI-022: Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F10, B-11, D-4.1, D-2.1, D-2.2, D-2.4, A-F20): English left in the Spanish UI (gate lines like "the kit's GitHub", FREEZE line, git stderr when offline with a misleading "check your connection", violation list, CLAIMED/all/human tokens, publish refusals); jargon for novices; ustedes/tú mix; one control with three labels; the plan written in English for a Spanish idea., Every engine line the page shows has a Spanish pattern or a plain Spanish summary; common git failures (not a repo, auth, DNS, timeout) map to one plain sentence with stderr under Technical details; Beginner view explains jargon (abbr/tooltip); tú throughout; one label per action; the planner writes titles and criteria in the idea's language.
- **Tests:** field_errors_sit_next_to_the_field, invalid_time_zone_is_refused, schedule_shows_dates_in_order, relative_path_says_so, spanish_page_has_no_engine_english, git_failures_are_plain, planner_follows_the_idea_language, one_label_per_action
- **Verify:** `python kit/.uak/tests/test_setup_forms.py && python kit/.uak/tests/test_setup_language.py`
- **Next step:** reproduce with the QA round D/A scripts; tests fail; fix forms first, then language.
## UAK-096 · Small events get small plans, and projects don't receive the kit's own tests

- **Type:** fix
- **Priority:** P2
- **Estimate:** 1.5 h
- **Depends on:** None
- **Paths:** kit/.agents/skills/uak-plan/SKILL.md, kit/.claude/commands/uak-plan.md, install.sh, kit/.uak/tests/test_plan_scale.py
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F12, A-F18, C-17): a 3-hour, 2-person stdlib idea got 7 P0 tasks including a human-gated design lock and a landing; publishing committed 532 files including the kit's own .uak/tests suite; headless work needs 4 prompts per task., The planning skill scales the task count to event length × team size and avoids human-gated tasks in sprints under a day; install.sh does not copy kit/.uak/tests into user projects unless something in the project needs them (check smoke, doctor and garden first; if they are needed, document why and close this criterion with that evidence); the plan skill documents a single headless "run to REVIEW" prompt.
- **Tests:** short_sprint_plans_are_small, install_skips_the_kit_tests
- **Verify:** `python kit/.uak/tests/test_plan_scale.py`
- **Next step:** check where install copies tests and where the plan skill sizes tasks; tests; fix.
## UAK-096 · Small events get small plans, and projects don't receive the kit's own tests

- **Type:** fix
- **Priority:** P2
- **Estimate:** 1.5 h
- **Depends on:** None
- **Paths:** kit/.agents/skills/uak-plan/SKILL.md, kit/.claude/commands/uak-plan.md, kit/.gemini/commands/uak-plan.toml, kit/.uak/settings/known-files.txt, kit/.uak/docs/CLI.md, install.sh, kit/.uak/tests/test_plan_scale.py
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F12, A-F18, C-17): a 3-hour, 2-person stdlib idea got 7 P0 tasks including a human-gated design lock and a landing; publishing committed 532 files including the kit's own .uak/tests suite; headless work needs 4 prompts per task., The planning skill scales the task count to event length × team size and avoids human-gated tasks in sprints under a day; install.sh does not copy kit/.uak/tests into user projects unless something in the project needs them (check smoke, doctor and garden first; if they are needed, document why and close this criterion with that evidence); the plan skill documents a single headless "run to REVIEW" prompt.
- **Tests:** short_sprint_plans_are_small, install_skips_the_kit_tests
- **Verify:** `python kit/.uak/tests/test_plan_scale.py`
- **Next step:** check where install copies tests and where the plan skill sizes tasks; tests; fix.
## UAK-093 · The product smoke exists from the start and boots the app

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-091
- **Paths:** kit/.uak/bin/lib/smoke-init.sh, kit/.uak/bin/start, kit/.uak/tests/test_smoke_onboarding.py
- **Acceptance:** Evidence (QA round C, notes/handoff:qa/rounds-2026-11-14 C-1, C-3, C-10): nothing on the onboarding path created .uak/bin/smoke-project, so `uak start` said READY and then the first /uak-ship and the merge gate failed PRODUCT_UNVERIFIED; after two green merges the integrated app crashed on boot (ImportError) because tests forced a fake store and no gate booted the app; init-smoke left an empty scripts/ dir., Until .uak/bin/smoke-project exists, `uak start` shows the exact init-smoke command for the detected stack (or a generic one): a blocking TODO in sprint mode (the kit's own merge gate runs the product smoke) and a non-blocking NOTE in marathon mode (the human merges on the forge); existing tests that expect START READY on a fresh marathon install keep passing (Dylan's decision 2026-11-17); the generated smoke for a web stack starts the app and requests one route (bounded timeout), not only unit tests; init-smoke creates no stray folders.
- **Tests:** start_asks_for_the_smoke, web_smoke_boots_the_app, init_smoke_leaves_no_stray_dirs
- **Verify:** `python kit/.uak/tests/test_smoke_onboarding.py`
- **Next step:** fixture: stdlib Python app whose import is broken but unit tests pass; the generated smoke must fail; then implement.

## UAK-093 · The product smoke exists from the start and boots the app

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-091
- **Paths:** kit/.uak/bin/lib/smoke-init.sh, kit/.uak/bin/start, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_smoke_onboarding.py
- **Acceptance:** Evidence (QA round C, notes/handoff:qa/rounds-2026-11-14 C-1, C-3, C-10): nothing on the onboarding path created .uak/bin/smoke-project, so `uak start` said READY and then the first /uak-ship and the merge gate failed PRODUCT_UNVERIFIED; after two green merges the integrated app crashed on boot (ImportError) because tests forced a fake store and no gate booted the app; init-smoke left an empty scripts/ dir., Until .uak/bin/smoke-project exists, `uak start` shows the exact init-smoke command for the detected stack (or a generic one): a blocking TODO in sprint mode (the kit's own merge gate runs the product smoke) and a non-blocking NOTE in marathon mode (the human merges on the forge); existing tests that expect START READY on a fresh marathon install keep passing (Dylan's decision 2026-11-17); the generated smoke for a web stack starts the app and requests one route (bounded timeout), not only unit tests; init-smoke creates no stray folders.
- **Tests:** start_asks_for_the_smoke, web_smoke_boots_the_app, init_smoke_leaves_no_stray_dirs
- **Verify:** `python kit/.uak/tests/test_smoke_onboarding.py`
- **Next step:** fixture: stdlib Python app whose import is broken but unit tests pass; the generated smoke must fail; then implement.

## UAK-093 · The product smoke exists from the start and boots the app

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-091
- **Paths:** kit/.uak/bin/lib/smoke-init.sh, kit/.uak/bin/start, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_smoke_onboarding.py
- **Acceptance:** Evidence (QA round C, notes/handoff:qa/rounds-2026-11-14 C-1, C-3, C-10): nothing on the onboarding path created .uak/bin/smoke-project, so `uak start` said READY and then the first /uak-ship and the merge gate failed PRODUCT_UNVERIFIED; after two green merges the integrated app crashed on boot (ImportError) because tests forced a fake store and no gate booted the app; init-smoke left an empty scripts/ dir., Until .uak/bin/smoke-project exists, `uak start` shows the exact init-smoke command for the detected stack (or a generic one): a blocking TODO in sprint mode when an app is detected (the kit's own merge gate runs the product smoke), a non-blocking NOTE in sprint mode when no app is detected yet (a fresh hackathon has nothing to boot, so the first claim is not deadlocked), and a non-blocking NOTE in marathon mode (the human merges on the forge); existing tests that expect START READY on a fresh install keep passing (Dylan's decisions 2026-11-17 and 2026-11-18); the generated smoke for a web stack starts the app and requests one route (bounded timeout), not only unit tests; init-smoke creates no stray folders.
- **Tests:** start_asks_for_the_smoke, start_notes_the_smoke_before_any_app, web_smoke_boots_the_app, init_smoke_leaves_no_stray_dirs
- **Verify:** `python kit/.uak/tests/test_smoke_onboarding.py`
- **Next step:** fixture: stdlib Python app whose import is broken but unit tests pass; the generated smoke must fail; then implement.

## UI-024 · The team step leads a beginner through the first run

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2.5 h
- **Depends on:** UI-023
- **Paths:** kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_first_run.py, kit/.uak/tests/test_setup_team.py, kit/.uak/tests/test_setup_roles.py, kit/.uak/tests/test_setup_resume.py, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (QA notes/handoff:qa/rounds-2026-11-14 A-F6, A-F7, A-F15, A-F16, A-F19, B-10, D-3.2, D-6.1, D-7.1, D-10.1, D-10.2, D-1.1, D-1.2, D-9.2): Claude Code's trust dialog defaults to "No, exit" and shows an English 51-permissions warning the page never mentions; launch commands copyable before the reviewer is registered; "Comprobar siguiente paso" redraws the list and jumps 1,014 px; a hanging remote makes the check take 75 s with every view 409; blocked reasons shown 3 times; two 1–5 numberings; two humans never addressed; "Set up my project" below the fold; busy-disabled buttons without a reason; after a planner rule break the page says "Done" with a green lint box and conflicting undo advice., Trust step says "press ↓ then Enter" and that the warning is expected, and detects trust (Claude's own config) to show ✓/✗; launch commands stay locked until the reviewer is registered; the check keeps the old list dimmed until the new result (no jump) and network steps are bounded (results stay viewable during a check); one place per blocked reason; one step model; a two-person note (who runs what); CTA above the fold; every disabled button has a reason; a rule break reads "Terminó con problemas" with one undo instruction and its command.
- **Tests:** trust_step_is_explicit, commands_wait_for_the_reviewer, check_does_not_jump, views_answer_during_a_check, rule_break_is_not_done
- **Verify:** `python kit/.uak/tests/test_setup_first_run.py`
- **Next step:** reproduce with QA round A/D scripts; tests fail; fix.

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-026 · Fixes from the live run on turno-cafeteria-3

- **Type:** fix
- **Priority:** P2
- **Estimate:** 2 h
- **Depends on:** UI-025
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_live_run.py, CHANGELOG.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-19, kit next 9998cb4): (a) after a successful publish (origin/main had the commit) step 3 kept "Espera: se está publicando el kit.", "Listo a las 07:35." and the "Revisar los archivos" button; (b) with Claude Code's trust already ✓ the note still said "Hasta entonces ignora los permisos … el plan se detiene antes de tiempo"; (c) "Creando el plan…" gives no idea of duration (it takes 4–5 min); (d) the automatic check (every 60 s) took ~31 s for `uak start` alone and hit the 45 s bound, then blamed "origin no respondió en 45 s" while origin answered in 0.4 s; (e) the user pasted the implementer command inside the Claude Code session opened for the trust step, so the agent ran it as a tool call, stayed in the main folder and refused to code; (f) the implementer finished and pushed HACK-001 but stopped before /uak-ship (its prompt only says "Run /uak-start"), so the task never reached REVIEW and the reviewer waited idle (same as QA round A); (g) the board card said "0 commit(s) desde que se tomó" while feat/hack-001 had 2 pushed commits., (a) once publish succeeds step 3 reads "Publicado en main (commit abc1234)" and is marked done, with no busy line and no review button; (b) with trust ✓ only the ✓ line shows (the instruction to open Claude appears only on ✗ or unknown); (c) the plan button area says it usually takes about 5 minutes and shows elapsed time; (d) the check bound covers a normal `uak start` with margin (measure it; the bound is at least 2× a normal run on macOS and Windows), the timeout message names the step that was running instead of always blaming origin, and the automatic check does not start while the previous one runs; (e) every launch command says "Pégalo en una terminal nueva, no dentro de Claude ni Codex", and the trust step says to close that Claude session afterwards; (f) the implementer prompt (Claude and Codex) tells the agent to carry the task through /uak-ship (to REVIEW) and then take the next task, and the page says the task reaches "En revisión" by itself; (g) the card's commit line (taken from the agent's last heartbeat) is not shown as current when it is older than the task branch's last pushed commit: it shows the branch's pushed commit count, or says when the count was taken; every new string has its Spanish pair.
- **Tests:** publish_step_says_published, trusted_hides_the_open_claude_note, plan_says_how_long, check_timeout_names_the_step, commands_say_new_terminal, implementer_prompt_ships, card_counts_branch_commits
- **Verify:** `python kit/.uak/tests/test_setup_live_run.py`
- **Next step:** reproduce each item with the setup test helpers; tests fail; fix.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026, UAK-097
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-097 · The walking skeleton can merge the files the kit itself generates

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-093
- **Paths:** kit/.uak/bin/lib/review-merge.sh, kit/.uak/bin/lib/lint.sh, kit/.agents/skills/uak-plan/SKILL.md, kit/.uak/tests/test_skeleton_scope.py, kit/.uak/docs/WHY.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-19, turno-cafeteria-3, kit next 9998cb4): HACK-001 (the walking skeleton) followed its acceptance ("Dockerfile y render.yaml generados con uak deploy --write", "bash .uak/bin/smoke sale con 0") and UAK-093's start NOTE ("give that step to the walking-skeleton task"), but `uak done` warned that .dockerignore, .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance are outside its Paths, so the merge gate sends the task to the human queue: deploy --write writes three files while the planner listed two, and the smoke adapter is a shared resource that needs a human even when the plan the human approved names it., (1) when a task's Paths name Dockerfile or render.yaml, `uak lint` requires .dockerignore too (or the scope gate treats the three deploy --write outputs as one unit); (2) the scope gate lets a task ADD .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance when the base has no smoke-project and the task's Paths name those exact files (the human approved that plan); editing an existing adapter, or adding it without those Paths, still needs a human; (3) /uak-plan puts those two files and .dockerignore in the walking-skeleton task's Paths when the stack is deployable; (4) the human-queue reason for a shared file says which of these applies; WHY.md cites this run.
- **Tests:** dockerfile_paths_need_dockerignore, skeleton_adds_the_smoke_adapter, editing_the_adapter_still_needs_a_human, adapter_outside_paths_still_needs_a_human
- **Verify:** `python kit/.uak/tests/test_skeleton_scope.py`
- **Next step:** read rm scope check in review-merge.sh (shared list before Paths); fixture repo with a skeleton task; tests fail; fix.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026, UAK-097, UI-027
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026, UAK-097, UI-027, UI-028
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026, UAK-097, UI-027, UI-028, UI-029
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UAK-097 · The walking skeleton can merge the files the kit itself generates

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-093
- **Paths:** kit/.uak/bin/lib/review-merge.sh, kit/.uak/bin/lib/lint.sh, kit/.agents/skills/uak-plan/SKILL.md, kit/.claude/commands/uak-plan.md, kit/.gemini/commands/uak-plan.toml, kit/.uak/tests/test_skeleton_scope.py, kit/.uak/docs/WHY.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-19, turno-cafeteria-3, kit next 9998cb4): HACK-001 (the walking skeleton) followed its acceptance ("Dockerfile y render.yaml generados con uak deploy --write", "bash .uak/bin/smoke sale con 0") and UAK-093's start NOTE ("give that step to the walking-skeleton task"), but `uak done` warned that .dockerignore, .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance are outside its Paths, so the merge gate sends the task to the human queue: deploy --write writes three files while the planner listed two, and the smoke adapter is a shared resource that needs a human even when the plan the human approved names it., (1) when a task's Paths name Dockerfile or render.yaml, `uak lint` requires .dockerignore too (or the scope gate treats the three deploy --write outputs as one unit); (2) the scope gate lets a task ADD .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance when the base has no smoke-project and the task's Paths name those exact files (the human approved that plan); editing an existing adapter, or adding it without those Paths, still needs a human; (3) /uak-plan puts those two files and .dockerignore in the walking-skeleton task's Paths when the stack is deployable; (4) the human-queue reason for a shared file says which of these applies; WHY.md cites this run.
- **Tests:** dockerfile_paths_need_dockerignore, skeleton_adds_the_smoke_adapter, editing_the_adapter_still_needs_a_human, adapter_outside_paths_still_needs_a_human
- **Verify:** `python kit/.uak/tests/test_skeleton_scope.py`
- **Next step:** read rm scope check in review-merge.sh (shared list before Paths); fixture repo with a skeleton task; tests fail; fix.
## UAK-097 · The walking skeleton can merge the files the kit itself generates

- **Type:** fix
- **Priority:** P1
- **Estimate:** 2 h
- **Depends on:** UAK-093
- **Paths:** kit/.uak/bin/lib/review-merge.sh, kit/.uak/bin/lib/lint.sh, kit/.agents/skills/uak-plan/SKILL.md, kit/.claude/commands/uak-plan.md, kit/.gemini/commands/uak-plan.toml, kit/.uak/tests/test_skeleton_scope.py, kit/.uak/docs/WHY.md, kit/.uak/settings/known-files.txt
- **Acceptance:** Evidence (Dylan's live run 2026-11-19, turno-cafeteria-3, kit next 9998cb4): HACK-001 (the walking skeleton) followed its acceptance ("Dockerfile y render.yaml generados con uak deploy --write", "bash .uak/bin/smoke sale con 0") and UAK-093's start NOTE ("give that step to the walking-skeleton task"), but `uak done` warned that .dockerignore, .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance are outside its Paths, so the merge gate sends the task to the human queue: deploy --write writes three files while the planner listed two, and the smoke adapter is a shared resource that needs a human even when the plan the human approved names it., (1) when a task's Paths name Dockerfile or render.yaml, `uak lint` requires .dockerignore too (or the scope gate treats the three deploy --write outputs as one unit); (2) the scope gate lets a task ADD .uak/bin/smoke-project and .uak/bin/.smoke-project.provenance when the base has no smoke-project and the task's Paths name those exact files (the human approved that plan); editing an existing adapter, or adding it without those Paths, still needs a human; (3) /uak-plan puts those two files and .dockerignore in the walking-skeleton task's Paths when the stack is deployable; (4) the human-queue reason for a shared file says which of these applies; WHY.md cites this run.
- **Tests:** dockerfile_paths_need_dockerignore, skeleton_adds_the_smoke_adapter, editing_the_adapter_still_needs_a_human, adapter_outside_paths_still_needs_a_human
- **Verify:** `python kit/.uak/tests/test_skeleton_scope.py`
- **Next step:** read rm scope check in review-merge.sh (shared list before Paths); fixture repo with a skeleton task; tests fail; fix.
## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004, UAK-010, UI-005, UI-006, UI-007, UAK-067, UI-008, UI-009, UI-010, UI-012, UAK-069, UI-015, UAK-090, UI-016, UI-017, UI-018, UAK-091, UAK-092, UAK-093, UAK-094, UAK-095, UI-019, UI-020, UI-021, UI-023, UI-024, UI-025, UI-026, UAK-097, UI-027, UI-028, UI-029, UAK-098, UI-030
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:** the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical, the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes, docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)

## UI-028 · A help chat on the page answers "what now?" with the cheapest model

- **Type:** feature
- **Priority:** P2
- **Estimate:** 4 h
- **Depends on:** UI-027
- **Paths:** kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/help_chat.py, kit/.uak/tests/test_setup_help_chat.py, kit/.uak/docs/SECURITY.md, kit/.uak/docs/WHY.md, CHANGELOG.md, docs/DASHBOARD.md
- **Acceptance:** Evidence (Dylan's live run 2026-11-19, turno-cafeteria-3): at almost every hand-off the human left the page to ask another assistant "what next?", "what does esperando dependencias mean?", "why does Codex do nothing?", "where do I paste this?"; Dylan asked for a help chat on the most visible part of the page that uses the cheapest model of the tool in use so it barely spends quota., A help panel reachable from every tab (button in the top bar) takes a question and answers in the page's language: (1) common questions ("¿qué sigue?", what a state or word means, why a task waits) are answered locally from the page's own state and glossary, without a model; (2) other questions run the person's own coding tool headless with its cheapest model (Claude Code: `claude -p --model haiku`; Codex: its mini model, verified against Codex's docs at implementation time), the tool chosen from the ones setup already detects, never an API key; (3) the model gets a bounded context: the current step, guidance, task states, notices, glossary and the kit's short user guide, with task titles and agent messages marked as untrusted data; (4) the chat is read-only: no tools (no Bash, no edits, no MCP), it may show a command for the human to copy but never runs one, and it never suggests running a UAK_HUMAN command inside an agent session; (5) cost bounds: answers capped in length, one request at a time, a per-minute limit, a visible "usa tu cuota de <tool> (modelo económico)" note, and a clear message when no tool is available or the call fails or times out (bounded, process tree killed); (6) every new string has its Spanish pair; SECURITY.md records the read-only and untrusted-data rules.
- **Tests:** local_answer_needs_no_model, model_call_uses_cheapest_and_no_tools, context_marks_untrusted_data, chat_never_runs_commands, rate_limit_and_timeout, no_tool_says_why
- **Verify:** `python kit/.uak/tests/test_setup_help_chat.py`
- **Next step:** design contract with the mentor (prompt, context pack, local intents, tool flags); fake `claude`/`codex` binaries in tests; then implement.
## UAK-098 · The kit reads an existing repo and plans only what is new

- **Type:** feature
- **Priority:** P2
- **Estimate:** 4 h
- **Depends on:** UAK-097, UAK-099
- **Paths:** kit/.uak/bin/survey, kit/.uak/bin/lib/commands.tsv, kit/.uak/docs/CLI.md, kit/.uak/templates/STATE.template.md, kit/.uak/templates/TASKS.template.md, kit/.uak/templates/IDEA.template.md, kit/.uak/bin/lib/lint.sh, kit/.claude/commands/uak-plan.md, kit/.agents/skills/uak-plan/SKILL.md, kit/.gemini/commands/uak-plan.toml, kit/.uak/settings/known-files.txt, kit/.uak/tests/test_continue_project.py, kit/.uak/docs/WHY.md
- **Acceptance:** Evidence (Dylan's proposal 2026-11-19): a person wants to hand the kit a repo they worked on before, have it analyzed, say what to add, and continue where it stopped; today install works on any repo and `uak map`, `uak deploy` and init-smoke read existing code, but /uak-plan always plans from zero (Setup P0, contract, walking skeleton from IDEA.md), so on a repo with code it would plan to rebuild what exists, and nothing records what is done, half done or missing., (1) `uak survey [--write]` (read-only without --write, no network, no LLM) writes `.uak/STATE.md` from `.uak/templates/STATE.template.md`: stack and run/test commands detected (deploy and init-smoke detection), the code map's areas and entry points, test files and the result of the detected test command when it is bounded and safe to run (or "not run" with why), open TODO/FIXME counts per area, branches not merged into the base, and the last commits; untrusted repo text is quoted, never followed; (2) /uak-plan has a "continue" path when `.uak/STATE.md` exists and the code is not empty: it reads STATE.md and the human's request (IDEA.md section "Qué quiero agregar"), plans only new or unfinished work, adds no Setup/skeleton task for what already runs, sets each task's Paths on real files and lists their importers from `uak map impact`, and reuses the existing smoke or makes "create the product smoke for the existing app" the first task when none exists; (3) a test fixture repo with a working app plus a half-done feature gets a plan with no rebuild task and a task that finishes the half-done feature; (4) WHY.md cites this proposal.
- **Tests:** survey_is_read_only_by_default, survey_writes_state_with_stack_and_tests, plan_continue_skips_existing_setup, plan_continue_finishes_half_done_work
- **Verify:** `python kit/.uak/tests/test_continue_project.py`
- **Next step:** design contract with the mentor (STATE.md shape, how the planner proves it is not rebuilding, safety of running the detected tests); fixture repo; tests fail; implement.

