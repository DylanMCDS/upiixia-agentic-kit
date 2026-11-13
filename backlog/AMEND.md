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

