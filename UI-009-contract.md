# UI-009 contract v1 (Fable mentor pass, 2026-11-13) · the team step, right for every person

Status: v1, written before code. Needs the reviewer's agreement (claude-Dylan-r) and three decisions from Dylan
(section "Decisions needed") BEFORE the red. Base: main 399c255. Spec: the last `## UI-009` section of
`claims:backlog/AMEND.md` (absorbs UI-011 and UI-014; 10 named tests, 3 test files).
Line numbers below are from main 399c255.

## Scope

1. Reviewer state is read from claims per project and per name; `state["reviewer"]` (server-wide) is removed.
2. No network Git, engine run or tool probe ever runs under `server.lock`; `/api/status` answers in under 1 s.
3. Offline is told apart from "main has no kit"; unrelated remote history gets one exact safe command or a new empty
   repository.
4. Each person picks which available tool implements and which reviews (the same tool may do both).
5. After the first claim the team step stays: one offer for a new implementer, a resume line per own claimed task, the
   reviewer command.

Files (task Paths only): `setup.py`, `setup.html`, `workspace.js`, `test_setup_team.py`, `test_setup_prepare.py`,
`test_setup_roles.py` (new), `kit/.uak/docs/WHY.md`, `docs/DASHBOARD.md`.
`planning.py` is NOT in Paths: it is only called (`available_planners`, `SUPPORTED`, `git`, `write_atomic`,
`regular_file`); `planning.kit_on_main` is no longer called by setup.py and stays untouched.

## Decisions needed (Dylan), before the red

D1. Existing assertions must change, so `done` needs
    `UAK_HUMAN=Dylan bash .uak/bin/uak allow UI-009 --tests --reason "the Codex reviewer command gains --sandbox/--add-dir (acceptance of UI-009); agent_launch_commands_are_exact pinned the old line"`.
    Exactly two assertions in `agent_launch_commands_are_exact` (test_setup_team.py:206 and :234-235): the review
    command string and the Codex stub's argv. Nothing else existing is edited; helpers only gain lines (see Tests).
D2. One implementer tool and one reviewer tool per person (the same tool allowed). Two implementers on one computer is
    out of scope (they can still run `wt new` by hand; their claims show in the claimed list). The acceptance's
    "implements, reviews, or both" per tool is the derived view of those two picks.
D3. `kit/.uak/settings/known-files.txt` (kit_hashes.py) and `CHANGELOG.md` are outside Paths but AGENTS.md requires
    the first after any kit file change. Confirm they may be touched (as in earlier UI tasks) or amend Paths.

## State & concurrency

### Locks (setup.py, SetupServer)
- `lock` (exists): guards `state`, `plan`, `worker`, `target`, `failed_target` and the new caches. Rule: no
  `server.run`, no subprocess that can reach the network, the engine or a coding tool, while holding it. Existing
  local-only uses stay (`publish_run`/`approve_run` digest + `git add`); new code adds none. In `/api/status` copy the
  state under `lock`, then compute `config()` and `guidance()` outside it.
- `slow` (new, `threading.Lock`): the slow lane. Held by every POST for its whole dispatch and by the GETs that may
  probe or fetch (`/api/team`, `/api/plan`, `/api/publish-kit`). Never taken by `/api/status`, `/api/dashboard`, `/`,
  `/workspace.js`. Lock order: `slow` then `lock`; never acquire `slow` while holding `lock`.
- No `pending` flag and no new BUSY phase: a request-side check changes no state. While it runs `/api/status` returns
  the last committed state unchanged.

### do_POST (replaces setup.py:806-810)
```
read body; self.identity = self.read_identity(data)        # as today, before any lock
with lock:  busy = worker alive                            # fast 409, as today
if busy: 409
with slow:
    with lock: busy = worker alive                         # re-check after waiting
    if busy: 409
    self.dispatch(data)                                    # NOT under lock
```
`dispatch` and its helpers take `lock` only around reads/writes of server fields and around starting a worker
(`*_run`/`launch` set the BUSY phase and assign `self.worker` inside one `with lock`). POSTs stay serialized exactly as
today (a second POST waits, then validates fresh state); only the mutex changes.

### Workers
- A worker's `work()` starts with `with self.slow: pass` (a drain): every request-side network section that began
  before the worker was started has finished before the engine runs. After that the worker holds neither lock except
  short `with lock` state updates (as today).
- While a worker is alive: POST → 409 (today); GET `/api/dashboard` → 409 (today); GET `/api/publish-kit` → 409;
  GET `/api/team` → the cached view for the current key when there is one (`"stale": true`), else 409;
  GET `/api/plan` → no probe and no fetch: last known `planners` and `kit_on_main` (defaults `[]`/`False`).
  So setup never fetches while the engine reads its own FETCH_HEAD.
- No background thread, timer or refresher. Every network process belongs to a request thread or to the one worker
  (Windows: a process left inside the project folder was WinError 32, setup.py:802-804).

### Network Git
- `NET_TIMEOUT = 30` s per command for request-side `ls-remote`/`fetch`, run through `server.run(..., group=True)` so
  a timeout stops the whole tree (git-remote-https; `taskkill /T` on Windows). Worker pushes keep 120 s.
