# UI-019 implementation contract: coming back to a project, the setup page restores where you were

Base: main 1124dab. Files: `kit/.uak/bin/lib/setup.py`, `setup.html`, `workspace.js`, new `kit/.uak/tests/test_setup_resume.py`.
Line numbers below are from 1124dab.

## 0. Findings that shape the design (read first)

1. **localStorage does not survive a restart.** The server binds `("127.0.0.1", 0)` (setup.py:539), so every restart is a
   new origin (new port). `uak-human`, `uak-profile`, `uak-language`, `uak-dash-theme` are all lost on restart today. This
   is the real cause of A-F2 (name forgotten). Consequence: **restart = server truth only; localStorage only helps a
   reload on the same server.** Language/profile lost on restart is a separate follow-up (out of scope).
2. **`main()` never inspects its target** (setup.py:2083-2104): state starts at `phase: "welcome"`, `server.target == ""`.
   That is "restart landed on Welcome".
3. **Existing tests pin behaviour that must not change** (tests only grow; only `test_setup_resume.py` is in Paths):
   - `test_setup_wizard.py:74`: `LiveServer(missing)` → `phase == "welcome"`. So the start inspect is called from
     `main()`, not from `make_server()`/`__init__`.
   - `test_setup_team.py:169`: `GET /api/team` without a name → **400**. So "asks inline" is a structured 400
     (`need: "human"`), not a 200.
   - `tt.ready()` does inspect → human → check; a server-side auto-check launched by inspect would make `/api/human`
     answer 409. So **the page triggers the auto-check, never the server**.
   - `/api/inspect` refuses any key but `target` ("Provide only the project folder.").
4. `plan_view(probe=False)` (a worker runs) reads `plan_known`, empty after a restart → `kit_on_main: false` → the page
   says "Publish the kit first" for an approved project while the first check runs. Must be seeded (section 2.3).
5. The team step lives in the **dashboard shell** (setup.html:1838), not in Configuration. "Land on the team step" means
   section `dashboard` with `#team-step` visible.
6. "Comprobar siguiente paso stuck": when `refresh()` fails (server gone) the busy label of the check button is never
   cleared (`setBusy` stays on). The gone handler must clear every busy button.
7. The schedule stores only `Freeze-Epoch` in PROJECT.md; start/end/zone cannot be restored from the repo. The done row
   shows the freeze time; the raw inputs are restored only from the reload draft.

## 1. Scope

In: server-side resume facts on start/inspect; human name persisted per clone; structured 400 from `/api/team`;
page landing (section + step), done/collapsed Prepare steps, planning hidden once approved, auto-check after inspect,
re-pick keeps the last check, reload keeps section and drafts, server-gone banner with back-off.

## 2. State model (server)

### 2.1 `project_progress(server, root)` → `resume` (new, setup.py)

Cheap, local, bounded. **No network, no engine, no coding-tool probe.** Runs outside `server.lock`; on `/api/inspect`
it runs inside the slow lane (it is a POST) but before the `with s.lock:` block of `dispatch`. Uses
`server.identity_run` (plain `run_command`), never `server.run` (the operation runner is counted and gated by tests,
same reason as `signing_identity`). Each Git call `timeout=10`; any failure yields "unknown" (`None`), never an error
for inspect.

Reads (at most 5 Git processes + the existing config read):

| Fact | How | Value |
|---|---|---|
| `installed` | `kit_present(root)` and `failed_target != root` | bool |
| `main_checkout`, common dir | one `git rev-parse --absolute-git-dir --git-common-dir` (reuse `git_dirs` logic with `identity_run`) | bool, Path |
| `human` | `read_human(common)` (section 2.2) | name or "" |
| `freeze` | `Freeze-Epoch` of the working-tree `.uak/PROJECT.md`, via the engine reader: give `read_config` a `keys` parameter (default unchanged so `settings` keeps its four keys) | int, 0 = not set |
| `idea` | `planning.regular_file(root, "IDEA.md")` is a non-empty file | bool |
| base ref | one `git for-each-ref --format=%(refname) %(objectname) refs/uak/ refs/remotes/<remote>/`; first that exists of `refs/uak/setup-base`, `refs/remotes/<remote>/<base>` (`remote_and_base()`; on ValueError → unknown) | ref or None |
| `kit_on_main`, `plan_approved`, `base_sha` | one `git show <base ref>:.uak/PROJECT.md`: exit 0 → kit on main; first `(?m)^Backlog-Approved:[ \t]*(\S+)` == `yes` → approved; `base_sha` = first 7 chars of the ref's SHA | True/False/None (None = no local copy of the ref) |
| claims ref | first of `refs/uak/setup-claims`, `refs/uak/dash-claims`, `refs/remotes/<remote>/claims` | ref or None |
| `reviewer`, `claims` | `read_claims(git, result, ref)` (2 local commands, already ref-parameterised): `reviewer` = `human + "-r"` in `reviewers` and not in `retired`; `claims` = `len(result["files"])` | True/False/None, int/None |

