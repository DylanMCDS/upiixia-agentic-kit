# Round A · novice "Luis", Spanish UI, real Claude planner and agents · kit 4df3acb · saved by the lead from the tester's reply

Journey: install 7 s, publish 1.5 s, real planner 4m30s (7 tasks, lint clean), approve 5 s; team step blocked twice (~20 min lost) by F1/F2; register luis-r 1.5 s; implement command claimed FILA-001, headless agent did red→green→push, stopped before /uak-ship. Evidence: A/shots/ (58), A/*.log, A/*.jsonl, A/workaround/.

Worked: out-of-order clicks explained (toast + Ir ahí), exact-name approval, second tab shows running plan, copy buttons, no overflow at 390, no page JS errors.

| ID | Sev | Finding | Fix |
|---|---|---|---|
| F1 | P1 | A newer kit release (6.3.0 vs 6.2.0) is a TODO in `uak start` → never READY → team step hidden; the only way out points at ~/.uak-kit (another clone); UAK_KIT_PIN can't pass because setup strips UAK_*. | Update = NOTE in setup, or "Seguir con esta versión" button that pins. |
| F2 | P1 | After a server restart the name is forgotten; in READY the name field is hidden, /api/team 400 and the team step silently hidden; "Atrás" loops. | Persist the human name per project; show the name field in the team step on that 400. |
| F3 | P2 | Server stopped → raw English "Failed to fetch", endless polling (~250 errors); new port/token after restart, old tab can't recover. | Spanish banner "rerun the command and open the new link"; back off polling. |
| F4 | P2 | After restart, Prepare steps look undone (schedule empty, step 3 "Primero guarda tu nombre" though the kit is on main). | Derive step state from the repo; mark "Hecho". |
| F5 | P2 | The version TODO becomes the page H1 after a refresh, with an English `git -C ~/.uak-kit pull` command. | Never promote maintenance to the headline. |
| F6 | P2 | Claude Code trust dialog defaults to "No, exit" + English "51 permissions" warning; page only says "acepta (sí)"; untrusted implementer stopped before shipping; untrusted planner completed (contradicts the page's text). | Say "press ↓ then Enter"; explain the warning; detect trust (~/.claude.json) and show ✓/✗. |
| F7 | P2 | Each "Comprobar siguiente paso" clears and redraws the list: height 4933→3919→4933, button jumps 1014 px. | Keep the old list dimmed until the new result. |
| F8 | P2 | After publishing, step 3 shows only "Listo a las 00:37." and "Revisar los archivos" stays. | "Publicado en main (commit …)", step done. |
| F9 | P2 | Dashboard lists tasks with open dependencies as "Disponibles". | "Bloqueada por X". |
| F10 | P2 | English in Spanish UI: "the kit's GitHub", update command, reviewer NOTE, "Failed to fetch", IDEA.md headings, plan titles/tests, "Nada que probar primero: no (static …)". | Translate engine lines; planner writes in the idea's language. |
| F11 | P2 | On READY the page switches itself to "Panel del proyecto", whose next step is raw `wt new FILA-001` (skips reviewer registration) and says "Usa Arranca tu equipo, arriba" (other tab). | Dashboard's next step opens the team step. |
| F12 | P3 | 3 h / 2 people → 7 P0 tasks incl. a human "design lock" and a landing. | Scale task count to event × team; avoid human-gated tasks in short sprints. |
| F13 | P3 | Schedule inputs overlap 8 px at 1280. | min-width:0 on grid children. |
| F14 | P3 | 0 px gap above "Guardar la idea". | Standard field gap. |
| F15 | P3 | Block reason shown 3 times; toast closes after 8 s. | One inline reason + toast. |
| F16 | P3 | Two 1–5 numberings at once (journey and wizard rail). | Hide the wizard rail after install. |
| F17 | P3 | Planning progress shows long absolute paths. | Relative paths. |
| F18 | P3 | 532 files committed incl. the kit's own tests and motionsites examples. | Don't ship kit tests into projects. |
| F19 | P3 | With 2 people the teammate is never addressed. | Explain who runs what with two humans. |
| F20 | P3 | One control has three labels. | One label. |
