## UI-002 · Make the dashboard approachable with a guided beginner profile

Builds on UI-001 (PR #1, integrated).

### What changes
- **Guided Beginner.** One step at a time, taken from the readiness gate (`uak start`). Each step shows:
  - the step itself and why it matters;
  - the gate's passed steps as an "Already done" checklist;
  - exactly one primary action.

  An automatic re-check runs on tab focus and every minute while a blocker is shown, and it announces a completed step. Only the exact claim command is ever copyable.
- **Your app.** A new `Live-URL` key in `.uak/PROJECT.md`, set to `-` in both templates and documented in CLI.md, adds a link to the deployed app.
  - It accepts only an absolute `https://` URL with a host and no credentials, and never guesses one.
  - The dashboard reads it from the base branch's PROJECT.md. Claims' `meta/config.md` carries only engine keys, so no engine change is needed. In local mode it reads the local file, and the static `uak dash` export carries it too.
  - The setup page edits it as an allowlisted, validated setting, and adds the key atomically to an older PROJECT.md.
  - The link opens with `target=_blank rel="noopener noreferrer"`.
- **macOS findings from UI-001:**
  - D1: Configuration's headline follows the gate's step.
  - D2: the review lists tool product names (Claude Code, Gemini CLI…).
  - D3: the review says the install adds `.mcp.json`.

### Verification (Windows 11, Python 3.13.7)
| Check | Result |
|---|---|
| Verify `test_dashboard_profiles.py` (10 task names + atomic save) | 11/11 PASS; red recorded first at 126582e |
| `test_setup_wizard.py`, `test_unified_workspace.py` | 14/14, 9/9 |
| `test_v51 --case dashboard_shows_everything`, `test_v57_install` | PASS |
| `gen_harness --check` | PASS |
| Browser (Edge, 1280x720 and 390x844 es-MX, reduced motion) | guided step, checklist, one primary action, https-only save, Your app link, 0 JS errors, no overflow |

`kit_lint` and `kit_hashes` on this Windows CRLF checkout are not conclusive; CI decides. Paths are amended to include `workspace.js` (the Spanish strings) and `known-files.txt`.

Reviewer: gpt-Dylan (independent). Final merge: Dylan.
