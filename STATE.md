# STATE

Phase: execution
Updated: 1794446872
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UI-006 UI-007 UAK-012 UAK-013 
CLAIMED: -
BLOCKED: -
REVIEW: UAK-011 UI-005 
INTEGRATED: UAK-009 UAK-010 UI-001 UI-002 UI-003 UI-004 
CANCELLED: -

Claims (first 24; status --task ID shows detail):
UAK-011 | REVIEW | gpt-Dylan | until 1794533261
UI-005 | REVIEW | claude-Dylan | until 1794531282

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794415983 | allow | Dylan | test change: UAK-010 | Why: test_dashboard_journey asserted the UAK-010 bug (a failed install looked installed); it now asserts the files are on disk
- 1794426182 | plan | Dylan/Dylan | tasks added: UI-005 UI-006 UI-007 | Why: backlog without PR (Plan-Channel: claims)
- 1794426214 | plan --amend | Dylan/Dylan | amended: UAK-006 | Why: scope or criteria fixed before review
- 1794443979 | deadline lease/UI-005/1794440637 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794444186 | plan | Dylan/Dylan | tasks added: UAK-011 UAK-012 UAK-013 | Why: backlog without PR (Plan-Channel: claims)

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
