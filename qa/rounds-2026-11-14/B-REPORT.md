# Round B · returning user and real repo cases · kit 4df3acb · saved by the lead from the tester's reply

Setup: read-only copy of turno-cafeteria-2 (remote HEAD → claims), odd-name projects with GitHub-like unrelated remotes, a teammate clone, a hanging origin; fake HOME pinning the kit's GitHub to v6.2.0 for most runs. Evidence: B/shots/, B/out/*.json, B/server-*.log.

Passed: spaces/accents in paths end to end, install, publish, reviewer registration, integrate, dashboard counts with hand-made states, no 390 overflow, no page errors, no state leaks between two projects, fast DNS-failure report.

| ID | Sev | Finding | Fix |
|---|---|---|---|
| B-01 | P1 | Clone of a remote whose HEAD is `claims` installs the kit on `claims`; check sends user to schedule; only publish says (English) "git switch main"; no warning that the default branch is claims. | Refuse/warn in inspect+install when HEAD ≠ UAK_BASE; warn when remote default branch is claims. |
| B-02 | P1 | "update the kit 6.2.0 → 6.3.0" blocks every check; Repair installs the server's own version; engine() refuses a project newer than the server until restart; UAK_KIT_PIN stripped. | NOTE during an event or "seguir con 6.2.0" button; hint to restart setup after updating. |
| B-03 | P1 | After the way-out `git pull`, publish refuses in English with no command; a `git push origin main` is needed. | Add the push step to the way-out; translated refusal with the exact command. |
| B-04 | P2 | Returning approved project lands on Prepare with empty forms, publish offer and "Crear el plan" enabled; team only after a manual check (~30 s). | Auto-check after inspect; collapse finished steps; hide plan creation when approved. |
| B-05 | P2 | Re-picking the same project loses its check. | Keep last check per project or re-run it. |
| B-06 | P2 | Frozen project shows "Tu equipo está trabajando". | FREEZE = frozen in team_phase/guidance. |
| B-07 | P2 | Merge needing a human not in setup's next step; reason raw English with absolute log path. | Needs-human first in guidance(), Spanish, no path. |
| B-08 | P2 | Offline dashboard shows local plan with everything available, ignoring known claims. | Fall back to last dash-claims ref, marked stale. |
| B-09 | P2 | "El comando de abajo…" shown without a command. | Only when a command exists. |
| B-10 | P2 | Hanging remote: check 75 s, every view 409 meanwhile. | NET_TIMEOUT + low-speed limit in ls-remote; stale dashboard during the check. |
| B-11 | P3 | English leftovers (kit's GitHub, FREEZE line, git ls-remote hint, CLAIMED, "ofrecida a all", human, smoke reason, publish refusals, reviewer.message). | Translate engine phrases, map tokens. |
| B-12 | P3 | Plural labels on single rows; "primera tarea" after the first was claimed. | Singular; "siguiente tarea". |
| B-13 | P3 | Dependency-blocked counted as available; approved review has no mark. | "Esperando dependencias" bucket; "aprobada" badge. |
| B-14 | P3 | Reload switches dashboard tab to the Configuration ready card (bare wt new, no reviewer step). | Keep the active tab. |
| B-15 | P3 | "Tu siguiente paso" cramped under "Tu app" (advanced). | Card. |
| B-16 | P3 | quotable() rejects `'` though shell_quote handles it. | Allow `'`. |
