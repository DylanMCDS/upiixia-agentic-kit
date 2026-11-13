# Round 1 report: Luis, cafeteria virtual queue (wizard path)

## Timeline (container clock)
- 00:28 `install.sh --wizard ... --no-open` prints address. 00:29 Spanish selected, project path typed, Hackathon + Claude Code + Codex, install (about 10 s).
- 00:30 name "luis", schedule saved untouched, kit published to main (547 files), idea saved, plan requested.
- 00:30-00:38 plan drafted by Claude Code (about 8 min). 00:39 plan approved/published (7 tasks), reviewer luis-r registered, HACK-001 claimed via page command (`wt new`).
- 00:40 Claude agent run: hit 5-hour usage limit (owner quota; not a kit issue). Codex reviewer run: failed, read-only sandbox.
- 04:03 (after limit reset) Claude re-run: lease had expired; asked to approve `uak status`. Luis ran it himself. 04:06 re-run: Claude wrote tests/stubs (app/, tests/ untracked in worktree), then stopped asking approval for `uak red`. Codex reviewer: `uak next` answered FREEZE.

## Goal
PARTIAL. HACK-001 is claimed (dashboard: 1 "En curso", 0 / 7 done) and the agent started (stubs + tests written), but it never got past `uak red` (headless acceptEdits blocks the Bash it needs; 12-turn cap). The reviewer is registered but idle with FREEZE, because the event window (saved as default "today 01:00-04:00") had ended by the time the quota reset; this is partly a test artifact.

## Frictions
1. HIGH: Event schedule defaults to today (01:00-04:00, 3 h from "now"), while Luis's hackathon is tomorrow. Saving untouched produces "El trabajo nuevo se detiene a las Fri 03:30; toma la primera tarea antes de las Fri 01:20" and later a frozen project ("Los cambios del proyecto están congelados"). Nothing says "this is today's date, change it". Also "Fri" is English inside the Spanish UI.
2. HIGH: After the plan, the agent flow needs real terminals with interactive approvals (MCP trust prompts etc.). In headless-style runs the agents stall on permissions ("approve uak red / uak status"). Luis has no hint on what to do when an agent asks for approval or says "lease expired / recovery token".
3. HIGH: Codex reviewer in `exec` mode: "el entorno de solo lectura impide escribir registros en .git" (exact page command; interactive codex may differ, the page's own Codex hint mentions `--add-dir .git` only in `wt` output, not in the page command). Retry with `-s workspace-write --add-dir .git` worked.
4. MEDIUM: Wizard did not prefill the project path although Luis passed it on the command line ("Elige la carpeta..." empty field).
5. MEDIUM: Plan creation takes about 8 min. Only a dimmed button, a top banner "Hay una operación en curso" and "Detalles técnicos" => "No technical output yet." (English). Luis can't tell it is working vs stuck. Technical details also keep saying "TODO 5. a plan: no tasks yet ... run /uak-plan" while a plan is already drafted (stale).
6. MEDIUM: After "Publicar el kit en main" the panel collapses silently; no "Publicado" confirmation visible.
7. MEDIUM: Plan and task titles are English in a Spanish UI; 7 tasks incl. landing page and demo video for 2 people / 3 h feels heavy. Team-size default is 3 though Luis said 2 (he had to change it).
8. MEDIUM: Commit identity shown as "Luis Estudiante 1 <luis1@example.invalid> ... pull requests se abrirán como @DylanMCDS" (taken from the machine; confusing/alarming for a new user, leaks the gh account name). Test-env artifact but a real novice would be unsure.
9. LOW: Commands contain `UAK_HUMAN=` with an empty value next to `--human luis`; looks like a bug/forgotten name.
10. LOW: "La tarea que sugirió la última comprobación ya no está disponible." after claiming; unclear. "Terminal 1: ... en cualquier carpeta" then the command cd's anyway.
11. LOW: "Soy la única persona en este repositorio" checkbox label reads oddly with 2 people; Luis left it unchecked (correct) but the reviewer name concept (luis-r) is unexplained for a friend who will join.
12. LOW: Agent warned `uak pace` critical (codex 7d 99% used) and untrusted workspace ignoring 51 allow entries in headless runs.

## Errors
- Claude: "You've hit your 5-hour limit" (quota). Later "lease is expired ... not allowed to read the recovery token".
- Codex #1: `uak next` failed, read-only sandbox. Codex #2: FREEZE.
- No crashes in the page itself.

## What the agents did
- Planner (Claude, 8 min): drafted 7 tasks HACK-001..007 (server+contract, design lock, queue engine, student screen, staff screen, landing, demo) with Tests per task; uak lint passed.
- Claude implementer: claim HACK-001 via `wt new`; then wrote tests/test_server.py with the six named tests and stubs (app/server.py, contract.py, api_mock.py); stopped before `uak red` awaiting approval.
- Codex reviewer luis-r: nothing to review; first run could not write .git, second reported FREEZE.

## Suggestions
Prefill schedule with a date picker choice (today/tomorrow) and warn when the window is short or in the past; localize day names and technical-details strings; add progress text/elapsed time during planning; confirm publication; prefill project path; explain what to do on agent approval prompts and expired leases; give the Codex command the sandbox flags; explain `luis-r` and the 2nd person's role (friend's setup).

Logs: agent-claude*.log, agent-codex*.log; frames: frames/ (38 PNG + captions.txt).
