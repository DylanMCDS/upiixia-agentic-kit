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
