# STATE

Phase: execution
Updated: 1794672841
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UAK-093 UI-020 UI-021 UI-022 UI-023 UI-024 UAK-096 
CLAIMED: UAK-091 UAK-092 UAK-094 UAK-095 UI-019 
BLOCKED: -
REVIEW: -
INTEGRATED: (24; last 12) ... UI-004 UI-005 UI-006 UI-007 UI-008 UI-009 UI-010 UI-012 UI-015 UI-016 UI-017 UI-018 
CANCELLED: UI-011 UI-013 UI-014 

Claims (first 24; status --task ID shows detail):
UAK-091 | CLAIMED | claude-Dylan-2 | until 1794669926 (EXPIRED: release --expired --read-summary TOKEN)
UAK-092 | CLAIMED | claude-Dylan-4 | until 1794669887 (EXPIRED: release --expired --read-summary TOKEN)
UAK-094 | CLAIMED | claude-Dylan-5 | until 1794669880 (EXPIRED: release --expired --read-summary TOKEN)
UAK-095 | CLAIMED | claude-Dylan-6 | until 1794669914 (EXPIRED: release --expired --read-summary TOKEN)
UI-019 | CLAIMED | claude-Dylan-3 | until 1794671419 (EXPIRED: release --expired --read-summary TOKEN)

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794672841 | deadline lease/UAK-091/1794669926 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UAK-092/1794669887 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UAK-094/1794669880 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UAK-095/1794669914 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794672841 | deadline lease/UI-019/1794671419 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
