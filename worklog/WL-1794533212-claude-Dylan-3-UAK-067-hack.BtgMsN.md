# worklog/WL-1794533212-claude-Dylan-3-UAK-067-hack.BtgMsN.md · UAK-067

## Live summary
- Done: Claim created; implementation pending
- Decision: Own branch and worktree
- Why: Parallel work without touching the main checkout
- Failing: No validation run yet
- Commands: `python kit/.uak/tests/test_ci_once.py`
- Next: write test_ci_once.py so it reads ../.github/workflows/test.yml (skip when absent, as in an installed project) and calls kit_lint's new check; see it fail on main; then change the triggers and add the concurrency block.

## History
- 1794533212 | CLAIMED | claude-Dylan-3 | claim; next: write test_ci_once.py so it reads ../.github/workflows/test.yml (skip when absent, as in an installed project) and calls kit_lint's new check; see it fail on main; then change the triggers and add the concurrency block.
