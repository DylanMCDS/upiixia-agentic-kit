# UI-006 contract draft (claude-Dylan, 2026-11-12) · "Start your team" from the page

Status: draft for a Fable mentor pass and the reviewer's agreement BEFORE code (security-sensitive: a human act
from the browser, and commands the person copies into a terminal). Base: main after UI-005 is integrated.

## When the step shows
Only when the last readiness check is READY (uak start) and the kit is on main. Before that, the page keeps the
gate's next step (UI-002/UI-005). Shown in Beginner and in Advanced (Advanced: a box above the dashboard frame with
the same next step and Copy button).

## (a) Register the reviewer: POST /api/team/reviewer {confirm: "NAME-r"}
- The human act. NAME is the human name saved in UI-005 (server-side value, `[a-z][a-z0-9-]{0,31}`), never taken
  from this request; `confirm` must equal "NAME-r" exactly (the page shows it and asks to click "Register NAME-r";
  the request carries the identity the person saw). Plain-words note before the click: "NAME-r reviews your
  agents' work; in Hackathon mode an approved change can merge automatically after the checks pass."
- Runs the engine shipped with setup: `[bash, <package>/bin/uak, register-reviewer, NAME-r]`, cwd = the project's
  main checkout (git dir == common dir; refused from a linked worktree), env: UAK_HUMAN=NAME, UAK_AGENT empty,
  sanitized environment, fixed argv, one operation at a time (worker lock), timeout 120 s.
- Idempotent: an already registered NAME-r answers "already registered" (the engine skips it).
- Keeps every UI-001 protection (loopback, Host, Origin, token, JSON schema, body limit). WHY.md: the second browser
  act of human authority after the plan approval (UI-004) and the kit publication (UI-005), with the evidence.

## (b) Agent launch commands (GET /api/team): copy only, the server never runs them
- Inputs: the next task ID from the READY line (CLAIM_COMMAND regex, `[A-Z][A-Z0-9]*-[0-9]+`), NAME (UI-005),
  the project root (validated by project_root). Nothing else; no free text from the browser.
- Terminal 1 · Claude Code implements:
  `cd 'ROOT' && bash .uak/bin/wt new TASK --agent claude-NAME && cd 'WORKTREE' && claude 'FIRST_IMPL_PROMPT'`
- Terminal 2 · Codex reviews as NAME-r:
  `cd 'ROOT' && UAK_AGENT=NAME-r codex 'FIRST_REVIEW_PROMPT'` (FIRST_REVIEW_PROMPT starts with `$uak-review`)
- ROOT/WORKTREE are single-quoted for Bash with `'` → `'\''`. WORKTREE follows wt's own rule (wt_path, wt:83):
  `<parent of ROOT>/<basename ROOT>-wt/<task lowercase>`; a test pins the two together so they cannot drift.
- FIRST_IMPL_PROMPT uses the kit's `/uak-start` command (.claude/commands/uak-start.md).
- Prompts are constants (like UI-004's PLANNER_PROMPT: no % ^ & | < > " or backticks).
- Each block says which terminal it goes in ("a new terminal window, any folder"), and on Windows "Git Bash".
- (c) One line: "Setup steps (install, publish, plan) need no agent; agents start only here."

## Copy on the tools step
Choosing coding tools explains the roles (one implements, one reviews as a second identity) and recommends
Claude Code + Codex; "I'm the only human on this repository" says in plain words what it changes.

## Tests (task names)
reviewer_is_registered_from_the_page (fixture with a bare remote: the role file appears on claims with
Registered-By: NAME; wrong/missing confirm, a linked worktree, no saved name, not READY → 400 and no record),
agent_launch_commands_are_exact (paths with spaces and a quote are quoted; task ID and name only from server
values; a hostile READY line or name never reaches the command), advanced_view_shows_the_next_step,
tool_roles_are_explained.

## Open questions for the reviewer
1. Is one confirmed click enough for registering a reviewer, or a typed confirmation like UI-004?
2. Implementer identity name: `claude-NAME` (kit convention harness-human) — agree?
3. Windows PowerShell users: show Git Bash only, or also a PowerShell variant?
