# STATE

Phase: execution
Updated: 1794493263
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UI-006 UI-007 UAK-012 
CLAIMED: -
BLOCKED: -
REVIEW: UAK-013 UI-005 
INTEGRATED: UAK-009 UAK-010 UAK-011 UI-001 UI-002 UI-003 UI-004 
CANCELLED: -

Claims (first 24; status --task ID shows detail):
UAK-013 | REVIEW | claude-Dylan | until 1794579521
UI-005 | REVIEW | claude-Dylan | until 1794535909

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794443979 | deadline lease/UI-005/1794440637 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794444186 | plan | Dylan/Dylan | tasks added: UAK-011 UAK-012 UAK-013 | Why: backlog without PR (Plan-Channel: claims)
- 1794447400 | plan --amend | Dylan/Dylan | amended: UI-005 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/bin/lib/planning.
- 1794452196 | plan --amend | Dylan/Dylan | amended: UAK-013 Paths: kit/.uak/bin/hook, kit/.uak/tests/test_hook_session_start_speed.py → kit/.uak/bin/hook, kit/.uak/tests/test_ho
- 1794455184 | allow | Dylan | test change: UAK-013 | Why: Dylan explicitly authorized this command in chat; add synchronization and Windows cleanup waits in test_hook_claims witho

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
