# STATE

Phase: execution
Updated: 1794609618
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UI-012 UI-015 
CLAIMED: -
BLOCKED: -
REVIEW: -
INTEGRATED: (19; last 12) ... UAK-069 UAK-090 UI-001 UI-002 UI-003 UI-004 UI-005 UI-006 UI-007 UI-008 UI-009 UI-010 
CANCELLED: UI-011 UI-013 UI-014 

Claims (first 24; status --task ID shows detail):

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794593048 | plan --amend | Dylan/Dylan | amended: UI-009 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/tests/test_setup_team.py, docs/DASHBOARD.md, kit
- 1794601802 | UI-015 | follow-up of UI-010 by claude-Dylan: Windows: one 10 s grace for both pipe readers; tests read git output as UTF-8 and skip the symlink case without symlink
- 1794602090 | allow | Dylan | test change: UI-015 | Why: Windows test robustness: git() helper decodes UTF-8; schedule_never_follows_links skips when the OS cannot create a symlin
- 1794603474 | plan | Dylan/Dylan | tasks added: UAK-090 | Why: backlog without PR (Plan-Channel: claims)
- 1794603485 | plan --amend | Dylan/Dylan | amended: UAK-006 | Why: scope or criteria fixed before review

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
