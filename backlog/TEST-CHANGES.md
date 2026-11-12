# Existing tests a human allowed to change (uak allow --tests)

Append-only. Format: - ID | epoch | human | reason. Why: a test is a spec; changing one is a human decision.

- UAK-010 | 1794415983 | Dylan | test_dashboard_journey asserted the UAK-010 bug (a failed install looked installed); it now asserts the files are on disk but not installed, and that readiness asks for Repair
- UAK-013 | 1794455184 | Dylan | Dylan explicitly authorized this command in chat; add synchronization and Windows cleanup waits in test_hook_claims without changing assertions
