# UI-024 · Implementation contract · the team step leads a beginner through the first run

Base: `origin/next` at 4cda234 (UI-018 + UI-019 merged). UI-024 depends on UI-023 (and so on UI-020/021): those are
not on next yet. Build on next **after** they merge and re-check the line numbers below (they are next@4cda234).
Verify: `python kit/.uak/tests/test_setup_first_run.py` (new file, CLI like `test_setup_trust.py`: `--package`,
`--case`, prints `PASS name` / `FAIL name: …`, ends with `SETUP_FIRST_RUN_RESULT failed=N`).

## 0. Evidence map

| Finding | What happened | Settled in |
|---|---|---|
| A-F6 | Claude Code's trust dialog defaults to "No, exit"; an English "Ignoring 51 permissions.allow entries…" warning the page never mentions; untrusted implementer stopped before shipping | §1 |
| D top-10 #4 (D-3.2) | implement/review commands copyable before the reviewer is registered (also A-F11: the ready line offers a bare `wt new`) | §2 |
| A-F7 | "Comprobar siguiente paso" clears and redraws the list: 4933→3919→4933 px, button jumps 1,014 px | §3a |
| B-10 | hanging remote: check took 75 s, every view answered 409 meanwhile | §3b |
| A-F15, D other (D-9.2) | one blocked reason shown 3 times | §4a |
| A-F16, D top-10 #10 (D-10.2) | two 1–5 numberings (journey bar + wizard rail) | §4b |
| D top-10 #10 (D-10.1) | "Set up my project" at 755 px on 1280×720 | §4c |
| D top-10 #5 (D-6.1) | Check/Repair/Choose project/Save natively disabled during an operation, no reason | §5 |
| D top-10 #6 (D-7.1) | after a planner rule break: "Done at …", green lint box under the red box, "undo" vs "ask for changes" | §6 |
| A-F19 | with 2 people the teammate is never addressed | §7 |
| D other (D-1.1, D-1.2) | trust note shown when Claude Code is not the selected planner; launch commands unexplained | §1, §2 |

D-REPORT.md does not print sub-numbers (3.2, 6.1 …); the D mapping above is by content and is the reviewer's to confirm.

## Paths: one amendment needed before the claim

The task's Paths are setup.py, setup.html, workspace.js, test_setup_first_run.py, WHY.md, CHANGELOG.md, DASHBOARD.md.
§2's server gate makes existing tests that read `/api/team` commands **without registering** fail:
`test_setup_team.py` (agent_launch_commands_are_exact, codex_command_can_write_git, team_step_survives_the_first_claim,
claims_reading_ignores_git_config, offline_team_step_says_offline's later part), `test_setup_roles.py` (lines ~84–201),
`test_setup_resume.py` (~198). Fix is mechanical: a helper `ready_team(srv, target, name="ana")` in test_setup_team.py
= `ready()` + `register(srv, name + "-r")`, used only by tests that read `commands`. **Do not** change `ready()`
itself (reviewer_state_follows_project_and_name asserts `registered is False` after `ready()`). Ask Dylan to add
those three test files to Paths (amendment via `uak plan`) before claiming. `planning.py` is also needed for §6's
undo helper; if Dylan prefers no planning.py change, put `undo_instruction()` in setup.py (it only needs `planning.git`).
known-files.txt: not needed (`scripts/kit_hashes.py` SKIPs `kit/.uak/bin/` and `kit/.uak/tests/`).

---

## 1. Trust: guidance and detection

### Where Claude Code records folder trust (verified on a real install, key names only)
`<config>/.claude.json`, where `<config>` = `$CLAUDE_CONFIG_DIR` if set, else the home directory. JSON object;
`projects` maps an **absolute folder path** to an object; trust is `projects[<path>].hasTrustDialogAccepted === true`.
On macOS/Linux keys are POSIX absolute paths; on Windows assume forward slashes (`C:/Users/...`) but compare
leniently (see risks). The file also holds the account e-mail, MCP server configs (possibly tokens in `env`) and
per-project history: **private**.

### Server: `claude_trust(folders)` in setup.py (read-only)
```
CLAUDE_CONFIG_MAX = 32 * 1024 * 1024
def claude_trust(folders):
    """{folder: True|False|None}. Reads Claude Code's own config, never writes it, keeps only booleans."""
```
- File: `Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home()) / ".claude.json"`. Missing, not a regular file
  (after `stat`, symlink allowed), larger than 32 MB, unreadable, not UTF-8, not JSON, `projects` not a dict → every
  folder `None` (unknown). Never raise into the view.
- Open with `open(path, "rb")` only. No lock, no temp file, no `os.utime`, no write of any kind, anywhere.
- For each folder: candidates = the folder and each of its parents, each in two spellings: `os.path.abspath` and
  `os.path.realpath` (macOS `/var` → `/private/var`), as POSIX strings. On Windows (`os.name == "nt"`) compare
  `key.replace("\\", "/").rstrip("/").casefold()` against the same normalisation of the candidates.
  Trusted = some candidate key has `hasTrustDialogAccepted is True` (exact folder first; a parent counts because
  Claude Code walks up; see risk R2). Present key without the flag, or no key → `False`.
- Keep nothing from the parse except the booleans: build the result inside the function, drop the parsed dict
  before returning (`del data`). Never put the path's content, the file path or any value into `details`,
  `redact()` output, logs or exceptions.
- Cache: `{(path, st_mtime_ns, st_size): result}` of size 1 on the server (under `server.lock`); a changed mtime
  or size re-reads. No TTL needed; Claude Code writes the file when the person accepts.

### View fields
- `GET /api/team`: `view["trust"] = {"project": bool|None, "worktree": bool|None}` **only when** a launch
  command's harness is `claude` (implement and/or review). `project` = the main checkout (the review command runs
  there); `worktree` = `<root>-wt/<task lower>` (the implement command runs there; it usually does not exist yet, so
  it is `False` unless a parent such as `<root>-wt` is trusted). Codex-only → no `trust` key.
