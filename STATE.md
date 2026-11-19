# STATE

Phase: execution
Updated: 1795097207
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 
CLAIMED: -
BLOCKED: -
REVIEW: -
INTEGRATED: (35; last 12) ... UI-009 UI-010 UI-012 UI-015 UI-016 UI-017 UI-018 UI-019 UI-020 UI-021 UI-023 UI-024 
CANCELLED: UI-011 UI-013 UI-014 UI-022 

Claims (first 24; status --task ID shows detail):

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794986278 | plan --amend | Dylan/Dylan | amended: UAK-093 Paths: kit/.uak/bin/lib/smoke-init.sh, kit/.uak/bin/start, kit/.uak/tests/test_smoke_onboarding.py → kit/.uak/bin/lib
- 1795050198 | allow | Dylan | test change: UI-024 | Why: UI-024 locks agent commands until the reviewer is registered; existing team/roles/resume tests use a ready_team() helper t
- 1795050291 | plan --amend | Dylan/Dylan | amended: UAK-093 | Why: scope or criteria fixed before review
- 1795060110 | plan --amend | Dylan/Dylan | amended: UI-024 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_
- 1795097207 | plan | Dylan/Dylan | tasks added: UI-025 UI-026 | Why: backlog without PR (Plan-Channel: claims)

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
