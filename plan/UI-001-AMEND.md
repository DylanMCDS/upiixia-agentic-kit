# Unified bilingual workspace amendment

## UI-001 · Configure a new project in a local browser from step zero

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** None
- **Paths:** install.sh, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_wizard.py, kit/.uak/tests/test_unified_workspace.py
- **Acceptance:**
  - An explicit wizard entry point opens a local browser before asking for installation choices; existing scripted installs and updates remain compatible.
  - Guide repository selection, prerequisites, an explicit sprint or marathon decision, coding tools, installation review, installation progress, and subsequent project configuration in one interface.
  - Reuse the existing installer with literal argument arrays and no shell interpolation; validate options before running it. Prevent duplicate concurrent installs.
  - Distinguish installation success from readiness to claim a task. Reuse uak start checks; show blockers and the next corrective action. Do not manufacture approvals, credentials, tasks, or agent identities.
  - Serve only explicit assets on 127.0.0.1. Validate Host, Origin, session token, JSON schema, and body size for mutations. Do not expose repository files, environment variables, or arbitrary command execution.
  - Persist only explicitly allowed project settings atomically, preserving unrelated content. Approval and review authority are outside the browser write API.
  - The UI renders offline with actionable empty, loading, and error states. Keep technical output in an expandable details panel.
- **Acceptance (human clarification):** Spanish/English can be switched without losing input; configuration and the existing dashboard share one local application and persistent preferences; Back is available after Welcome, preserving inputs and preventing duplicate writes during active operations. User-facing Spanish translations are explicitly authorized; source code and contributor documentation remain English.
- **Tests:** wizard_starts_before_installation, legacy_install_remains_noninteractive, invalid_requests_cannot_mutate, installer_arguments_are_literal, duplicate_install_is_rejected, setup_preserves_unrelated_settings, installed_is_not_ready
- **Verify:** `python kit/.uak/tests/test_setup_wizard.py && python kit/.uak/tests/test_unified_workspace.py`
- **Next step:** write failing behavior tests and record uak red before implementation; agree the wizard contract with the reviewer.

