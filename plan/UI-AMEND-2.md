## UAK-006 · Proof of no change, and the targets turned on

- **Type:** integration
- **Priority:** P0
- **Estimate:** 4 h
- **Depends on:** UAK-003, UAK-004, UAK-005, UAK-008, UI-002, UI-004
- **Paths:** scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md
- **Acceptance:**
  - the protocol suites run the old and the new engine side by side on the same fixtures: every command's stdout and the resulting claims tree are identical
  - the XFAIL set of test_claims_perf.py is empty: next ≤ 40, status ≤ 30, heartbeat ≤ 20 processes
  - docs/perf-windows.md has the before and after times from `scripts/perf_claims.sh` on Windows
- **Tests:** old_and_new_engines_print_the_same_and_write_the_same_tree
- **Verify:** `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`
- **Next step:** reuse the guard differential of v5.9.2 (docs/perf-windows.md)


## UI-002 · Make the dashboard approachable with a guided beginner profile

- **Type:** feature
- **Priority:** P1
- **Estimate:** 1 day
- **Depends on:** UI-001
- **Paths:** kit/.uak/bin/lib/dash.html, kit/.uak/bin/lib/dash.py, kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/templates/PROJECT.sprint.md, kit/.uak/templates/PROJECT.marathon.md, kit/.uak/docs/CLI.md, kit/.uak/tests/test_dashboard_profiles.py
- **Acceptance:**
  - Offer Beginner and Advanced presentation profiles with a persistent, reversible choice. Neither profile changes permissions, operational mode, or coordination gates.
  - Beginner is almost fully guided for someone who never used the kit: one step per screen, one primary action, one sentence on why it matters, and the completed steps as a short checklist.
  - The current step comes only from the readiness gate (`uak start`) until the project is ready, and from its ready line afterwards; Beginner never contradicts Configuration.
  - A step that happens outside the browser shows the exact command with a Copy button and where to paste it; the browser never approves or publishes on the human's behalf outside the approval flow of UI-004.
  - The state is rechecked automatically (on an interval and when the tab regains focus); a completed step advances and is announced politely to assistive technology.
  - When the project becomes ready, the interface opens project progress: percentage, tasks in plain language, and the next action.
  - No jargon (claims, worktree, command names) outside the copy block; an unavoidable term has a one-line explanation. Advanced and Technical details stay one click away from every step.
  - Keyboard navigation, visible focus, labelled controls, reduced motion, readable contrast, and 390px layouts work. Render all untrusted content as text.
  - A "Your app" section links to the deployed application when one exists. The URL lives in a new `Live-URL:` key of `.uak/PROJECT.md` (read with `uak_cfg`, documented in CLI.md and both templates), editable in the interface as an allowlisted setting: only an absolute `https://` URL with no credentials, saved atomically. The link opens in a new tab with `rel="noopener noreferrer"`. Without a URL, the section says the app is not deployed yet and points to the deploy step; it never guesses a URL.
  - Preserve offline static dashboard export, dark/light themes, task/review information, and existing dashboard contracts.
- **Tests:** beginner_profile_persists, advanced_profile_preserves_details, next_action_matches_real_state, hostile_content_is_text, static_dashboard_remains_offline, beginner_shows_one_action, copy_command_is_exact, ready_opens_progress, live_url_is_https_only, live_url_link_is_shown_when_set
- **Verify:** `python kit/.uak/tests/test_dashboard_profiles.py`
- **Next step:** reuse UI-001's guidance contract (/api/status and /api/dashboard `guidance`); write failing profile tests.
