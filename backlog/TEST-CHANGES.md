# Existing tests a human allowed to change (uak allow --tests)

Append-only. Format: - ID | epoch | human | reason. Why: a test is a spec; changing one is a human decision.

- UAK-010 | 1794415983 | Dylan | test_dashboard_journey asserted the UAK-010 bug (a failed install looked installed); it now asserts the files are on disk but not installed, and that readiness asks for Repair
- UAK-013 | 1794455184 | Dylan | Dylan explicitly authorized this command in chat; add synchronization and Windows cleanup waits in test_hook_claims without changing assertions
- UI-009 | 1794589480 | Dylan | the Codex reviewer command gains --sandbox/--add-dir (acceptance of UI-009); agent_launch_commands_are_exact pinned the old line
- UI-015 | 1794602090 | Dylan | Windows test robustness: git() helper decodes UTF-8; schedule_never_follows_links skips when the OS cannot create a symlink (qa/windows/UI-010-1401.md)
- UI-024 | 1795050198 | Dylan | UI-024 locks agent commands until the reviewer is registered; existing team/roles/resume tests use a ready_team() helper that registers the reviewer first (no assertion weakened)
- UI-026 | 1795114867 | Dylan | UI-026 (d) raises the 45 s check bound and names the slow step; (f) the implementer prompt carries the task through /uak-ship: update the expected values in test_setup_first_run (437, 441), test_setup_team (545-546), test_setup_roles (65-66); no check weakened
- UAK-099 | 1795136059 | Dylan | UAK-099 reverses UAK-097's render.yaml-only rule: test_skeleton_scope.py:90 expected a static render.yaml task to fail lint; it now must pass, and a Dockerfile without .dockerignore must still fail
- UAK-100 | 1795139830 | Dylan | UAK-100 replaces the idle line that tells agents to wait (the Codex wait-loop incident): update the expected golden string at test_claims_read.py:218 only; the golden check itself is unchanged