- Setup never reads `FETCH_HEAD` after its own fetch. All setup fetches use explicit refspecs into private refs:
  `+refs/heads/BASE:refs/uak/setup-base`, `+refs/heads/claims:refs/uak/setup-claims`. `publish_checks`,
  `approval_checks` and `reviewer_on_claims` switch from `FETCH_HEAD` to these refs.
- `REMOTE`/`BASE` = `UAK_REMOTE`/`UAK_BASE` or `origin`/`main`, one helper used everywhere (also plan_view and
  POST /api/plan: PENDING #41). Both must match `[A-Za-z0-9][A-Za-z0-9._/-]{0,99}\Z`, else a plain 400.

### remote_state(server, root, fresh=False) → dict (the only reader of the remote for team/plan views)
1. `git remote get-url REMOTE` fails → `{"state": "none"}` (no network).
2. `git ls-remote --heads REMOTE refs/heads/BASE refs/heads/claims`; non-zero or timeout →
   `{"state": "offline", "detail": redact(stderr)[-300:]}`.
3. BASE listed: fetch into `refs/uak/setup-base` unless that ref already equals the listed SHA; fetch failure →
   offline. `kit` = `cat-file -e refs/uak/setup-base:.uak/PROJECT.md`. BASE not listed → `kit: False`.
4. claims listed: fetch into `refs/uak/setup-claims` (same skip). Then two local commands:
   `git grep --no-color -E '^(Reviewer|Registered-By|ID|State|Owner): ' refs/uak/setup-claims -- roles/reviewers claims`
   (exit 1 = no match) and `git ls-tree --name-only refs/uak/setup-claims meta/retired/`.
   Only files named `[A-Za-z0-9_.-]+\.md` are parsed; everything read is data.
5. Result: `{"state": "ok", "kit": bool, "reviewers": {name: registered_by}, "retired": [names],
   "claims": {ID: {"state", "owner"}}, "at": monotonic}`. A reviewer counts only when `Reviewer` equals the file stem
   and `Registered-By` is non-empty (review-merge.sh:16-18).

Cache: `server.remote_cache[(str(root), REMOTE, BASE)]`, only `state == "ok"` results, TTL 15 s. Failures are never
cached (Retry really retries). Cleared for the key by: `apply_readiness` (every finished check, publish, approval),
the end of `register_run`, `/api/inspect`. `fresh=True` skips the cache: used by POST /api/team/reviewer (before the
engine) and by `register_run`'s read-back. Decisions are never taken from the cache.

### Reviewer state
- `registered(server, root, who)` = from `remote_state`: `who in reviewers and who not in retired`.
- `server.state` has no `reviewer` key. `/api/status` adds `"reviewer"` computed for `(target, human + "-r")` from
  the cache entry of that project (or `{}`); `register_run` writes its result into the cache, plus a per-key
  `last_error`. So `state.reviewer.registered` in existing tests still reads true after a registration, and another
  project, another name or a retire never inherits it.
- Network failure: `registered: null` (unknown), never a remembered `true`; the page shows the offline note and Retry,
  no Register button.
- Tool detection cache: `server.tools_cache[str(root)]` = `available_planners` rows filtered to `planning.SUPPORTED`,
  TTL 60 s, cleared by `/api/inspect` and `/api/check`. Probes run under `slow`, outside `lock`.

### Team phase (after the first claim)
`team_phase(state)` → `"ready"` when `state["ready"]`; `"waiting"` when the last check is not ready and its only TODO
is the engine's `a claimable task: uak next offers none` line (start:172); else `""`. Derived from `checks`, not stored
(every reset of `checks` resets it). `/api/status` adds `"team": team_phase(state)`.
- `team_context` accepts `"ready"` or `"waiting"` (its refusal text for `""` is unchanged).
- `guidance()`: phase `"waiting"` → `{"kind": "waiting", "title": "Your team is working", "detail": "No task is free
  to start right now.", "steps": [the engine's reason lines], "commands": []}`: no terminal box, no "todo".

### Roles (per person, per project, not shared)
- Stored in `<git-common-dir>/uak-setup/roles.json`, written with `planning.write_atomic`. Why there: it survives a
  restart (the server's state does not), it is per clone, it can never be committed, staged, published or seen by a
  teammate, it needs no `.gitignore`, installer or known-files change, and a task worktree shares it. Precedent: the
  engine keeps `uak-red/` in the Git directory.
- Shape: `{"version": 1, "people": {"ana": {"implement": "claude", "review": "codex"}}}`, keyed by the human name so
  a second person on the same clone starts from the defaults.
- Read: at most 16 KB, a dict, names matching `HUMAN_NAME`, values in `planning.SUPPORTED`; anything else is ignored.
  The folder or file being a symlink → ignored on read, 400 on write.
- Effective roles: the saved pick when both its tools are available now; otherwise the default and
  `roles.note = "Your saved choice used a tool that is not available now, so setup chose again."`.
  Default: both available → `claude` implements, `codex` reviews (today's behaviour); one available → it does both;
  none → no roles, no commands.

## API changes

### GET /api/team (same protections; `Cache-Control: no-store`)
400 when there is no name or `team_phase` is `""` (as today). Otherwise 200:
```json
{"human": "ana", "reviewer": "ana-r", "phase": "ready", "stale": false,
 "remote": {"state": "ok", "detail": ""},
 "registered": {"name": "ana-r", "registered": true, "registered_by": "ana", "retired": false, "message": ""},
 "tools": [{"id": "claude", "label": "Claude Code", "available": true, "reason": "", "role": "implement"},
           {"id": "codex", "label": "Codex", "available": false, "reason": "Sign in to it in a terminal first.", "role": "none"}],
 "roles": {"implement": "claude", "review": "codex", "saved": false, "same_tool": false, "note": ""},
 "task": "APP-003",
 "commands": [{"id": "implement", "harness": "claude", "tool": "Claude Code", "identity": "claude-ana-2", "task": "APP-003",
               "terminal": "Terminal 1: a new terminal window, any folder", "command": "…", "resume": "…"},
              {"id": "review", "harness": "codex", "tool": "Codex", "identity": "ana-r",
               "terminal": "Terminal 2: another new terminal window, any folder", "command": "…"}],
 "claimed": [{"task": "APP-001", "state": "CLAIMED", "owner": "claude-ana", "mine": true, "here": true,
              "tool": "Claude Code", "resume": "cd '…-wt/app-001' && UAK_HUMAN= claude"}],
 "note": "", "retry": false, "can_check": false}
```
- Existing keys keep their meaning (`task`, `human`, `reviewer`, `commands[].id/tool/terminal/command/resume`, `note`,
  `registered`); `commands` holds at most one `implement` and one `review`.
- `role` per tool: `implement`, `review`, `both`, `none` (derived from `roles`). `reason` is exactly
  `available_planners`' text. Cursor and Gemini rows are not listed.
- `remote.state`: `ok`, `offline`, `none`. Order of the gates, first match sets `note` and stops the commands:
  1. unsafe folder → the existing "Rename the project folder…" note (now also checked on the common Git dir);
  2. linked worktree → existing note;
  3. `offline` → `"Setup cannot reach REMOTE right now (DETAIL). Check your connection, then press Retry."`,
     `retry: true`, `registered.registered: null`, `commands: []`, `claimed: []`. Never "publish";
  4. `none` → `"This project has no remote named REMOTE. Add one, then press Retry."`, `retry: true`;
  5. `kit` false → the existing "Publish the kit to main first…" note (reachable remote only);
  6. no tool available → `"No coding tool can start here: Claude Code: REASON. Codex: REASON. With Cursor or Gemini,
     claim the task with the command below and open the tool in its folder yourself."`, `commands: []` (the guide keeps
     the bare `wt new` command, as today when the team step has no commands).
- `registered`: `retired: true` → `message = "ana-r was retired, so it cannot review. Choose another name in Your
  name, or ask the human who retired it."`, no review command. Otherwise the page words it from
  `registered_by` (equal to `human` → "is registered"; else "was already registered by X").
- `claimed`: one row per file under claims `claims/` whose state is CLAIMED, BLOCKED or REVIEW and whose ID matches
  `TEAM_TASK`. `mine` = owner matches `^(claude|codex)-NAME(-[1-9])?\Z` with the server's NAME; `here` = the
  directory `<ROOT>-wt/<id lowercase>` exists. `resume` only when `mine and here` and that tool is available now.
  Other rows are text only (ID, state, owner).
- Offer (`task` + the `implement` command): the task of the last READY line, when `TEAM_TASK` accepts it, claims has
  no CLAIMED/BLOCKED/REVIEW record for it and its worktree folder does not exist. Otherwise `task: ""`, no
  `implement` command, `can_check: true` and
  `note = "APP-001 was claimed since the last check. Press Check what's next to find a free task."`
  (phase `waiting`: `note = "No task is free to start right now."`, the reasons come from the guidance).
- Implementer identity: the first of `TOOL-NAME`, `TOOL-NAME-2` … `TOOL-NAME-9` that owns no CLAIMED/BLOCKED claim
  and is not retired (one identity = one live task, claim.sh:27-34). None free → no command, a note.

### POST /api/team/roles `{"implement": "claude"|"codex", "review": "claude"|"codex"}`
Exactly that key set, strings. Needs the name and a team phase (`team_context`), the main checkout, and both tools
available now (`"That coding tool is not available here: REASON"` → 400, file untouched). Writes the file, replies
200 `{"roles": {...}}` (same object as GET). All UI-001 protections; 409 while a worker runs.

### POST /api/team/reviewer (unchanged contract)
Same checks, messages and codes. Reads claims with `remote_state(fresh=True)` under `slow`, not under `lock`; writes
the cache instead of `state["reviewer"]`. Offline → the existing 400 "Could not reach …".

### GET and POST /api/publish-kit · unrelated history
`publish_checks` fetches BASE into `refs/uak/setup-base`. When the remote BASE has commits and there is no common
ancestor (local HEAD unborn, or `git merge-base HEAD refs/uak/setup-base` prints nothing), it raises a `ValueError`
subclass carrying `way_out`; the reply is 400:
```json
{"error": "origin/main already has its own first commits (for example a README or .gitignore created on GitHub), and they do not share history with this folder. Nothing was changed.",
 "way_out": {"command": "cd '/path/to/project' && git pull --no-rebase --no-edit --allow-unrelated-histories origin main",
             "renamed": [],
             "steps": ["If Git reports a conflict, open the files it names, keep what you need from both, then run git add on them and git commit.",
                       "Or publish to a new empty repository (no README, no .gitignore, no license): git remote set-url origin <its URL>"]}}
```
- Unborn local branch and remote files that already exist here (the round 4 dead end: GitHub's `.gitignore` against
  the installer's): the command renames this folder's copies first, never overwriting:
  `cd 'ROOT' && mv -n -- '.gitignore' '.gitignore.mine' && git pull --no-rebase --no-edit --allow-unrelated-histories origin main`
  (`renamed: [".gitignore"]`; a step adds: "Your copies were kept as NAME.mine. Choose Repair or update kit so the kit
  adds its lines to .gitignore again, then compare and delete the .mine files."). Colliding paths come from
  `git ls-tree -r --name-only -z refs/uak/setup-base` ∩ paths that exist here; they are remote data, so a command is
  built only when there are at most 8, each matches `[A-Za-z0-9._][A-Za-z0-9._/-]{0,199}\Z` with no `..` part, and
  `NAME.mine` does not exist. Otherwise `command: ""` and only the new-repository step is offered.
- A local branch that is simply behind (HEAD is an ancestor of the remote) keeps today's "git pull" message
  (test_setup_prepare.py:187 stays green). Ahead/diverged with a common ancestor keeps today's message.
- The steps are text (the second holds a placeholder, as publish_checks' "git remote add … <its URL>" does); only
  `command` gets a Copy button. Setup never runs any of it.

### GET /api/status
Adds `"team"` and the derived `"reviewer"`. No other change; never waits on `slow`.

## Command templates

Variables, all server values: `ROOT` = `project_root().as_posix()`; `GITDIR` = the common Git dir,
`Path(...).resolve().as_posix()` (what `wt` prints for Codex, wt:325-327; `C:/…` on Windows); `WT` =
`<parent of ROOT>/<basename ROOT>-wt/<task lowercase>`; `TASK` (TEAM_TASK); `NAME` (HUMAN_NAME); `IMPL` = the chosen
implementer identity. `ROOT`, `GITDIR` and `WT` go through `shell_quote`; if any holds `'` or a control character, or
ROOT is a drive root, there is no command (existing note). Everything else is a constant.

Prompts (constants; no `% ^ & | < > " ' \`` or newline; each starts with a word, never `/`):
- `IMPL_PROMPT` (exists) = `Run /uak-start for TASK. Work only in this worktree.`
- `IMPL_PROMPT_CODEX` = `Run $uak-start for TASK. Work only in this worktree.`
- `REVIEW_PROMPT` (exists, Codex) = `You are the reviewer NAME-r. Run bash .uak/bin/uak next; when it names a task to review, run $uak-review with that task ID. Never write code for a task.`
- `REVIEW_PROMPT_CLAUDE` = the same sentence with `/uak-review`.

| Role · tool | Command |
|---|---|
| implement · Claude Code | `cd 'ROOT' && UAK_HUMAN= bash .uak/bin/wt new TASK --agent IMPL --human NAME && cd 'WT' && UAK_HUMAN= claude 'IMPL_PROMPT'` |
| resume · Claude Code | `cd 'WT' && UAK_HUMAN= claude` |
| implement · Codex | `cd 'ROOT' && UAK_HUMAN= bash .uak/bin/wt new TASK --agent IMPL --human NAME && cd 'WT' && UAK_HUMAN= codex --sandbox workspace-write --add-dir 'GITDIR' 'IMPL_PROMPT_CODEX'` |
| resume · Codex | `cd 'WT' && UAK_HUMAN= codex --sandbox workspace-write --add-dir 'GITDIR'` |
| review · Claude Code | `cd 'ROOT' && UAK_HUMAN= UAK_AGENT=NAME-r claude 'REVIEW_PROMPT_CLAUDE'` |
| review · Codex | `cd 'ROOT' && UAK_HUMAN= UAK_AGENT=NAME-r codex --sandbox workspace-write --add-dir 'GITDIR' 'REVIEW_PROMPT'` |

- With today's defaults and a free `claude-NAME`, the Claude lines are byte-identical to UI-006's.
- `--sandbox workspace-write` goes with `--add-dir` because Codex ignores `--add-dir` in a read-only sandbox (an
  untrusted folder starts read-only; rounds 1 and 3 failed with "Operation not permitted"). No approval or bypass
  flag is ever added (the `BYPASS` list of test_setup_planning stays absent from every command).
  This flag pair is from the mentor's knowledge of the Codex CLI, not from a run: see Risks R1.
- One tool, both roles: two terminals of the same tool, two identities (`TOOL-NAME` in the task worktree, `NAME-r` in
  the main checkout).
- Windows: unchanged rule, "paste in Git Bash, not PowerShell". Paths are forward-slash native paths, valid for `cd`
  in Git Bash and for `codex.exe --add-dir`; no argument starts with `/`.

## UI changes (setup.html, workspace.js)

- `#team-step` shows when `state.ready || state.team` (not only `ready`). `journeyStep`: `data.ready || data.team`
  → `team`/`progress` (never back to `prepare`). `loadTeam` reruns when target, name, `ready`, `team` change and after
  every busy → idle transition. A failed GET keeps what is drawn and shows the error in `#team-note`; only a 400 hides
  the step.
- New block `#team-roles` between the reviewer block and the commands: two radio groups, "Who implements?" and "Who
  reviews?", one option per available tool; unavailable tools listed below with their reason, not selectable. A change
  POSTs `/api/team/roles` and redraws. When both picks are the same tool: "TOOL does both jobs under two names:
  IMPL writes the code and NAME-r reviews it in a separate session. The reviewer never reviews its own identity's
  work."
- Headings become formatted strings: `2. {tool} implements`, `3. {tool} reviews`. Existing ids stay
  (`team-implement`, `team-review`, `team-implement-command`, `team-implement-resume`, `team-review-command`, the Copy
  ids). Tool-specific hints are separate static paragraphs with `data-tool="claude"`/`"codex"`, toggled by script
  (the Claude trust hint stays inside `#team-implement`: test_setup_trust.py:91).
- New `#team-claimed` list: per row `ID · state · owner` (textContent) and, when `resume` is present, the line with
  its own Copy button labelled with the task (`aria-label` "Copy the command for APP-001").
- `#team-note` gains two buttons: `#team-retry` (`retry`: re-GET /api/team) and `#team-check` (`can_check`: the
  existing POST /api/check).
- Reviewer block: `registered === null` → no Register button and no status claim; `retired` → the message, no button.
- Publish step: when a 400 carries `way_out`, a box `#publish-way-out` shows the error, the command in
  `<code data-no-i18n>` with Copy, and the steps as text.
- Tools step copy keeps the four pinned phrases (`tool_roles_are_explained`) and adds: "With only one tool, it does
  both jobs under two names." `teamGuide`'s sentence names the chosen tool: "…claims this task for {tool}."
- Guidance kind `waiting` shows `#next-check` ("Check again").
- Every new English string (static, formatted, server notes, the three `available_planners` reasons, the `way_out`
  error and steps) has a Spanish entry in workspace.js; server notes with values use the catalog's pattern rows.

## Security

- All new routes keep the UI-001 protections (loopback, Host, Origin on writes, token, JSON, body limit, no-store).
- Commands are built only from: the validated READY task, `HUMAN_NAME`, enum tools, constant prompts, paths from Git
  on this computer. Nothing from the browser except the two enum picks. Nothing from claims except a task ID that
  matches `TEAM_TASK` and an owner that must equal an identity the server itself builds from NAME.
- Claims content, remote file names and remote error text are data: shown with `textContent`, redacted, length-capped.
- No destructive command is ever emitted. A test greps every emitted line for `--force`, ` -f`, `reset`, `clean`,
  `rm `, `checkout --`, `branch -D`, `+refs`, `push`. `mv -n` never overwrites.
- The roles file holds only a name and two enums, lives in the Git directory, is never read through a symlink.
- `UAK_HUMAN=` still empties human authority in every agent line; the reviewer identity is only ever `NAME-r`.

## Tests

Shared helper changes (additions only, no assertion touched): `Team.__call__` answers the auth probes
(`[bin, "auth", "status"]`, `[bin, "login", "status"]`) from `self.tools` (default both signed in: exit 0), and
`Team.ready_code` (default 0) is the exit code of the canned `uak start`. Without the first, `/fake/bin/claude` cannot
run and every existing team test would see no tool. Stub `claude`/`codex` scripts come from `stub_tools`.

### test_setup_team.py
1. `reviewer_state_follows_project_and_name` · Fixture: two `ready_project`s (A, B), each with its own bare remote,
   ONE server. Steps and assertions: register `ana-r` on A → `/api/team` and `/api/status` say registered. Inspect B
   as `ana`, check → `registered.registered is False` and status `reviewer` is not registered, Register is offered
   **(fails today: the server-wide flag says registered)**. Back on A → registered, with no engine run. `/api/human`
   = `bob` on A → `reviewer == "bob-r"`, not registered. Retire `ana-r` with the real engine, name `ana`, POST
   `/api/check` → `registered.retired is True`, `registered is False`, no review command. `"reviewer" not in
   srv.state`.
2. `codex_command_can_write_git` · Fixture: `ready_project` named `team space é` under a symlinked root; both tools.
   The review command equals the Codex review template with `GITDIR` = physical `<ROOT>/.git` **(fails today: no
   `--add-dir`)**. Run it in bash with the stubs: Codex's argv is exactly
   `["--sandbox", "workspace-write", "--add-dir", GITDIR, REVIEW_PROMPT]`, `GITDIR` is one argument and an existing
   directory, `UAK_AGENT=[ana-r]`, `UAK_HUMAN=[]`. With roles `codex` implements: after the line runs, the stub ran in
   the worktree and its `--add-dir` value is the main checkout's `.git` (not the worktree's `.git` file).
3. `team_step_survives_the_first_claim` · Fixture: `ready_project`; run the emitted implement line (real `wt new`,
   real claim by `claude-ana`). (a) POST `/api/check` with the same canned READY line (the stale offer of round 3) →
   `/api/team`: `task == ""`, no `implement` command, `can_check`, `claimed` has APP-001 / CLAIMED / `claude-ana` with
   `resume == "cd 'WT' && UAK_HUMAN= claude"`, the review command is still there **(fails today: `wt new APP-001` is
   offered again)**. (b) `team.ready` = the engine's real waiting output (`TODO  7. a claimable task: uak next offers
   none` + a `· Waiting on` line; the literal is also asserted to exist in `bin/start`), `ready_code = 1` → status
   `ready is False`, `team == "waiting"`, `guidance.kind == "waiting"` without `terminal`; `/api/team` is 200 with
   the resume line and the review command **(fails today: 400)**. (c) a READY line naming APP-003 → the implement
   command uses `--agent claude-ana-2`. (d) page source: `journeyStep` and `loadTeam` read `team`.
4. `offline_team_step_says_offline` · Fixture: `ready_project`, then `git remote set-url origin <tmp>/gone.git`.
   `/api/team` → 200, `remote.state == "offline"`, `retry is True`, no commands, `registered.registered is None`, the
   note contains "cannot reach" and not "publish" **(fails today: "Publish the kit to main first")**. URL restored →
   the next GET has commands (a failure is not cached). The empty-bare-remote case of
   `team_step_needs_main_checkout_and_kit_on_main` still says "publish the kit". Spanish entry exists.

### test_setup_prepare.py
5. `status_answers_during_network_git` · Fixture: `installed()`; runner = `FakePlanner` subclass that, on a command
   containing `ls-remote`, sets `entered` and waits on `gate` (at most 6 s) before running it. A thread sends
   GET `/api/publish-kit`; after `entered`, the test times GET `/api/status`: 200 in under 1.0 s **(fails today on
   that assertion, about 6 s, not a hang: the client timeout is 10 s)**, phase unchanged and not in `BUSY`. Then the
   gate opens, the thread is joined and its reply is 200. Second half with `Team` on a `ready_project`: the block is
   inside POST `/api/team/reviewer`; status again under 1 s; a POST `/api/human` sent meanwhile returns only after the
   gate opens. Every network call the runner saw has `timeout <= 30`.
6. `unrelated_remote_history_has_a_way_out` · (a) the incident: `installed()` (unborn), local `.gitignore` = `mine`,
   a clone pushes a root commit with `.gitignore` and `README.md` to origin. GET and POST `/api/publish-kit` → 400
   with `way_out` **(fails today: no `way_out`, and the advice "git pull" stops on the untracked .gitignore)**;
   `command` is exactly the `mv -n … && git pull …` line; run in bash → exit 0, `.gitignore.mine` holds `mine`,
   `.gitignore` is the remote's, HEAD is the remote commit; then the preview is 200 and `publish()` puts the kit on
   top of that commit. (b) local commits with no common ancestor: `command` is the plain pull line; run → exit 0,
   `git rev-list --max-parents=0 HEAD` has two roots. (c) a colliding remote file named `a'b` → `command == ""`, the
   new-repository step is present. (d) no emitted command contains a destructive word (list in Security). (e) the
   behind case of line 187 still says "git pull" and has no `way_out`.

### test_setup_roles.py (new; imports test_setup_team helpers; its own `roles_project(root, tmp, harnesses)`)
7. `roles_follow_the_tools_you_have` · both tools: `tools` and `roles` show the default (claude implements, codex
   reviews) **(fails today: no `tools` key)**; POST roles `codex`/`claude` → 200 **(today 404)**; the commands follow
   (`--agent codex-ana`, `$uak-start`; `UAK_AGENT=ana-r claude`, `/uak-review`). A NEW server on the same folder
   returns the same roles. `git status --porcelain` is unchanged and a fresh clone has the defaults (not shared).
   Name `bob` → defaults; back to `ana` → her pick. Bad bodies (extra key, unknown tool, list, missing key) → 400,
   file bytes unchanged.
8. `one_tool_does_both_roles` · only `.claude` installed: `roles == {implement: claude, review: claude}`,
   `same_tool is True`; both lines run with the stubs: implement as `claude-ana` (the worktree's `.uak-env`), review
   with `UAK_AGENT=[ana-r]` and the `/uak-review` prompt. Mirror with only Codex signed in. The page has the "never
   reviews its own identity's work" sentence, with Spanish.
9. `any_tool_can_review` · for the four picks (claude/codex, codex/claude, claude/claude, codex/codex): the two
   commands equal the templates byte for byte; each review line runs with the stubs and the argv is exact.
10. `unavailable_tool_is_not_offered` · Codex (a) not installed in the project, (b) not on this computer
    (`find_binary` → None), (c) signed out (probe exit 1): its row has `available False` and the matching reason, no
    command contains `codex`, POST roles naming it → 400, a saved pick naming it falls back with `roles.note`. (d) a
    `.cursor`-only project: `commands == []`, the note names both reasons. Each reason has a Spanish entry.

Also before `done` (not named tests): the whole existing team, prepare, guide, trust, planning and wizard files green;
browser QA at 1280x720 and 390x844, es + en, of the roles block, the claimed list, offline + Retry and the way-out box.

## Out of scope

- Two implementers per person; Cursor or Gemini commands; a PowerShell variant.
- The server changing a remote, merging, renaming files or running any offered command.
- `planning.py`, `dash.py`, the engine (`start`, `wt`, `uak next`), the dashboard's own fetches.
- The identity warning (UI-012), Spanish leftovers (UI-013), planning honesty (UI-010).
- Resuming a previous tool conversation (`--continue`, `resume`): the resume line only reopens the tool in the folder.

## Risks

R1. Codex flags unverified here. `--sandbox workspace-write --add-dir DIR PROMPT` and whether `--add-dir` lifts
    Codex's protection of `.git` in the main checkout must be proven by a real interactive Codex run as `NAME-r`
    (`uak next` succeeds) on macOS and in Windows Git Bash before `done`, recorded as evidence (as UI-006 amendment
    7). If the installed Codex refuses the pair, stop and amend this contract; do not improvise flags.
R2. Folder names: a space or an accent is covered by tests; `'` or a control character → no command; a 253-character
    folder still fails inside `wt` (r4 P3, not fixed here).
R3. `.uak-env` in the main checkout overrides the shell's `UAK_AGENT` (uak:40-58): the review line would run under
    that name. `team_view` should refuse the review command with the same wording `registration_checks` uses when the
    file names an agent other than `NAME-r`. Small; include if the reviewer agrees.
R4. A retire or a claim made in a terminal shows after at most 15 s or the next Check; the register decision always
    reads fresh.
R5. Name change: the old name's registration, roles and claims remain theirs; `bob` sees `ana`'s claims as text only.
R6. Two projects in one server: every cache is keyed by the physical root; the roles file is per repository. One
    `slow` lock for the server means a slow check on one project delays the same page's next POST by at most
    `NET_TIMEOUT` per command.
R7. `gh` not signed in does not block the team step (nothing here calls `gh`); the implementer's PR falls back to
    `wt pr`'s URL. A tool's sign-in is the only auth this step checks.
R8. `claude auth status`/`codex login status` may be slow or need the network: 20 s each, cached 60 s, never under
    `lock`. A tool that signs out mid-session is offered for up to 60 s.
R9. `refs/uak/setup-base` and `refs/uak/setup-claims` stay in the clone (like `refs/uak/dash-*`); they are overwritten
    on each read and never pushed.
R10. Case (a) of the way out leaves `.mine` files and the remote's `.gitignore` without the kit's lines until Repair
     runs; the step says so. Verify that `install.sh --update` re-adds them (install.sh:325-336) in the test or QA.
R11. `git grep` on a claims tree with hundreds of tasks is one process; if a claims file name holds a colon it is
     skipped by the file-name pattern.
R12. Behaviour change: GET `/api/team` and GET `/api/publish-kit` can answer 409 while a worker runs; the page must
     keep its drawing instead of hiding the step.

## Reviewer (claude-Dylan-r)

Verdict: AMENDMENTS (11, all binding). The design (slow lane, private refs, roles in the common Git dir, one safe way out)
is sound and I agree with D2. D1 is NOT minimal as written (amendments 1 and 2). D3: yes, touch
`kit/.uak/settings/known-files.txt` (via `scripts/kit_hashes.py`) and `CHANGELOG.md`; also check `README.md` (it still
words the team step as one tool implements, the other reviews) and update it only if it states the old rule. Nothing else
outside Paths found (the tests dir is globbed, not listed; skills/setup, uak-setup commands and llms.txt do not describe
the team step).

1. D1 is incomplete: line 187 of test_setup_prepare.py (`publish_kit_pushes_only_the_verified_commit`, "git pull" in
   body["error"]) is the UNBORN-local case (`installed()` never commits; the remote's first commit is someone else's
   README). Under this contract that case is the unrelated-history case and gets `way_out`, whose new error text has no
   "git pull" (the command sits in `way_out`). The contract's claims "behind keeps today's message" and "187 stays green"
   are therefore false. Fix without editing the assertion: the 400 `error` string for every unrelated-history case must
   contain the literal `git pull` (for example "...Nothing was changed. The command below runs git pull for you to
   review."). If the implementer prefers other wording, D1 must list this assertion as a third edit and say so. Test 6(e)
   must use a real behind case (local has the remote's older commit) as well as 187's scenario.
2. Second hidden conflict with an existing assertion: test_setup_team.py ~248 (hostile READY lines) requires
   `not body.get("commands")`. The contract keeps the review command when there is no offer. Rule: when the last READY
   line does not parse (no CLAIM_COMMAND match, or TEAM_TASK refuses the ID), `commands` stays empty with a note (today's
   behaviour). The "keep the review command, `task: ""`, `can_check`" path applies only when the line parses to a
   valid task that claims says is taken. Also the note "X was claimed since the last check" is only for that case;
   waiting/hostile get their own notes. Add the hostile lines to test 3 as a negative.
3. Race in the slow lane: GETs (`/api/team`, `/api/plan`, `/api/publish-kit`) check "worker alive" before taking `slow`.
   A POST that holds `slow` starts a worker, releases, and the waiting GET then fetches while the engine runs (and two
   fetches into the same private ref can fail with a ref lock, read as "offline"). Every GET that takes `slow` must
   re-check `worker alive` under `lock` AFTER acquiring `slow` and apply the 409/cache rules then, exactly as do_POST
   does. Also `self.worker = Thread(...)` and `.start()` must both happen inside the same `with lock` (today
   `is_alive()` is False between assign and start). Test: a GET queued behind a POST that starts a worker returns
   409/cache and runs no `fetch`/`ls-remote` (the runner records none) while the worker lives.
4. Caches (`remote_cache`, `tools_cache`, per-key `last_error`, reviewer entry) are read by `/api/status` and written by
   the worker and request threads: every read and write goes through a short `with lock`, never held across a runner
   call. Add to test 5 a check that `/api/status` during a blocked probe (`available_planners` auth probe gated, not only
   `ls-remote`) also answers under 1 s, since probes run under `slow` too.
5. Tool probes: `available_planners` runs `run()` without `group=True`, 20 s each, and now holds `slow`; a hung probe with
   grandchildren can block longer than its timeout and freezes every POST. `planning.py` is out of Paths, so setup.py
   must wrap the probe: call it through a runner adapter that forces `group=True` and caps `timeout` at 20. Correct R6:
   the worst case for one slow-lane request is probes (2 x 20 s) plus up to 3 network commands (3 x 30 s), not "one
   NET_TIMEOUT". Do not claim otherwise in WHY.md/DASHBOARD.md.
6. Claims reading: `check_collisions` (claim.sh:19) refuses a claim when `claims/ID.md` exists in ANY state. The offer
   rule "no CLAIMED/BLOCKED/REVIEW record" would re-offer a task whose claims file has another state. Offer only when
   `claims/ID.md` does not exist at all (any state blocks the offer), and the `claimed` list shows CLAIMED/BLOCKED/REVIEW
   as designed. Identity freeing stays as designed (conservatively ignores lease expiry; say so in a comment). Parse
   `git grep` output by path: `roles/reviewers/*` lines only feed Reviewer/Registered-By (a `State: REGISTERED` line there
   is not a claim state); `ls-remote` must compare the exact ref name (`refs/heads/BASE`), not the tail match.
7. REMOTE/BASE validation is too loose for refs: also reject `..`, `//`, a trailing `/` or `.`, `.lock` components and
   `@{`; plain 400 with one test row. (A bad name must never reach `+refs/heads/BASE:refs/uak/...` and surface as a fake
   "offline".) Distinguish a timeout (exit 124) in the offline detail ("timed out after 30 s") from refusals.
8. Way-out safety: the collision set must include IGNORED and untracked local files and directories (merge silently
   overwrites ignored files), compare case-insensitively on macOS/Windows, and the command is built only when every
   colliding path passes the pattern; a collision that is a directory here but a file on the remote, or the reverse,
   yields `command: ""`. `mv -n` exits 0 without moving when the target exists: the command must therefore be
   `... && test ! -e 'X.mine' && mv -- ...` style or equivalent so a skipped move stops the chain before `git pull`
   (with `&&`, never `;`). Test 6 adds: an ignored colliding file, a directory/file clash, and an existing `.gitignore.mine`
   (all give `command == ""` or a refusing chain, never a lost file; assert file bytes before/after).
9. R1 is a gate, not a note: the recorded evidence for the Codex lines must include a NETWORK/ref write inside the
   sandbox (the reviewer's `uak next` fetches claims and registration/heartbeat push), not only a local `.git` write,
   because `workspace-write` normally has no network. If network is blocked, stop and amend the contract (no improvised
   `-c` flags). Both macOS and Windows Git Bash runs are listed in the evidence; the reviewer (me) must see the output
   before approving `done`. Also keep the `BYPASS` absence assertion for the new lines and assert no argument besides the
   prompt starts with `-` other than the two known flags.
10. R3 is included (binding): `team_view` refuses the review command when `.uak-env` in the main checkout names an agent
   other than `NAME-r` (same wording style as `registration_checks`), with a test. Roles file: write preserves other
   people's entries, replaces an unreadable/oversized/invalid file only after checking it is a regular file in a non-
   symlinked `uak-setup` folder, and a test asserts the file is not in `git ls-files`, not in `git status --porcelain`
   and not changed by `wt new`/a second worktree.
11. Test hardening (each must fail today and use literals, not the code under test):
   a. Tests 2, 7, 9: expected command strings are written out literally in the test (with `q()` only for the path), never
      built from `MODULE` templates, so a wrong template cannot pass itself.
   b. Test 4 and 1: offline also asserts `/api/status`.reviewer.registered is `None` (not a remembered true) and that a
      ls-remote timeout (runner returns 124) reads as offline and is not cached.
   c. One test enumerates every new server note/reason/error and `way_out` step the suite produces and asserts each has an
      entry (or pattern row) in the workspace.js catalog; Spanish is not left to eyeballing.
   d. A unit assertion that GITDIR/ROOT/WT containing `'` or a control char yield no command (use `--separate-git-dir`
      for GITDIR), and that a Windows-style `C:/...` GITDIR is quoted as one word.
   e. test_setup_roles.py must set `MODULE`/`tp.PLANNING` for the imported team helpers in its own `main()`, and the new
      names are appended to each file's `TESTS` list (additions only).
   f. Test 5's 1.0 s bound is kept, but state in the test that it measures one status request (not mean), and run the
      suite 3 times before `done` to show no flake on the slower platform.
