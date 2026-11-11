# Pending improvements (not planned yet)

Ideas found while building and testing the visual setup. None is a task yet: Dylan decides which become one
(`UAK_HUMAN=Dylan bash .uak/bin/uak plan FILE`). Ask claude-Dylan "¿hay mejoras pendientes?" to review this list.

| # | Improvement | Why / evidence | Found |
|---|---|---|---|
| 1 | A command to reopen the setup page from an installed project (e.g. `bash .uak/bin/uak setup`) | Today the page only starts from the kit's clone (`install.sh --wizard`); an installed project has `.uak/bin/lib/setup.py` but no command for it. A teammate (Joahan) asked whether the kit must be installed to run the installer. | 2026-11-11, PR review chat |
| 2 | Translate the Advanced dashboard and remove the repeated status text | In Spanish, parts of the detailed panel stay in English ("Agents online", "0 of 4 tasks integrated"), and the notice under the title repeats "Tu proyecto de un vistazo". | 2026-11-11, demo video |
| 3 | Make `test_v3::guard_subagent_budget` hermetic | It reads the machine's real usage pace ("pace critical" lowers Max-Parallel-Subagents to 1), so it fails on Dylan's Mac and on main alike. | 2026-11-11, UI-002 smoke on macOS |
| 4 | Local test runs under a global `core.hooksPath` | `test_tokens_coverage::publish_failure_is_recorded` fails when `~/.gitconfig` sets `core.hooksPath` (the test remote's pre-receive hook is skipped). Tests could pin `core.hooksPath` in their fixtures. | 2026-11-11, UI-002 smoke on macOS |
