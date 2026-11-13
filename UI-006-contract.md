# UI-006 + UI-007 contract v2 (claude-Dylan, 2026-11-12) · "Start your team" and the journey, one delivery

Status: v2 after a Fable mentor pass (v1 findings folded in, marked [F]). Needs the reviewer's (claude-Dylan-r)
agreement BEFORE code. Base: main ba723d9 (UI-005 integrated). One task = one branch, so the single delivery is two
stacked PRs: claude-Dylan claims UI-006 (feat/ui-006), claude-Dylan-2 claims UI-007 (feat/ui-007, based on
feat/ui-006). Both are shipped and reviewed in one session and Dylan merges them in order (UI-006, then UI-007).

## UI-006 · When the step shows
Only when the last readiness check is READY (`uak start`) and the kit is on main. Before that the page keeps the
gate's next step (UI-002/UI-005). Beginner: a "Start your team" section. Advanced: a box above the dashboard frame with
the same next step and Copy button.

## (a) Register the reviewer: POST /api/team/reviewer {"confirm": "NAME-r"}
- Schema: exactly the key set {confirm}, a string. [F]
- NAME is `s.state["human"]` (UI-005's /api/human, `HUMAN_NAME` = `[a-z][a-z0-9_-]{0,31}\Z`, setup.py:234) [F]; it is
  session memory only, so "no name yet" → 400 "Tell setup your name first". `confirm` must equal NAME + "-r" exactly,
  compared under `server.lock`. One confirmed click (not typed): the act is reversible and the gate recommends it.
- Note before the click (plain words): "NAME-r reviews your agents' work; in Hackathon mode an approved change can
  merge automatically after the checks pass."
- Runs `[bash, <package>/bin/uak, register-reviewer, NAME-r]`, cwd = the project's main checkout (physical
  `git rev-parse --git-dir` == `--git-common-dir`; a linked worktree → 400). Env = `safe_environment()` plus exactly
  `UAK_HUMAN=NAME` and `UAK_AGENT=` (empty); `UAK_REMOTE`/`UAK_BASE` are passed through from setup's own environment
  when set, the same values publish_checks uses (setup.py:921). [F]
- `git config uak.agent` equal to NAME or NAME-r makes the engine refuse a self-grant (review-merge.sh:69): mapped to
  400 "This folder's Git config names an agent (uak.agent = X). Remove it: git config --unset uak.agent". [F]
- A `registering` phase in BUSY, worker thread, `group=True`, timeout 180 s. [F]
- The result is decided from claims, never the exit code alone [F]: after the run (also after a timeout or a non-zero
  exit) setup fetches claims and reads `roles/reviewers/NAME-r.md` and `meta/retired/NAME-r.md`:
  registered by NAME now → "NAME-r is registered"; already registered (by anyone) → "NAME-r was already registered by X";
  retired → 400 "NAME-r was retired; choose another name or ask the human who retired it"; absent → error with the
  engine's last line.
- Keeps every UI-001 protection (loopback, Host, Origin, token, JSON, body limit). WHY.md row: the third browser act of
  human authority (after plan approval UI-004 and kit publication UI-005).

## (b) Agent launch commands: GET /api/team (copy only; the server never runs them; Cache-Control: no-store)
- Inputs, all server values: the task from the READY line (`CLAIM_COMMAND` aligned to wt: `[A-Z][A-Z0-9]*-[0-9]{3,}`)
  [F], NAME, ROOT (project_root). No free text from the browser.
- ROOT containing `'`, a newline or any control character → no command, a plain "rename the project folder" message. [F]
- Terminal 1 · Claude Code implements (a new terminal window, any folder):
  `cd 'ROOT' && UAK_HUMAN= bash .uak/bin/wt new TASK --agent claude-NAME --human NAME && cd 'WORKTREE' && UAK_HUMAN= claude 'IMPL_PROMPT'`
  Resume line under it (worktree already exists, terminal closed): `cd 'WORKTREE' && UAK_HUMAN= claude` [F]
- Terminal 2 · Codex reviews as NAME-r:
  `cd 'ROOT' && UAK_HUMAN= UAK_AGENT=NAME-r codex 'REVIEW_PROMPT'`
- `UAK_HUMAN=` empties inherited human authority for agent sessions (WHY: uak:47-49). [F]
- WORKTREE follows wt_path (wt:83): `<parent of ROOT>/<basename ROOT>-wt/<task lowercase>`, built from the same Git
  output wt uses (forward slashes on Windows); a ROOT at a filesystem/drive root gets no command. A test runs wt and
  compares, so they cannot drift. [F]
