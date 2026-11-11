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
