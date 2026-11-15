# STATE

Phase: execution
Updated: 1794721653
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UAK-093 UI-020 UI-021 UI-022 UI-023 UI-024 UAK-096 
CLAIMED: -
BLOCKED: -
REVIEW: UAK-091 UAK-094 UAK-095 UI-019 
INTEGRATED: (25; last 12) ... UI-004 UI-005 UI-006 UI-007 UI-008 UI-009 UI-010 UI-012 UI-015 UI-016 UI-017 UI-018 
CANCELLED: UI-011 UI-013 UI-014 

Claims (first 24; status --task ID shows detail):
UAK-091 | REVIEW | claude-Dylan-2 | until 1794804390
UAK-094 | REVIEW | claude-Dylan-5 | until 1794804399
UAK-095 | REVIEW | claude-Dylan-6 | until 1794804734
UI-019 | REVIEW | claude-Dylan-3 | until 1794807678

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794672841 | deadline lease/UAK-092/1794669887 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UAK-094/1794669880 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UAK-095/1794669914 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UI-019/1794671419 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794717917 | plan --amend | Dylan/Dylan | amended: UI-019 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
