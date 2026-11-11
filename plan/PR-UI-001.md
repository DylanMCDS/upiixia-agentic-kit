## UI-001 · Configure a new project in a local browser from step zero

`bash install.sh --wizard [TARGET] [--no-open]` opens a loopback-only setup page before any installation choice. The page covers welcome, repository, workflow and tools, review and install, and readiness. It shares one interface with the existing team dashboard (Beginner and Advanced presentation, Spanish/English, light/dark).

### What this branch contains
- `efa591e` visual setup wizard (gpt-Dylan)
- `ddcd44b` unified bilingual setup and dashboard navigation (gpt-Dylan)
- `5d50cc1` fixes from claude-Dylan's pre-review and a mentor audit:
  - one next step derived from `uak start` for Configuration and the dashboard; only the exact claim command is copyable;
  - a ready check opens project progress;
  - installed projects (no installer next to setup) and Git Bash's `$BASH` are handled;
  - nested JSON gets a 400;
  - the dashboard distinguishes no remote from a failed refresh.

### Safety boundary
- Binds 127.0.0.1 only.
- Mutations check Host, Origin, session token, JSON content type and a 64 KB body limit.
- The installer gets a literal argument list.
- Browser writes are limited to Blackbox and Pace, written atomically.
- No approval, identity or remote change from the browser.
- The dashboard iframe is sandboxed without same-origin.

### Verification (Windows 11, Python 3.13.7, Git Bash)
| Check | Result |
|---|---|
| Verify: `test_setup_wizard.py` / `test_unified_workspace.py` | 14/14 / 9/9 PASS |
| The same two files through an installed project's `smoke --package-only` | failed=0 |
| `test_v51 --case dashboard_shows_everything`, `test_v57_install` | PASS |
| `gen_harness --check` | PASS |
| `kit_hashes --check` | up to date |
| Browser (Edge, 1280x720 and 390x844, reduced motion) | guidance todo/ready, auto-open progress, no JS errors, no horizontal overflow |

`kit_lint` on Windows reports only 31 executable-bit findings for unchanged Bash files; Linux/macOS CI must confirm. The full package smoke on Windows has failures unrelated to this branch (`test_claims_perf::the_counter_sees_ps`, symlink privilege WinError 1314); see the task evidence.

Reviewer: gpt-Dylan (independent). Final merge: Dylan.
