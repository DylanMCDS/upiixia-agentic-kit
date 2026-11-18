# STATE

Phase: execution
Updated: 1794967701
AVAILABLE: UAK-001 UAK-002 UAK-003 UAK-004 UAK-005 UAK-006 UAK-007 UAK-008 UI-023 UI-024 
CLAIMED: UAK-093 UI-021 
BLOCKED: -
REVIEW: UAK-096 
INTEGRATED: (30; last 12) ... UI-006 UI-007 UI-008 UI-009 UI-010 UI-012 UI-015 UI-016 UI-017 UI-018 UI-019 UI-020 
CANCELLED: UI-011 UI-013 UI-014 UI-022 

Claims (first 24; status --task ID shows detail):
UAK-093 | CLAIMED | claude-Dylan-2 | until 1794970906
UAK-096 | REVIEW | claude-Dylan-6 | until 1795053224
UI-021 | CLAIMED | claude-Dylan-3 | until 1794980541

Blockers: BLOCKED tasks; use status --task ID --summary.
Current decisions (last 5):
- 1794953524 | plan --amend | Dylan/Dylan | amended: UI-020 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_
- 1794953545 | plan --amend | Dylan/Dylan | amended: UI-020 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_
- 1794953550 | plan --amend | Dylan/Dylan | amended: UI-021 Paths: kit/.uak/bin/lib/setup.py, kit/.uak/bin/lib/setup.html, kit/.uak/bin/lib/workspace.js, kit/.uak/tests/test_setup_
- 1794956530 | plan --amend | Dylan/Dylan | amended: UAK-096 | Why: scope or criteria fixed before review
- 1794966686 | plan --amend | Dylan/Dylan | amended: UAK-096 Paths: kit/.agents/skills/uak-plan/SKILL.md, kit/.claude/commands/uak-plan.md, install.sh, kit/.uak/tests/test_plan_sca

Global next step: available P0; else review PRs, tests, demo, rehearsal.
Why: bounded snapshot to resume without rereading history.