- `GET /api/plan`: `view["trust"] = bool|None` for the project folder beside the existing `trust_command`.

### Page (team step and planning step)
One block `<div id="trust-help" class="trust-help">` rendered by a function `trustLine(state)` inside both
`#team-implement` (for `worktree`), `#team-review` (for `project`, Claude only) and `#plan-trust` (for `project`).
Replace the current hints "accept it (yes)" / "accept both" with:

| State | Mark | English (catalog key) | Spanish |
|---|---|---|---|
| true | ✓ (`aria-label="Trusted"`) | "Claude Code already trusts this folder." | "Claude Code ya confía en esta carpeta." |
| false | ✗ (`aria-label="Not trusted yet"`) | "Claude Code does not trust this folder yet, so it will ask first." | "Claude Code aún no confía en esta carpeta, así que te lo preguntará primero." |
| null | i | "Setup could not read whether Claude Code trusts this folder. If it asks, answer as below." | "No se pudo leer si Claude Code confía en esta carpeta. Si te lo pregunta, responde como se indica abajo." |

For false and null, always followed by the keyboard instruction (two lines, `<kbd>` for keys):
- "The question starts on \"No, exit\": press ↓ until \"Yes, proceed\" is selected, then press Enter." →
  "La pregunta empieza en «No, exit»: pulsa ↓ hasta que quede marcado «Yes, proceed» y luego pulsa Enter."
- "If you pressed Enter on \"No, exit\", Claude Code closes: paste the same command again." →
  "Si pulsaste Enter en «No, exit», Claude Code se cierra: vuelve a pegar el mismo comando."

And the expected-warning line (shown for false and null; not for true):
- "Before it, you may see an English warning such as \"Ignoring 51 permissions.allow entries … has not been
  trusted\". That is expected the first time and goes away once you accept." → "Antes puede salir un aviso en inglés
  como «Ignoring 51 permissions.allow entries … has not been trusted». Es normal la primera vez y desaparece al
  aceptar." (The number varies; the line says "such as".)

The quoted dialog labels "No, exit", "Yes, proceed" and the English warning stay English inside `<span lang="en"
data-no-i18n>` (they are what the terminal shows). Then the existing MCP sentence: "Then approve this project's uak
server (MCP)." (Spanish exists or add: "Después aprueba el servidor uak de este proyecto (MCP).").

