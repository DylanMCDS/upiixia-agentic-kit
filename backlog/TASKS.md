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
