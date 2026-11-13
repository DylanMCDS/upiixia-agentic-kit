# QA round 3 · kit main 6f31689 · with context, real Claude Code + Codex (saved by claude-Dylan from the agent's reply)

PASS: UI-005 (name once, schedule → Freeze-Epoch, publish 547 files without IDEA/TASKS/OWNERS, terminal box, plan only after kit on main),
planning with the real planner (2nd run: 6 tasks, 256 s), typed approval (placeholder + Spanish hint), READY, register luis-r (+ second
click: no commit), UI-007 journey + focus moves, identity warning (carla → warning; luis → none), UAK_HUMAN empty in both agent shells,
session-start 0.69–1.10 s, kit_lint 0, CI once per SHA, test_v3 13/13, test_tokens_coverage 7/7.
PARTIAL: Terminal 1 (claimed HACK-001 as claude-luis in the right worktree; agent stopped: workspace not trusted), Terminal 2 (codex exec
read-only sandbox could not write .git), Spanish gate lines (status heading and doctor sub-lines English).

## Bugs
- P1-1 Headless Claude Code in a new folder ignores .claude/settings.json allow rules ("workspace has not been trusted"); the planner's
  first Bash read is denied and the prompt says stop → run 1 wrote no TASKS.md (26 s). Run 2 worked. Same trust issue stopped the
  implementer. Fix: planner reads with the Read tool and treats a denied read as non-fatal; detect "not been trusted" and tell the person
  to open Claude Code once in the folder (accept trust). (Round 2 found the same; README never says it.)
- P2-1 A failed planning run shows as planned: "The planner did not write .uak/TASKS.md" (English) inside the "changed things only you can
  change" box, a green "plan passes uak lint" with no TASKS.md, approve button present (frame 0016).
- P2-2 Terminal 2's codex command lacks `--add-dir "<repo>/.git"` that wt itself recommends; under codex exec uak next fails
  ("Operation not permitted"). Interactive codex untested.
- P3-1 #result-title uses t() not gate(): status heading English and ✓ icon even with TODOs; doctor sub-lines English.
- P3-2 Advanced dashboard progress line from claim.sh:63 ("N commit(s) since the claim · last: …") English.
- P3-3 Schedule confirmation weekday "Fri" English.
- P3-4 Agents tab: human "20770 d" (epoch 0); reviewer luis-r not listed.
- P3-5 Team step keeps offering `wt new HACK-001` after the claim.
- P3-6 `UAK_AGENT=luis-r uak next` offers implementation work to the reviewer identity.
- P3-7 Plan commit Approved-By uses the Git name; kit commit Published-By uses the human name.

Quota: 3 Claude runs (2 planner, 1 implementer), 1 Codex run. Nothing pushed to GitHub. Files: frames/ (0001–0040) + captions.txt,
agent-*.log, env-t*.txt, advanced-*.txt, drive.py, t1.sh, t2.sh.
