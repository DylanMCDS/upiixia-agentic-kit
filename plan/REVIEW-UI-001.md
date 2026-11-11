# UI-001 pre-review packet

Author: gpt-Dylan. Reviewer: claude-Dylan. Human: Dylan.

- Fork: https://github.com/DylanMCDS/upiixia-agentic-kit.git
- Branch: feat/ui-001
- Exact pushed SHA: ddcd44ba6c2606269a9a297da581f514e4a40782
- Base: 87af1682fb1c683a21936b711889d2461e74be36
- Author worktree: C:/Users/dylan/OneDrive/Documentos/Repositorios/Hackathon/upiixia-agentic-kit-wt/ui-001
- State: CLAIMED, not formally shipped. No PR opened and no approval requested yet.

## What changed

An explicit `bash install.sh --wizard [TARGET] [--no-open]` opens local setup before installation choices. A five-step interface covers welcome, repository selection, explicit workflow/tool selection, review/install, and continuing preferences/readiness checks. The human expanded UI-001 to include Spanish/English, Back navigation, and the existing dashboard in the same application; the amended plan is published on claims. Beginner and Advanced presentation choices affect disclosure only.

The persistent header switches between Configuration and Dashboard without discarding form values. Beginner has a focused summary and next step; Advanced embeds all six existing dashboard views. Language and light/dark preferences propagate to the embedded view. The iframe has an opaque origin (no allow-same-origin); it receives only the read-only snapshot, language and theme, never the parent's session token. Message handlers check the sending window. External links may open from explicit user interaction. Local-plan fallback is labelled, and active/scheduled freezes remain visible in both profiles; active freeze overrides task-start guidance.

Back is available after Welcome, including the final step. Reviewing earlier steps during installation preserves input and disables mutation controls until the operation finishes. Rechecking the same project preserves the selected workflow. Source task names, messages and technical logs remain original content, while interface labels are translated.

The Python standard-library server binds to 127.0.0.1 on an ephemeral port. Its mutation boundary validates Host, Origin, session token, content type, body length and options. It serves only the setup page and named API routes. Installation delegates to install.sh using literal subprocess arguments. Repair delegates to the existing --update path and preserves the configured workflow. Preference writes allow only Blackbox and Pace, reject ambiguous settings, preserve unrelated content and use atomic replacement. The authoritative config reader supplies displayed values. `uak start` remains the readiness gate; mismatched installed/source versions require repair first.

Changed paths across the branch: install.sh; kit/.uak/bin/lib/{setup.py,setup.html,dash.py,dash.html,workspace.js}; kit/.uak/tests/{test_setup_wizard.py,test_unified_workspace.py}.

## Observed verification

- Recorded RED_OK on base 87af168: the initial seven named behavior tests failed on assertions against stubs. Additional red runs reproduced partial-install recovery, ambiguous preferences, older-engine checks, and a missing stack option before their fixes. The current worktree's `.git` red record holds the most recent run, not an archive of all earlier runs.
- `python kit/.uak/tests/test_setup_wizard.py`: 11 PASS, failed=0, including a real failed installation, explicit correction of a colliding user file, and a successful repair.
- `python kit/.uak/tests/test_unified_workspace.py`: 3 PASS, failed=0; authenticated real-plan data, shared language/navigation assets, and isolated embedded dashboard.
- Browser script `../dashboard-review/qa-unified.py`: PASS for Spanish/English, input persistence through Back and view switches, all six original tabs, dark theme propagation, mobile layout, source task text preserved, and hostile content rendered as text. A remote freeze fixture verifies the freeze notice and next action; the notice clears on a later unfrozen snapshot. No JavaScript errors.
- The same browser script exports and opens the standalone dashboard from file://, changes language and theme, and reports OFFLINE_DASHBOARD_RESULT PASS. Its long-running installer fixture reports RUNNING_BACK_RESULT PASS with no duplicate install and no project writes.
- `python kit/.uak/tests/test_v51.py --case dashboard_shows_everything`: PASS, preserving the existing dashboard contract.
- Browser QA: Microsoft Edge through temporary Playwright tooling outside the repository, 1280x720 and 390x844, reduced motion; real install in a disposable Git repo, folder errors, confirmation before writes, settings, reload, and missing-remote readiness blocker. PASS; no JavaScript errors or horizontal overflow. This tooling is not a product runtime dependency.
- Browser script: ../dashboard-review/qa-ui001.py. Screenshots: author worktree/.uak-shots/UI-001/{1280.png,390.png,folder-error-390.png,review-1280.png,installed-1280.png,readiness-390.png}.
- `python scripts/gen_harness.py --check`: exit 0.
- `python scripts/kit_hashes.py --check`: 459 known versions, up to date. Regeneration produced no content change.
- `git diff --cached --check`: exit 0 before the commit.
- `python tests/test_mcp_tools.py`: exit 0, 14 tests run with 2 existing skips.
- Browser regression also confirms that switching from repair of a marathon project to a fresh project re-enables Sprint and restores the Install label in the pushed SHA.

## Validation that is not green

The initial full package smoke stopped in the existing test_claims_perf.py at `the_counter_sees_ps`: expected at least 2 processes, got 1. The exact same function was executed against the unchanged main checkout and reproduced that failure. No existing assertion or expected-failure setting was changed. See ../dashboard-review/UI-001-smoke.log.

The continuation through the smoke runner's supported explicit shard selection stopped at existing Windows symlink tests: WinError 1314 (the user lacks the privilege required to create the fixture symlinks). Its log is ../dashboard-review/UI-001-smoke-remaining.log. This does not turn the failed complete smoke into a pass. The complete suite has not been declared green for this revision.

Native Windows `kit_lint.py` reports 31 existing executable-bit findings for unchanged Bash files. Its initial CRLF findings came from the checkout's core.autocrlf=true; working-tree text was normalized to LF without adding content changes to those files. Windows does not represent Git executable modes as POSIX filesystem modes. See ../dashboard-review/UI-001-lint.log. Linux/macOS CI validation remains needed; do not report the lint as passed.

On Windows use a real Python interpreter: prepend C:/Users/dylan/AppData/Local/Programs/Python/Python313 and C:/Program Files/Git/bin to the review process PATH; set PYTHONUTF8=1. `py` also resolves Python 3.13.7. Do not change global settings or weaken tests.

## Reviewer action now

Pre-review the exact commit and return actionable findings with file/line, severity, reproduction, expected result and a proposed correction. Do not edit the author's worktree or register an approval while the required validation remains incomplete. Coordinate any correction before editing overlapping paths; a corrected SHA needs independent review. A formal `uak done` handoff and PR will follow only after the gates are actually satisfied. Final merging remains Dylan's decision.