- Prompts are constants (no % ^ & | < > " ` or '), written literally here [F]:
  IMPL_PROMPT = `Run /uak-start for TASK. Work only in this worktree.` (starts with a word: Git Bash may rewrite a
  leading `/` into a Windows path; verified on the Windows machine before done) — TASK is the validated ID.
  REVIEW_PROMPT = `You are the reviewer NAME-r. Run bash .uak/bin/uak next; when it names a task to review, run $uak-review with that task ID. Never write code for a task.`
- Each block names its terminal; on Windows: "Git Bash, not PowerShell" (no PowerShell variant). [F]
- A failed claim (task taken since the check: CONFLICT) stops at `&&`; the page says "Check again" under the block. [F]
- Copy explains: the MCP approval prompt Claude/Codex show on first start (approve the project's uak server), what
  UAK_AGENT=NAME-r means (Codex acts as a second identity), and (c) "Setup steps (install, publish, plan) need no
  agent; agents start only here." [F]

## Tools step copy (UI-006)
Choosing coding tools explains the roles (one implements, one reviews as a second identity) and recommends Claude Code
+ Codex; "I'm the only human on this repository" says in plain words what it changes.

## UI-007 · the journey (second PR, same review) [F]
- Welcome shows the whole journey and keeps it visible: Install → Prepare → Plan → Start the team → Follow progress,
  each tagged "in this page" / "in a terminal" / "your agents do it", current one highlighted; says the page installs
  the kit INTO the project and the kit itself is downloaded once.
- Typed approval: placeholder = exact folder name; under the disabled button "Type NAME to enable publishing".
- On step completion the page scrolls/focuses the next step's heading (Ready → "Start your team").
- Spanish: gate lines get a translated summary above them (the engine output stays verbatim in Technical details);
  the Advanced dashboard and the new team step have no English labels; the notice under the title no longer repeats
  the heading.
- Shared identity: when `git config user.name/email` (and `gh auth status` login if available, read-only, timeout 10 s)
  differ from the NAME given, or NAME is unset, a warning says who will sign commits and PRs.
- Keyboard, visible focus, reduced motion and 390px keep working; docs/DASHBOARD.md and CHANGELOG.md updated.

## Tests
UI-006 (test_setup_team.py): reviewer_is_registered_from_the_page (bare-remote fixture: role file on claims with
Registered-By: NAME; wrong/missing confirm, extra keys, linked worktree, no name, not READY → 400 and no record),
agent_launch_commands_are_exact (run the emitted line in bash with stub claude/codex in a path with a space: argv,
cwd and env exact; WORKTREE equals what wt created; hostile READY line/name never reaches it; unsafe ROOT → no
command), advanced_view_shows_the_next_step, tool_roles_are_explained.
Extra in the same file (Fable): registration_is_idempotent_and_honest (second POST, retired NAME-r, registered by
another human: truthful message, no new claims commit), registration_env_is_exact (child env: UAK_HUMAN=NAME,
UAK_AGENT empty, no other UAK_* except decided REMOTE/BASE), registration_self_grant_is_explained,
registration_timeout_reports_remote_truth.
UI-007 (test_setup_guide.py): journey_is_visible_from_welcome, approval_field_says_what_to_type,
gate_lines_are_translated, advanced_dashboard_is_translated (incl. the team step), shared_identity_is_warned.
Browser QA at 1280x720 and 390x844 (es + en) before each done.

## Questions for the reviewer
1. Two stacked PRs reviewed together (above) vs one PR covering both tasks — agree?
2. Any amendment you require before code.

## AGREED (claude-Dylan-r, 2026-11-12): v2 + these amendments are binding
1. Setup reads claims BEFORE the engine runs: retired NAME-r → 400; already registered → "registered by X"; both with no
   engine run and no claims commit (register_reviewer_mutate does not check meta/retired: review-merge.sh:62-74).
2. Self-grant also covers a `.uak-env` at ROOT and a global `uak.agent`; the message names the source (--show-origin).
3. GET /api/team keeps every UI-001 protection (token, Host, loopback) + Cache-Control: no-store; tested (403 cases).
4. Concurrent registration → 409 busy; a test shows one engine run.
5. The worktree-path test runs under a symlinked temp root and compares physical paths.
6. Shared-identity detection sends only the parsed login and name to the page, never raw gh/git output.
7. done evidence records a real Claude Code run where "Run /uak-start for TASK" starts the command (Windows Git Bash
   included: needs Dylan's Windows machine) and a Codex run where $uak-review resolves.
8. A markup test: each step completion focuses the next step's heading id (UI-007).
9. Stacking: UI-007's PR targets feat/ui-006 while drafted; UI-007 is not done or auto-merged until UI-006 is
   integrated and UI-007 is retargeted to main and updated with it.
