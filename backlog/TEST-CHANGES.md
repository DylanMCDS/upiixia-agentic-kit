# Existing tests a human allowed to change (uak allow --tests)

Append-only. Format: - ID | epoch | human | reason. Why: a test is a spec; changing one is a human decision.

- UAK-010 | 1794415983 | Dylan | test_dashboard_journey asserted the UAK-010 bug (a failed install looked installed); it now asserts the files are on disk but not installed, and that readiness asks for Repair
- UAK-013 | 1794455184 | Dylan | Dylan explicitly authorized this command in chat; add synchronization and Windows cleanup waits in test_hook_claims without changing assertions
- UI-009 | 1794589480 | Dylan | the Codex reviewer command gains --sandbox/--add-dir (acceptance of UI-009); agent_launch_commands_are_exact pinned the old line
- UI-015 | 1794602090 | Dylan | Windows test robustness: git() helper decodes UTF-8; schedule_never_follows_links skips when the OS cannot create a symlink (qa/windows/UI-010-1401.md)