Furthest real step (furthest evidence wins; sub-facts only mark sub-steps done):

```
not installed            → "install"
claims and claims > 0    → "progress"
plan_approved is True    → "team"
kit_on_main is True      → "plan"
otherwise                → "prepare"
```

`resume` is a **hint from the last local copy** (`"source": "local"`). The gate (`uak start`) stays the only authority
for `ready`; the auto-check (section 4.3) confirms or corrects within seconds. `resume` never enables a human act:
`team_context`, `publish_checks`, `approval_checks` are unchanged.

When it is recomputed: `open_target()`, every `/api/inspect`, at the end of every worker (one place: the `drained()`
wrapper in `start_worker`, after `work()` returns, outside the lock), and after a successful `/api/schedule` (not
preview), `/api/idea`, `/api/human`. `/api/status` only copies it from `state` (stays lock-only, UI-011).

### 2.2 Human name per project

- File: `<git common dir>/uak-setup/human.json`, content `{"version": 1, "name": "ana"}\n` (same folder as
  `roles.json`, separate file: `write_roles` rewrites its whole file and would drop a foreign key). Per clone, shared by
  linked worktrees, never committed (inside `.git`).
- `read_human(gitdir)`: returns "" when the folder or file is a symlink, not a regular file, larger than 4096 bytes, not
  JSON, not a dict, or `name` fails `HUMAN_NAME.fullmatch`. Never raises.
- `write_human(planning, gitdir, name)`: same refusals as `write_roles` (folder is a link or not a directory; file is a
  link or not a regular file → ValueError), `folder.mkdir(exist_ok=True)`, `planning.write_atomic`. Factor the shared
  checks of `read_roles`/`write_roles` into one helper rather than copying them.
- `POST /api/human` (validation unchanged): set `state["human"]`, then if a target is set try `write_human`. The name is
  never blocked by the file: reply 200 either way (shape in section 3). Writing happens in the slow lane, outside the lock.
- On inspect / `open_target`: `human = read_human(common) or <current session name>`; `human_source` =
  `"project"`, `"session"` (carried from another project in this server, memory only, **not written on inspect**) or `""`.

### 2.3 New/changed server state

- `state["resume"]` (dict, section 3), `state["inspect"]` (int, +1 on every inspect and on `open_target`),
  `state["checked"]` (bool: False wherever `checks` is reset to `[]`, True in `apply_readiness`),
  `state["human_source"]`.
- `server.checks_kept = {}`: `normcase(str(root))` → `{"ready", "checks", "next_command", "next_note", "details",
  "phase", "freeze", "at": time.monotonic()}`, saved under the lock at the start of an inspect (for the outgoing
  target, only when `checked` and phase in `("setup", "ready")`) and in `apply_readiness`.
- Re-pick: `/api/inspect` restores the kept entry when it is for this root, younger than `CHECK_KEEP = 600` s,
  `installed` is unchanged and `failed_target != root`; then `checked: true`. Otherwise today's reset. `s.forget(root)`
  and `tools_cache.pop` stay as they are.
- `plan_known[str(root)]` is seeded at inspect with `([], bool(resume["kit_on_main"]), "")` when absent, so a GET
  `/api/plan` during the first check never claims the kit is unpublished.
