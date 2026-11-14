# STATE

Phase: execution
Updated: 1794656422
AVAILABLE: (16; last 12) ... UAK-005 UAK-006 UAK-007 UAK-008 UAK-093 UI-019 UI-020 UI-021 UI-022 UI-023 UI-024 UAK-096 
CLAIMED: UAK-091 UAK-092 UAK-094 UAK-095 
BLOCKED: -
REVIEW: UI-018 
INTEGRATED: (23; last 12) ... UI-003 UI-004 UI-005 UI-006 UI-007 UI-008 UI-009 UI-010 UI-012 UI-015 UI-016 UI-017 
CANCELLED: UI-011 UI-013 UI-014 

Claims (first 24; status --task ID shows detail):
UAK-091 | CLAIMED | claude-Dylan-2 | until 1794669926
UAK-092 | CLAIMED | claude-Dylan-4 | until 1794669887
UAK-094 | CLAIMED | claude-Dylan-5 | until 1794669880
UAK-095 | CLAIMED | claude-Dylan-6 | until 1794669914
UI-018 | REVIEW | claude-Dylan-3 | until 1794742822

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794629679 | plan --amend | Dylan/Dylan | amended: UI-018 | Why: scope or criteria fixed before review
- 1794654984 | deadline lease/UI-018/1794643734 | REQUIRES_RECOVERY | Claim kept; read the summary and use release --expired --read-summary. No work is deleted.
- 1794655398 | plan | Dylan/Dylan | tasks added: UAK-091 UAK-092 UAK-093 UAK-094 UAK-095 UI-019 UI-020 UI-021 UI-022 UI-023 UI-024 UAK-096 | Why: backlog without PR (Plan-Channel: 
- 1794655406 | plan --amend | Dylan/Dylan | amended: UAK-006 | Why: scope or criteria fixed before review
- 1794656056 | plan --amend | Dylan/Dylan | amended: UAK-094 Paths: kit/.uak/bin/lib/status.sh, kit/.uak/bin/lib/messages.sh, kit/.uak/bin/stats, kit/.uak/bin/board, kit/.uak/bin/d

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