A "Check again" link-button `#trust-recheck` ("Comprobar de nuevo") re-runs `loadTeam()` (team) / `loadPlan()`
(planning) so ✗ turns ✓ after the person accepts in the terminal; the team view also refreshes on
`visibilitychange` (already polled by UI-019's autoCheck path, but trust needs no engine run: just `loadTeam()`).

`#plan-trust` is shown only when the selected planner is Claude Code (D: trust note shown when Claude is not the
planner): `el("plan-trust").hidden = !planView || !planView.trust_command || selectedPlanner() !== "claude";`.

## 2. Launch commands wait for the reviewer (UI and server)

### Server (`team_view`)
- After `view["registered"] = reviewer_record(...)` and all existing early returns, if
  `view["registered"]["registered"] is not True`: build **no** `commands` (no command or resume strings at all),
  set `view["commands"] = []`, `view["locked"] = {"reason": LOCK_REASON % who, "target": "team-register"}` and
  `view["waiting"] = [{"id": "implement", "tool": TOOL_LABEL[roles["implement"]]}, {"id": "review", "tool":
  TOOL_LABEL[roles["review"]]}]` (labels only, for greyed placeholders). The implement identity is still computed
  so `view["task"]` stays informative.
  `LOCK_REASON = "Register %s first (step 1): agents start only once a reviewer can review their work."`
  Spanish: "Registra primero a %s (paso 1): los agentes empiezan solo cuando hay un revisor que pueda revisar su trabajo."
  (Retired reviewer: reason = the existing retired message; offline/none already returns no commands.)
- `view["note"]` must never repeat `locked.reason` (one place, §4a).
- `claimed[].resume` (reopen an agent that already holds a task) stays available: it starts nothing new.
- `/api/status` is unchanged; the gate lives in the team view, which is the only source of launch commands.

### Page
- `drawTeam`: when `view.locked`, `#team-implement` and `#team-review` render as placeholders: heading
  ("2. {tool} implements" / "3. {tool} reviews"), the terminal hint, **no `<code>`, no Copy button** (hidden, not
  just aria-disabled: there is no text to copy), and one line `#team-locked-why` (class `hint blocked-reason`) with
  `locked.reason`, placed once above both blocks. Register button keeps focus order first.
- After `team/reviewer` succeeds, `loadTeam()` already redraws: commands appear, `#team-locked-why` hides, and focus
  moves to `#team-implement-heading`.
- `drawChecks` ready line (`li.ready-next`, A-F11): the `<code>` with `guidance.commands` is shown only when
  `(data.reviewer || {}).registered === true`; otherwise the text is "Next: register your reviewer in Start your
  team." ("Siguiente: registra a tu revisor en «Arranca tu equipo».") and the button opens the team step
  (`pointTo("team-register")`) instead of "See project progress". Server `guidance()` is unchanged
  (test_unified_workspace keeps its `["bash .uak/bin/wt new APP-001"]`).

## 3. "Check" without a jump, and views that answer during a check

### 3a. No layout jump (A-F7)
Server (`launch`): for `operation == "checking"` **keep** `checks`, `ready`-independent fields, and add
`checks_stale=True`; i.e. `state.update(phase=operation, ready=False, next_command="", next_note="", details="",
error="", checked=False, checks_stale=True)` without `checks=[]` (install still clears). `apply_readiness` sets
`checks_stale=False` with the new list. On a failed/timed-out check (§3b) the old list stays and
`checks_stale=False`, plus the error.

Page (`drawChecks`, inside the UI-018 block, first lines):
```
var list = el("checks"), waiting = data.phase === "checking";
list.classList.toggle("stale", waiting);
if (waiting) list.setAttribute("aria-busy", "true"); else list.removeAttribute("aria-busy");
if (waiting) return false;            // never redraw (or empty) while a check runs
```
then the existing key/redraw. CSS: `#checks.stale { opacity: .55; transition: opacity .2s }`, none under
`prefers-reduced-motion`. Contrast of the dimmed text is decorative-only while `aria-busy` is set; the status line
`#operation-status` already says "Checking…" — add once: "Your last result stays below until the new one arrives."
("Tu último resultado sigue abajo hasta que llegue el nuevo."). No focus move, no scroll.

Interaction with UI-018/UI-019:
- UI-018 `checksKey` dedupe still applies after the check; `checkSummary(before, …)` ("nothing changed") unchanged.
- UI-019 `autoCheck()` dims the same way (it goes through `/api/check`); it never sets `pointAfterCheck`, so no scroll.
- UI-019 kept check (re-picked project): it fills `checks`; the auto-check that follows dims it, never empties it.
- A reload during a check shows the old list dimmed (it is in `/api/status`), not an empty list.

### 3b. Bounded network, views answer (B-10)
- `CHECK_TIMEOUT = 45` in setup.py. `launch()` for `checking` runs `self.run(command, cwd=self.target,
  timeout=CHECK_TIMEOUT, group=True, env=CHECK_ENV)` with
  `CHECK_ENV = {"GIT_HTTP_LOW_SPEED_LIMIT": "1000", "GIT_HTTP_LOW_SPEED_TIME": "10"}` (HTTP stalls end in 10 s;
  `group=True` kills ssh/git-remote-https children on the 45 s timeout). Do not set `GIT_SSH_COMMAND` (it would
  override the person's `core.sshCommand`). Install keeps 120 s.
- Return code 124 → `phase="setup"`, keep old checks, `error = CHECK_TIMEOUT_ERROR % (remote, CHECK_TIMEOUT)` with
  `CHECK_TIMEOUT_ERROR = "The check stopped: %s did not answer within %d s. Your last result is still shown. Check your connection, then press Check again."`
  Spanish: "La comprobación se detuvo: %s no respondió en %d s. Tu último resultado sigue a la vista. Revisa tu conexión y pulsa Comprobar de nuevo."
- `GET /api/dashboard` while a worker runs: return the last good body for this target from `server.dash_cache`
  (filled on every 200), as `dict(cached, stale=True, checking=True)`, status 200. No cache: status 200 with the
  local plan built **without network** (same branch as dash.py's offline fallback: `module.build(empty dir,
  TASKS.md, name)` + `source="local", connection="checking", stale=True`). Never 409 for a view.
- `GET /api/team` while a worker runs (`cached_team`): the cached view `stale=True` (as today); **no cache** →
  status 200 with `{"stale": True, "checking": True, "commands": [], "note": "Checking your project… the commands
  come back when it ends.", "registered": {"registered": None, …}, …base fields of team_view}` instead of `Busy`.
  Spanish: "Comprobando tu proyecto… los comandos vuelven cuando termine."
- `GET /api/plan`: already `plan_view(False)` (200). `GET /api/publish-kit` stays 409 (it is an action preview).
- Page: a `stale` team/dashboard view keeps what is drawn, dims it (`.stale`), and Copy buttons on a stale view are
  aria-disabled with the §5 reason (a command may be outdated mid-check).

## 4. One place per reason, one step model, CTA above the fold

### 4a. One place per blocked reason (A-F15)
Rule: a blocked reason has **one persistent place**, the `#<button>-why` line under its button (aria-describedby);
the toast is only the click's feedback (UI-018, keep: 8 s, pause on hover/focus, Esc). Any `.notice` that restates
a reason must go:
- delete `#plan-onmain-note` (restates planBlock's "Publish the kit to main first (step 3).");
- `team_view.note` never equals `locked.reason` (§2);
- the identity box / `#error` never repeats `nameBlock`'s "Save your name first (step 1).".
Implementer: grep every `text:` in `planBlock`, `nameBlock`, `BUSY_REASON`, `LOCK_REASON` and make sure no
`.notice`/`#error` markup or code path shows the same string.

### 4b. One step model (A-F16, D-10.2)
The journey bar (`#journey`, 1. Install … 5. Follow progress) is the only numbered model.
- Wizard rail `#steps`: drop the digits. Each `.step-number` shows "•" (current/todo) or "✓" (done, `aria-label`
  "Done"); the rail gets a heading "1. Install" ("1. Instalar"), so its items read as sub-steps of journey step 1.
- After install the rail is hidden: render sets `document.body.classList.toggle("installed", !!data.installed)`;
  CSS `body.installed .sidebar { display: none }` and `body.installed .layout { grid-template-columns: 1fr }`.

### 4c. CTA above the fold (D-10.1)
In `#welcome`, move `<button class="primary" id="begin">Set up my project</button>` and its "Already using the
kit?" hint to right after the **first** `p.intro`, before the second `p.intro`, `.benefit` and `#demo`. Target:
top of `#begin` ≤ 600 px at 1280×720 (journey bar + eyeline + h1 + one intro).

## 5. Busy-disabled buttons say why (D-6.1)
Inside the UI-018 block add:
```
var BUSY_REASON = {
  installing: "Wait: the kit is being installed.", checking: "Wait: setup is checking your project.",
  planning: "Wait: the coding tool is drafting the plan.", approving: "Wait: the plan is being approved.",
  publishing: "Wait: the kit is being published.", registering: "Wait: the reviewer is being registered." };
function setWaiting(button, phase) { … }
```
Spanish: "Espera: se está instalando el kit." / "Espera: se está comprobando tu proyecto." / "Espera: la herramienta
está escribiendo el plan." / "Espera: se está aprobando el plan." / "Espera: se está publicando el kit." /
"Espera: se está registrando al revisor."
`setWaiting(button, phase)`: when `isBusy(phase)` and the button is not that phase's owner (owner keeps `aria-busy`
and its busy label, UI-018) → `setBlocked(button, {text: BUSY_REASON[phase]})` (aria-disabled, focusable, click →
toast with the reason, `#id-why` line if one exists); when not busy → `setBlocked(button, <its real block or null>)`.
Replace every native `X.disabled = busy` / `= operationBusy()` for these **buttons**: check, next-check,
change-project, repair, save, human-save, schedule-save, publish-preview, publish-kit, idea-save, plan-create,
plan-change, plan-recheck, team-register, team-retry, team-check, refresh-dashboard, and the project/workflow
submit buttons and `#install`. Form inputs may stay natively disabled (the running-review notice explains).
The server stays the guard (409 on POST during a worker).

## 6. Planner rule break: "Terminó con problemas" (D-7.1)

### Server
- `plan_run` keeps `before["head"]`; when `found` is non-empty: `plan["undo"] = undo_instruction(...)`,
  state `phase="planned"` (or `"error"` when the plan file is missing, as today), `error=""` for a written plan,
  and `state["outcome"] = "problems"`, `state["problem"] = "The planner changed things only you may change."`
  ("La herramienta cambió cosas que solo tú puedes cambiar."). A clean run sets `outcome=""`, `problem=""`.
- `undo_instruction(run, root, before, after, found) -> {"text": str, "command": str}`:
  - git-undoable kinds: HEAD moved, index changed, tracked files changed (in `before["files"]`, tracked at
    `before["head"]`: one `git ls-tree -r --name-only -z <before_head> -- <paths>`).
  - not git-undoable: Git config, hooks folder, files the planner created that did not exist before, an empty
    `before_head`, a path that is not `quotable()`.
  - All undoable → `command = "cd %s && git reset -q %s && git restore --source=%s --worktree -- %s"`, parts
    joined only when needed: `git reset -q <before_head>` iff HEAD or index changed; `git restore --source=<before_head>
    --worktree -- <shell_quote(p)…>` iff tracked files changed (sorted). Root = `shell_quote(Path(target).resolve().as_posix())`.
    `text = "Undo it with this command, then press Create the plan again:"` → "Deshazlo con este comando y luego pulsa Crear el plan otra vez:".
    `.uak/TASKS.md` and `.uak/OWNERS.md` are never restored (they are the plan).
  - Anything not undoable → `command = ""`, `text = "Undo these changes by hand, then press Create the plan
    again."` → "Deshaz estos cambios a mano y luego pulsa Crear el plan otra vez." (the violation list names them).
  - Setup never runs this command; it only shows it.
- `approval_checks` refusal text when violations exist: "The last planning run changed things only you may change.
  Undo them with the instruction under Proposed plan, then create the plan again." (Spanish in the catalog.)

### Page
- `drawPhaseButtons`: when a planning run ends with `data.outcome === "problems"` →
  `report(owner, format("Finished with problems at {time}: {problem}", …), true)` instead of `done()`.
  Catalog: "Finished with problems at {time}: {problem}" → "Terminó con problemas a las {time}: {problem}".
- `drawPlan`, when `view.violations.length`: hide `#plan-lint` (no green "passes" box), hide `#plan-ask`
  (no "Ask for changes"), hide/aria-block `#plan-approve` with reason "Undo the planner's changes first, then
  create the plan again." (replaces "Fix the plan's problems first: ask for changes." for this case), and inside
  `#plan-violations`: the list, then `#plan-undo-text` + (if command) `<code id="plan-undo-command" data-no-i18n>` +
  Copy `#copy-plan-undo`. Remove the static sentence "Undo those changes, then create the plan again." from the
  box markup (the undo text is the one instruction). The box heading: "The planner broke a rule" ("La herramienta
  rompió una regla").

## 7. Two-person note (A-F19)
`team_view` adds `view["people"]` = N from the project's `IDEA.md` line `- Team size: N person|people` (regex
`^- Team size: (\d{1,2}) `, local read, 0 when absent). The page shows `#team-two-people` (a `.team-block`, first
in the team step after the heading) when `people !== 1`:
- "Two or more people? Each person uses their own computer: they clone the project, open this page there, save
  their own name and register their own reviewer (name-r). You run the commands shown on your page; your teammate
  runs the ones on theirs. Never paste a teammate's commands: they carry their name."
- Spanish: "¿Sois dos o más? Cada persona usa su propia computadora: clona el proyecto, abre esta página allí,
  guarda su nombre y registra su propio revisor (nombre-r). Tú ejecutas los comandos de tu página; tu compañero, los
  de la suya. Nunca pegues los comandos de otra persona: llevan su nombre."
  (UI-021 decides tú vs vosotros; if it settles on tú only, use "¿Son dos o más?" → keep consistent with UI-021.)
- One short line under each launch block: implement "Terminal 1 · on your computer" / review "Terminal 2 · on
  your computer" (existing terminal strings, add "on your computer").

## 8. Tests: `kit/.uak/tests/test_setup_first_run.py`

Imports like test_setup_trust.py: `test_setup_planning as tp`, `test_setup_wizard as wizard`, `test_setup_team as
team` (Team runner, `ready_project`, `ready`, `register`, `by_id`, `fresh`), `test_setup_feedback as tf`
(`run_page`, `page_function`, `catalog`, `tree`). `main()` loads setup.py/planning.py from `--package` and sets
`wizard.MODULE`, `team.MODULE`, `tp.PLANNING` as test_setup_trust does. Every test sets `CLAUDE_CONFIG_DIR` to a
temp dir for its duration (restore in `finally`) so no test reads the developer's real `~/.claude.json`.
Fake-DOM parts return `None` without Node (print the note, keep the static assertions).

### trust_step_is_explicit
Fixture: `ready_project(root, tmp)` (claude+codex), Team() with roles so implement=claude; `ready` + `register`.
`cfg = tmp/"cfg"`; `.claude.json` = `{"projects": {<realpath(root) posix>: {"hasTrustDialogAccepted": true,
"mcpServers": {"x": {"env": {"TOKEN": "tok-SECRET-123"}}}}}, "oauthAccount": {"emailAddress": "ana@example.invalid"}}`.
Assertions:
1. `/api/team` → `trust == {"project": True, "worktree": False}` (fails today: no `trust` key).
2. The response body (raw bytes) contains neither `tok-SECRET-123` nor `example.invalid` nor `.claude.json`.
3. `.claude.json` bytes and `st_mtime_ns` unchanged after 3 GETs; `os.listdir(cfg) == [".claude.json"]`.
4. Rewrite the file with the key on `<realpath(root)>-wt` → `worktree is True` (parent rule) and the cache noticed
   the change (mtime/size key).
5. File with `{not json` → both `None`; file removed → both `None`; status 200 each time.
6. Codex-only roles (`/api/team/roles` implement=codex, review=codex) → no `trust` key.
7. `/api/plan` has `trust is True` for the project.
8. Markup/catalog: `#team-implement` and `#plan-trust` contain `id="trust-help"`-rendered or static text with
   "↓", "Enter", "No, exit", "Yes, proceed", "permissions.allow"; catalog has the four English lines of §1 with
   Spanish containing "↓", "Enter", "«No, exit»", "«Yes, proceed»" (fails today: no "↓").
9. Static: `el("plan-trust").hidden = …selectedPlanner() !== "claude"` (regex) (fails today).
10. Static: setup.py has no `open(` of the config with a write mode, no `write_text`/`write_bytes`/`replace` on a
    path containing `claude.json` (regex over the `claude_trust` function source).

### commands_wait_for_the_reviewer
Fixture: `ready_project`, Team(); `IDEA.md` written with "- Team size: 2 people".
1. `ready(srv)` (no register) → `/api/team` 200, `commands == []`, `locked.reason` contains "ana-r",
   `locked.target == "team-register"`, `[w["id"] for w in waiting] == ["implement", "review"]`, and the raw body
   contains no "wt new" and no "UAK_AGENT=" (fails today: both commands present).
2. `note != locked.reason`; `spanish_for(view)`-style: `locked.reason` pattern is in the catalog.
3. `register(srv)` → `/api/team` has implement + review commands, no `locked`.
4. Retired reviewer (`team.retire` helper) → `commands == []`, `locked.reason` == retired message.
5. `people == 2`; markup has `id="team-two-people"` whose visible text contains "own computer" and every visible
   line is in the catalog.
6. Fake DOM (`tf.run_page`): `drawChecks({ready: true, guidance: {commands: ["bash .uak/bin/wt new APP-001"]},
   reviewer: {registered: false}, checks: []})` → no visible `<code>` under `#checks` with "wt new"; with
   `registered: true` it is visible. (drawChecks is in the UI-018 block.)

### check_does_not_jump
1. Server: Team() whose `uak start` blocks on `team.check_gate` (new attribute; wrap like `net_gate`). After a
   first finished check (2 lines), POST `/api/check` → while blocked, `/api/status` has `phase == "checking"`,
   the **same** `checks` as before and `checks_stale is True` (fails today: `checks == []`). Release; new checks,
   `checks_stale is False`.
2. Fake DOM: `drawChecks(data)` with 2 lines; then `drawChecks({phase: "checking", checks: data.checks})` and
   `drawChecks({phase: "checking", checks: []})` → `list.replaced` unchanged, 2 rows, class `stale`,
   `aria-busy="true"` (fails today: the empty call replaces). Then `drawChecks({checks: [one line]})` →
   replaced once, no `stale`, no `aria-busy`.
3. Busy reasons (§5), fake DOM: `setWaiting(el("check"), "checking")` → `aria-disabled="true"`, not natively
   disabled, click shows the toast with `BUSY_REASON.checking`; catalog has all six Spanish reasons. Static: no
   `el\("(check|next-check|change-project|repair|save|human-save|schedule-save|publish-preview|publish-kit|idea-save)"\)\.disabled = (busy|operationBusy\(\))`
   remains in the script (fails today: lines ~2213, 4038, 4227–4236).
4. One place (§4a): `'id="plan-onmain-note"' not in html`; for every reason string in `planBlock`/`nameBlock`
   (regex `text: "([^"]+)"`), no `.notice` in the markup contains it.
5. One step model (§4b): no `<span class="step-number">[1-5]<` in `#steps`; a CSS rule `body.installed .sidebar`
   with `display: none`.
6. CTA (§4c): within `#welcome`, `index('id="begin"') < index('class="benefit"')` and less than the index of the
   second `class="intro"` (fails today).

### views_answer_during_a_check
Fixture: `ready_project`, Team() with `check_gate` (hanging `uak start`), `ready` + `register`.
1. Before the check: GET `/api/dashboard` 200 (fills the cache).
2. POST `/api/check`, wait until the runner entered `start`. Then, each within 3 s: `/api/dashboard` → 200 with
   `stale is True` (fails today: 409); `/api/team` → 200 with `stale is True`; `/api/plan` 200; `/api/status` 200.
3. A second project picked during no worker, never viewed, then a hanging check: `/api/team` → 200,
   `checking is True`, `commands == []` (fails today: 409 via `Busy`); `/api/dashboard` → 200, `stale is True`,
   `connection == "checking"`, and `team.net` shows no fetch/ls-remote beside the worker.
4. The check call recorded by the runner: `timeout <= 45`, `group is True`, `env` has
   `GIT_HTTP_LOW_SPEED_LIMIT == "1000"` and `GIT_HTTP_LOW_SPEED_TIME == "10"` (fails today: timeout 120, no env).
5. Runner returns 124 for `start` → state `error` contains "45 s" and the remote name, `checks` == the previous
   ones, `phase == "setup"`; the error is in the catalog (pattern).

### rule_break_is_not_done
Fixture: `tp.project(root, tmp)`; `FakePlanner(misbehave="edit-other")`, then `"approve-and-commit"`, then
`"git-config"` (reset the repo between runs as `planner_never_approves_or_pushes` does).
1. edit-other: `/api/status` → `outcome == "problems"`, `error == ""`, `problem` set (fails today: no `outcome`).
   `/api/plan` → `undo.command == "cd %s && git restore --source=%s --worktree -- 'AGENTS.md'" % (q(root.resolve()), before)`
   where `before` = `git rev-parse HEAD` taken before the run. Run it with `bash -c` (helper like
   test_setup_prepare's `bash_line`): exit 0, AGENTS.md equals its committed content, `.uak/TASKS.md` still the plan.
2. approve-and-commit: command starts `cd … && git reset -q <before> && git restore --source=<before> --worktree --`
   and includes `'.uak/PROJECT.md'`, not `.uak/TASKS.md`; after running it `HEAD == before` and PROJECT.md has
   `Backlog-Approved: no`.
3. git-config: `undo.command == ""`, `undo.text` == the by-hand line (catalog has it).
4. Fake DOM: state `{phase: "planning"}` → `drawPhaseButtons({phase: "planned", outcome: "problems", problem: "…"},
   "planning")` in Spanish → `#plan-create-result` text starts with "Terminó con problemas", has class `error`,
   does not contain "Listo" (fails today: "Listo a las …").
5. Static `drawPlan`: `plan-lint` and `plan-ask` hidden when `violations.length` (regex); `#plan-violations`
   markup no longer contains "Ask for changes" nor the static "Undo those changes" sentence; it contains
   `id="plan-undo-command"` and `id="copy-plan-undo"`.

### Existing suites to run green (no new assertions)
test_setup_team, test_setup_roles, test_setup_resume (after the `ready_team` helper), test_setup_feedback,
test_setup_trust (its `team` text check "trust" must still pass), test_setup_prepare, test_setup_planning,
test_unified_workspace, then `cd kit && bash .uak/bin/smoke --package-only` and `python3 scripts/kit_lint.py`.

## 9. Risks

| # | Risk | Handling |
|---|---|---|
| R1 | Windows: `.claude.json` key format (`C:/…` vs `C:\…`, drive-letter case), `%USERPROFILE%` vs `HOME` | normalise separators + casefold on `nt`; `Path.home()` (USERPROFILE); unknown → `None`, never ✗; README note "On Windows the ✓/✗ is best effort". Commands still say "paste in Git Bash" (existing `#team-windows`). |
| R2 | Trust inheritance: a parent key counted as ✓ may not match Claude Code's rule in a future version; the worktree is a **sibling** (`<root>-wt`), so trusting the root never covers it | exact folder first; parent → ✓ only with `hasTrustDialogAccepted is True`; the keyboard instruction is still one click away (#trust-recheck). WHY.md cites A-F6. |
| R3 | Stale cache: the person accepts in the terminal, the page still shows ✗ | cache keyed by mtime_ns+size (no TTL); "Check again" button; refresh on `visibilitychange`. Claude Code writing late or a half-written file → parse error → `None` ("could not read"), never a wrong ✓. |
| R4 | Privacy of reading Claude's config (e-mail, MCP tokens, history) | read-only `rb`, 32 MB cap, only booleans leave the function, nothing in details/logs/redact, test 2 and 3 enforce it; CHANGELOG + DASHBOARD.md say "setup reads only whether Claude Code trusts the folder, from Claude Code's own config, and never changes it". Never write Claude's config (no auto-trust): trusting is the person's act. |
| R5 | `CLAUDE_CONFIG_DIR` set in the terminal that started setup but not where Claude runs (or vice versa) | read from setup's environment; mismatch → likely `False`/`None`, still with instructions. |
| R6 | Server gate breaks 3 test files outside Paths | Paths amendment first (above). |
| R7 | 45 s check timeout too short on a slow but working network (big fetch) | low-speed limit only ends *stalled* HTTP; 45 s total covers the engine's ls-remote/fetch of small refs; the error keeps the old list and says press Check again. Revisit with blackbox data. |
| R8 | Dimmed list hides a real change in height (fewer lines after the check) | one redraw at the end is a real change, not a jump during the wait; acceptable. |
| R9 | Undo command on a repo where the person also staged work before the run | `git reset -q <before_head>` unstages it (content stays on disk); the text says "then press Create the plan again" — WHY.md notes it; only included when HEAD/index changed. |
| R10 | UI-020/021/023 land first and move strings (tú, Spanish patterns, offline dashboard fallback) | rebase on next after them; reuse UI-023's no-network dashboard builder if it exists instead of §3b's local build. |

## 10. Docs
- WHY.md: one entry per rule (trust detection A-F6; commands gated D top-10 #4 + A-F11; dimmed check A-F7; bounded
  check + stale views B-10; one place A-F15; one step model A-F16; CTA D-10; busy reasons D-6; rule break D-7;
  two people A-F19).
- CHANGELOG.md (Unreleased): user-visible lines in plain English.
- docs/DASHBOARD.md: `/api/team` new fields (`trust`, `locked`, `waiting`, `people`, `checking`), `/api/status`
  (`checks_stale`, `outcome`, `problem`), `/api/plan` (`trust`, `undo`), `/api/dashboard` stale during a check.