- `SetupServer.open_target()` (new; called by `main()` after `make_server`, before printing the URL; never by
  `make_server`): `project_root(state["target"])`; on ValueError or when `not kit_present(root)` or
  `install_unfinished(root)` → do nothing (stays `welcome`: first-time users keep the welcome screen). Otherwise the
  same state update as inspect (`target`, `installed`, `can_repair`, `phase: "setup"`, identity, human, resume,
  `inspect: 1`, `checked: false`). No worker, no network. Never raises (catch `OSError`, `ValueError`,
  `subprocess.SubprocessError`).

## 3. API changes (all additive; nothing existing is removed or renamed)

`GET /api/status`, `POST /api/inspect` reply gain:

```json
{
  "human": "ana", "human_source": "project",
  "inspect": 3, "checked": false,
  "resume": {
    "step": "team",
    "installed": true, "main_checkout": true,
    "human": true, "freeze": 4102444800, "idea": true,
    "kit_on_main": true, "plan_approved": true, "base_sha": "9e6debb",
    "reviewer": null, "claims": 0,
    "source": "local"
  }
}
```

`resume` is `{}` before any target. `null` means "no local copy to read"; the page treats null as "not known yet", never as done.

`POST /api/human {"name": "ana"}` → 200:

```json
{"human": "ana", "persisted": true, "note": ""}
```

`persisted: false` with `note: "Setup could not remember your name for this project (.git/uak-setup/human.json is a link or not a regular file). It is kept until you close setup."` when the file is refused or no target is set (`note: ""` in the no-target case).

`GET /api/team` refusals stay 400 and gain `need` (new `Need(ValueError)` carrying it; `refusal()` adds the key like `way_out`):

```json
{"error": "Tell setup your name first (Your name, in Prepare): registering the reviewer is a human act.", "need": "human"}
{"error": "Press Check what's next first: the team starts after the readiness check says Ready.", "need": "check"}
```

`POST /api/team/reviewer` gets the same bodies (it shares `team_context`). Error texts unchanged.

`GET /api/plan` gains `"approved": true|false` (`resume.plan_approved is True`) and `"approved_sha": "9e6debb"`.

`POST /api/inspect` on the current target keeps the last check (section 2.3). Request shape unchanged.

## 4. UI changes (setup.html, workspace.js)

