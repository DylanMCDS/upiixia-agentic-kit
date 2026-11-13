# Test rounds · kit main 6f31689 · 2026-11-13 (cafeteria copies, local bare remotes, real Claude Code/Codex)

| Round | Who | Goal reached | Report |
|---|---|---|---|
| r1 | Novice "Luis", browser, Spanish, no context | Partial: plan created by real Claude (7 tasks), HACK-001 claimed, implementer wrote tests, stopped asking approvals; reviewer idle (FREEZE after the usage-limit pause) | r1-REPORT.md · video ~/Movies/uak-pruebas-2026-11-13/ronda1-novato-navegador.mp4 |
| r2 | Novice "Valeria", README/terminal, no context | Yes, with friction (terminal path) | r2-REPORT.md |
| r3 | QA with context, real tools | Most items PASS; agents stopped on permissions | r3-REPORT.md · video ronda3-con-contexto.mp4 |
| r4 | Adversarial with context | 1 P1, 5 P2, 9 P3; protections held | HANDOFF.md (night section) · video ronda4-adversarial.mp4 |

## Cross-round findings, ranked (candidates for the next backlog; Dylan decides)
1. P1 · Agents in a NEW folder: Claude Code ignores .claude/settings.json allow rules until the folder is trusted interactively
   ("workspace has not been trusted") → headless planner can fail on its first command (r3 run 1), implementers stop asking approvals (r1, r3),
   README never says "open claude once and accept trust" (r2). Fix: say it in the page/README + detect the line; planner reads with Read.
2. P1 · setup.py state["reviewer"] is server-wide: wrong "registered" for another project/name/after retire (r4).
3. P2 · Codex reviewer command needs `--add-dir "<repo>/.git"` (wt recommends it) / workspace-write (r1, r3).
4. P2 · Network git under the server lock blocks /api/status (r4); offline team step says "publish the kit" (r4, PENDING #40).
5. P2 · After the first claim the page leaves "ready" and the team commands vanish (r4) / keeps offering the claimed task (r3).
6. P2 · Failed planning shown as a passing plan (r3). Planning ~4-8 min with no progress cue (r1).
7. P2 · Event schedule defaults to today; saving it untouched freezes a next-day hackathon silently (r1).
8. P2 · Identity heuristic: one word suppresses the warning (git ok, gh someone else) (r4); accents (PENDING #44).
9. P2 · GitHub repo created with .gitignore → publish advice "git pull" is a dead end (r4).
10. P3 · Spanish leftovers: status heading, doctor sub-lines, weekday, claim progress line, "No technical output yet"; Approved-By vs
    Published-By names differ; reviewer offered implementation work by uak next; "20770 d" for never-seen humans; terminal-path
    setup registered example reviewers ana/leo (r2).