All new page logic sits between `// UI-019 resume: begin` and `// UI-019 resume: end` (one contiguous block, like
UI-018's feedback block) and is made of small pure functions the tests run under Node:

| Function | Contract |
|---|---|
| `savedKey(target)` | `"uak-setup:v1:" + target` |
| `readSaved(target)` | parsed object or `{}`; `{}` when missing, not JSON, `v !== 1`, `target` mismatch, `at` older than 7 days, or `section` not in `setup`/`dashboard`; every access in try/catch |
| `writeSaved(target, patch)` | merges `patch`, stamps `at`, caps each draft at 20000 chars; no-op without target; never stores the token |
| `landing(data, saved)` | `{section, panel}`: `welcome` phase → `{setup, 0}`; `options` → `{setup, 2}`; installed → panel 4 and `section = saved.section` if set, else `dashboard` when `resume.step` is `team`/`progress`, else `setup`; not installed → `setup` regardless of `saved` |
| `stepsDone(data)` | `{name: !!data.human, schedule: resume.freeze > 0, publish: resume.kit_on_main === true, plan: resume.plan_approved === true}` |
| `planningVisible(data)` | today's rule AND `resume.plan_approved !== true` |
| `shouldAutoCheck(data)` | `installed && !checked && !error && !isBusy(phase) && !requestBusy && !gone && autoCheckedFor !== target + ":" + inspect`; the caller sets `autoCheckedFor` before posting |
| `probeDelay(n)` | `[2000, 4000, 8000, 16000, 30000, 30000][n]`, `undefined` after that |
| `serverLost(e)` / `serverBack()` | section 4.5 |

### 4.1 Landing (boot, re-pick, target change)
- Boot: `api("status")` → `landing(data, readSaved(data.target))` replaces the unconditional `show(4, false)`
  (setup.html:3875-3882). For `dashboard`: `show(4, false)`, `render(data)`, `openSection("dashboard")`,
  `loadDashboard()`. No focus move on boot. `data-loading` is removed only after the landing is applied (UI-018: no flash).
- `openSection` calls `writeSaved(state.target, {section})` (B-14: the active tab survives reloads).
- `project-form` submit uses the same `landing` after inspect (re-pick lands where the project is, not on Prepare).
- `render`: when `data.target !== previous target` (another tab re-picked on the same server) re-run the landing and
  drop `planView`, `teamView`, `latestDashboard`.
- `journeyStep(data)`: with no finished check (`!data.checked`) return `data.resume.step`; afterwards today's logic,
  except `plan` is never returned when `resume.plan_approved === true`.

### 4.2 Completed steps shown done and collapsed (A-F4, A-F8, B-04)
- Each `.prepare-step` (`name-step`, `schedule-form`, `publish-step`) gets a summary line (`#name-done`,
  `#schedule-done`, `#publish-done`) and a "Change" button (`#name-reopen`, …). `drawPrepare` sets `data-done` from
  `stepsDone(data)`; CSS hides the step's body under `[data-done]:not([data-open])`.
- Texts (English keys + Spanish in workspace.js): `"Saved: {name}."` (exists), `"Freeze set: {when}."` (epoch formatted
  in the browser's zone), `"Published on main (commit {sha})."` → "Publicado en main (commit {sha}).", `"Done"` → "Hecho",
  `"Change"` → "Cambiar".
- `el("prepare").hidden` and `el("planning").hidden` use `planningVisible`; when the plan is approved the planning
  panel shows one done row `"Plan approved on main (commit {sha})."` and no `plan-create` / `plan-change` / idea form
  ("Crear el plan" is never offered for an approved plan). `loadPlan()` is skipped while planning is hidden.
- No jumping: done/collapsed is decided in the first `render` before `data-loading` is lifted; later it changes only
  when an operation the person started finishes. Polling never toggles `data-done` back and forth (`null` facts keep
  the previous drawing).

### 4.3 Auto-check after inspect
- After every `render`, `if (shouldAutoCheck(data))` → `startCheck(false)`, `lastButton = "check"` (or `next-check` in
  the dashboard), `checkAuto = true`, `api("check", {})` then `refresh()`. Once per `target:inspect`; never retried on
  failure (a 400 such as a kit version mismatch goes to the check's result line through `failed()`, a 409 is ignored:
  the running operation renders when it ends).
- Order on landing: post the check **before** any `loadPlan`/`loadTeam` GET, so the slow lane is not first taken by a
  20 s tool probe; `loadTeam` runs when the check ends (render already does this for `ready`/`team`).
- While it runs: the check button shows its UI-018 busy label and then `report(... checkSummary ...)` in its reserved
  result line. With `checkAuto`: no `pointTo`, no `NEXT_FOCUS`, no toast, and **no automatic
  `openSection("dashboard")`** (A-F11/B-14: the page does not switch tabs by itself; the landing already chose).
  The existing 60 s beginner `autoCheck` is unchanged apart from returning early when `gone`.

### 4.4 Team step asks for the name inline (A-F2)
- `#team-step` gains `#team-name-block` (hidden by default): label, `<input id="team-name">`,
  `<button id="team-name-save">`, `<p id="team-name-status" role="status">`.
- `loadTeam` no longer returns early on `!state.ready && !state.team` when `resume.step` is `team`/`progress`. On a
  400: `e.body.need === "human"` → show `#team-step` with only the name block and the translated error;
  `need === "check"` → show `#team-step` with "Checking your project…" in `#team-note` (the auto-check is running or
  about to); any other 400 hides the step as today.
- `team-name-save` → `POST /api/human` → `refresh()` → `loadTeam()`. The Prepare name field and this one show the same
  value. A `persisted: false` note is shown in the status line, translated.

### 4.5 Reload keeps values
- Drafts written on `input` (debounced 300 ms) to `writeSaved(target, {drafts})`: `human-name`, `team-name`,
  `schedule-start`, `schedule-end`, `schedule-zone`, `idea-text`, `idea-audience`, `idea-goal`, `idea-length`,
  `idea-team`. Never the approval confirmation, never the target of another project.
- `restoreDrafts(saved)` after the first render: fills a field only when it is empty and not focused; a server value
  (saved name, saved idea) wins. A draft is dropped when its step is saved successfully.

### 4.6 Server-gone banner (A-F3)
- Markup: `<div id="server-gone" class="notice error" role="alert" hidden>` at the top of `body` (sticky, so it does
  not push the layout), text `"Setup has closed: run the command again and open the new link."` → es
  `"Setup se cerró: vuelve a ejecutar el comando y abre el nuevo enlace."`, plus `<button id="server-gone-retry">Retry</button>`.
- Detection in `api()`: `fetch` rejects (network error), or the reply is not JSON, or 403 with the session-expired
  text → `serverLost(e)`; the thrown error has `gone = true` and a translated message. No caller shows a raw
  `e.message` when `e.gone` (`refresh`, `loadPlan`, `loadTeam`, `loadDashboard`, `action`): the raw "Failed to fetch"
  never reaches the DOM.
- `serverLost`: `gone = true`; show the banner; clear `timer`, `dashboardTimer`; clear every busy button
  (`setBusy(button, false)` for all `PHASE_BUTTONS` and `BUSY_LABEL` ids) so nothing looks stuck; schedule one probe.
- Probe: a single timer, `GET /api/status`, delays `probeDelay(0..5)` = 2, 4, 8, 16, 30, 30 s, then **stops** (7
  failed requests in total, about 90 s). After that only the Retry button and a `visibilitychange` to visible issue one
  probe each. Every other loop (`refresh`, `loadDashboard`, 60 s `autoCheck`, `tickPlanProgress`, the identity retries)
  returns immediately while `gone`.
- `serverBack` (a probe answers 200): hide the banner, `gone = false`, reset the probe counter, `render(data)`.
  A restarted server has a new port and token, so the old tab normally never recovers: the banner is the final state.

## 5. Tests (`kit/.uak/tests/test_setup_resume.py`)

Conventions: same runner shape as `test_setup_feedback.py` (`TESTS`, `--package`, `--case`,
`SETUP_RESUME_RESULT PASS|FAIL failed=N`). Imports: `test_setup_planning as tp`, `test_setup_team as tt`,
`test_setup_feedback as tf`, `test_setup_wizard as wizard`. Server fixtures: `tt.ready_project` (installed, pushed,
approved two-task plan, `Freeze-Epoch: 4102444800`), `tt.fresh`, `tt.Team`, `tt.ready`, `tp.live/post/get/wait_idle`.
Page logic under Node: reuse `tf.NODE_PROGRAM`, `tf.tree`, `tf.page_function`, `tf.script`, `tf.PRELUDE` with a local
`run(sources, scenario)` (do not edit `test_setup_feedback.py`). First source is a shim, evaluated before workspace.js:
it replaces `localStorage` with a real in-memory store (`getItem/setItem/removeItem`, pre-seeded `uak-language`),
defines `window.fetch = (...a) => window.__fetch(...a)` and a counting `console.error`. Sources: shim, workspace.js,
PRELUDE, `el`, `isBusy`, `error`, `api`, the UI-018 block, the UI-019 block. Without Node the scenario returns None,
so **every test also has static/server assertions that fail today**.

### restart_lands_on_the_team_step
Fixture: `target, remote = tt.ready_project(root, tmp)`. Server 1: `tt.ready(srv, target)` (name ana, READY),
`GET /api/team` once (fills `refs/uak/setup-*`). Close it.
1. Real restart: `subprocess.Popen([sys.executable, setup.py, "--no-open", str(target)])` with `UAK_*` stripped; read
   the `UAK SETUP http://127.0.0.1:PORT/#TOKEN` line; `GET /api/status` with the token → `phase != "welcome"`,
   `resume["step"] == "team"`, `human == "ana"`. Terminate. *Today: `phase == "welcome"`, no `resume`.*
2. In process: recording runner wrapping `tt.Team()` (records every command); `srv2 = tp.live(target, runner)`;
   `srv2.open_target()`. Assert: nothing went through the runner (`team.net == []`, no `uak start`), and with
   `origin` re-pointed to a missing path first the call still returns in under 5 s; status has `installed`,
   `checked is False`, `inspect == 1`, `resume == {step: "team", plan_approved: True, kit_on_main: True,
   freeze: 4102444800, human: True, source: "local", ...}` and `len(resume["base_sha"]) == 7`.
   *Today: AttributeError (`open_target`).*
3. Restore origin; `POST /api/check {}` → 202, `wait_idle`; **without** posting `/api/human`:
   `GET /api/team` → 200, `reviewer == "ana-r"`, an `implement` command present. *Today: 400.*
4. `GET /api/plan` → `approved is True`. *Today: KeyError.*
5. A project without the kit: `open_target()` leaves `phase == "welcome"` and writes nothing into the folder.
6. Page: `landing({installed: true, phase: "setup", resume: {step: "team"}}, {})` → `{section: "dashboard", panel: 4}`;
   `resume.step == "prepare"` → `setup`; `planningVisible({installed: true, resume: {plan_approved: true}})` is false;
   static: the boot code calls `landing(` and `journeyStep` reads `resume`. *Today: no UI-019 block.*

### refresh_keeps_the_step_and_values
1. Server: after `tt.ready`, two `GET /api/status` are equal on `target, human, ready, checks, resume, inspect` and
   `checked is True`. *Today: no `checked`/`resume`/`inspect` keys.*
2. Node: `writeSaved("/p/a", {section: "dashboard", drafts: {"schedule-start": "2026-11-20T10:00"}})`, then
   `readSaved("/p/a")` returns it and `readSaved("/p/b")` is `{}`; `landing(data, saved).section == "dashboard"`;
   garbage JSON, `v: 2`, `section: "evil"` and `at` 8 days old each read as `{}`; a saved `dashboard` with
   `installed: false` lands on `setup`; `restoreDrafts` fills the empty `schedule-start` and leaves a non-empty
   `human-name` alone; a draft over 20000 chars is cut.
3. `stepsDone({human: "ana", resume: {freeze: 4102444800, kit_on_main: true, plan_approved: true}})` is all true;
   with `kit_on_main: null` → `publish: false`.
4. Static: `openSection` contains `writeSaved(`; html has `#name-done`, `#schedule-done`, `#publish-done`; a CSS rule
   on `.prepare-step[data-done]` hides the body; catalog has Spanish for "Published on main (commit {sha})." and
   "Plan approved on main (commit {sha})."; `tf.layout_is_stable_across_refresh` still passes (call it).

### name_persists_per_project
Fixture: projects `a`, `b` via `tt.ready_project(root, tt.fresh(tmp, x), name=...)`.
1. Server 1: inspect a, `POST /api/human ana` → body `persisted is True`;
   `realpath(a)/.git/uak-setup/human.json` is `{"version": 1, "name": "ana"}`; `uak-setup` absent from
   `git ls-files` and `git status --porcelain`. *Today: no file, no key.*
2. Server 2 (new): inspect a → `human == "ana"`, `human_source == "project"`; inspect b → post `bob`; inspect a →
   `ana`; inspect b → `bob`. Server 3: inspect b first → `bob`. *Today: "".*
3. Carry-over: server 4, inspect a (`ana`), inspect fresh project c → `human == "ana"`, `human_source == "session"`,
   and c has no `human.json` (inspect never writes).
4. Safety: `human.json` replaced by a symlink to an outside file naming `eve` → inspect reads `""`/session name;
   `uak-setup` replaced by a symlink to an outside folder → `POST /api/human` is 200 with `persisted is False`, a note
   that `tt.translated()`, and the outside folder stays empty; a 5000-byte file, `{"name": "Ana!"}`, `{"name": "ana\n"}`
   and non-JSON are ignored; saving a name leaves an existing `roles.json` byte-identical; a linked worktree of a
   reads `ana`.
5. `tt.ready(srv, d, name=None)` on a fresh project d, `GET /api/team` → 400 **and** `body["need"] == "human"`;
   before any check with a name → 400 and `need == "check"`. *Today: no `need`.*
6. Page: html has `#team-name` and `#team-name-save` inside the `team-step` section; `loadTeam` reads `need`.

### repick_keeps_state
1. `tt.ready(srv, a)`; `before = status`; `POST /api/inspect a` → 200; status has `ready is True`, same `checks` and
   `next_command`, `human == "ana"`, `checked is True`, `inspect == before["inspect"] + 1`.
   *Today: `ready False`, `checks == []`.*
2. Inspect b → `ready is False`, `checked is False`, `checks == []` (never inherited); inspect a → restored.
3. Age it: `srv.checks_kept[key]["at"] -= 601`; inspect a → reset, `checked is False`.
4. No engine run and no network during the re-inspects (recording runner).
5. Node: `shouldAutoCheck({installed: true, checked: true, ...})` false; `checked: false` true, then false for the
   same `target:inspect`, true again after `inspect` grows; false while a phase is busy, with `error`, or `gone`.
6. Static: the `project-form` handler calls `landing(`.

### server_gone_banner
1. Static: `<div id="server-gone" role="alert" hidden>`; catalog maps the English text to exactly
   `"Setup se cerró: vuelve a ejecutar el comando y abre el nuevo enlace."`; `api` calls `serverLost(`; `refresh`,
   `loadDashboard`, `autoCheck` return early on `gone`. *Today: none of these.*
2. Node (es): mark `check` busy; `__fetch` rejects `TypeError("Failed to fetch")`; `await api("status")` rejects with
   `gone === true`; `#server-gone` is visible with the Spanish text; no node's text contains "Failed to fetch";
   `check` is no longer `aria-busy`; exactly one timer is pending.
3. Back-off: advancing through the timers shows delays `[2000, 4000, 8000, 16000, 30000, 30000]`, then no timer;
   fetch was called 7 times in total; `console.error` count is 0; a click on `#server-gone-retry` makes one more call.
4. Recovery: `__fetch` resolves a 200 status → banner hidden, counter reset.
5. A 403 with "This setup session expired…" shows the same banner.

## 6. Out of scope

- A fixed port or any persistence of language/profile/theme across restarts (finding 0.1): file a follow-up.
- Restoring schedule start/end/zone from the repo (only the freeze epoch is stored).
- Rewording the dashboard's next-step card (A-F11's raw `wt new` text); here the page only stops switching tabs by itself.
- Retiring or renaming a reviewer when the name changes; re-planning an approved backlog from the page.
- Any change to `team_context`, `publish_checks`, `approval_checks` gates, or to the engine (`uak start`).
- Server-side auto-check, and any new key on `/api/inspect`.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Local refs are stale (plan reverted, remote reset) | `resume` is a labelled hint; the auto-check and the fresh reads behind every human act decide. `null` is never drawn as done. |
| Two projects in one server | One `state`, but checks kept per target (10 min), name per project with a session fallback, localStorage key per target, `team_cache`/`remote_cache` already keyed by target. Two tabs: `render` re-lands when `data.target` changes. |
| A persisted name breaks an existing test that expects a new server to have no name on a reused repo | None found (`test_setup_team.py:162-169` uses a fresh project). Run the whole suite (`bash .uak/bin/smoke --package-only`); if one appears, report it, do not edit it. |
| Re-pick keeps a READY line that went stale | 10-minute cap; the team view already says "claimed since the last check"; the 60 s beginner check continues. |
| Windows paths | Compare targets with `os.path.normcase` on resolved paths; the page compares the exact `state.target` string the server sent; `write_atomic` is already used for `roles.json` there; the subprocess test uses `sys.executable` and `terminate()`. macOS: physical paths (`/private/var`), as `tt.physical`. |
| Name changed later | The file is overwritten; `team_cache` is keyed by name; the old `NAME-r` stays registered on claims and the page shows the new one as not registered (no automatic retire). |
| Stale or hostile localStorage | Versioned key, 7-day expiry, enum check on `section`, size caps, `textContent`/`value` only, server truth wins on the step; storage is per port, so old entries are simply orphaned. |
| Slow-lane contention on landing | Check is posted before any GET that probes; `project_progress` uses local Git only, 10 s per call, outside the lock. |
| Layout jumps (UI-018) | Landing and done rows are applied before `data-loading` is lifted; the banner is sticky; auto-check moves no focus and opens no section. |
| Repo rules outside Paths | `setup.py`, `setup.html`, `workspace.js` are installer-placed: `python3 scripts/kit_hashes.py` updates `kit/.uak/settings/known-files.txt`; a new rule needs a `WHY.md` line. Both files are outside the task's Paths: ask the lead to extend Paths before shipping. `python3 scripts/kit_lint.py` must stay green. |
