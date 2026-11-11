# UI-004 design draft (claude-Dylan; from ui004-headless-research.md, docs checked 2026-11-10)

## Harnesses offered
- Claude Code and Codex only, when installed AND logged in (`claude auth status`, `codex login status`, exit 0).
- Gemini and Cursor: shown as "not supported for planning yet" with the reason (headless Gemini cannot run shell
  commands; Cursor needs --force/--yolo to write). Revisit when their docs change.

## Fixed argv (cwd = project root, stdin = DEVNULL, shell=False, no user text)
- Claude: `claude -p <PLANNER_PROMPT> --permission-mode acceptEdits --allowedTools "Bash(bash .uak/bin/uak graph *)"
  "Bash(bash .uak/bin/uak lint *)" "Bash(bash .uak/bin/uak clock *)" --disallowedTools "Bash(git commit *)"
  "Bash(git push *)" "Bash(git add *)" "Bash(bash .uak/bin/uak plan *)" "Bash(bash .uak/bin/uak done *)"
  "Bash(bash .uak/bin/uak merge *)" "Bash(bash .uak/bin/wt *)" mcp__uak --output-format stream-json --verbose
  --max-turns 60` (+ the same rules with a PowerShell(...) prefix on Windows).
- Codex: `codex exec --cd <root> --sandbox workspace-write --json <PLANNER_PROMPT>` (.git read-only, no network).
- PLANNER_PROMPT is a constant (no `% ^ & | < > "`): run /uak-plan steps 1-3 from IDEA.md, write .uak/TASKS.md and
  .uak/OWNERS.md, run uak graph and uak lint, then stop; never set Backlog-Approved, never git add/commit/push,
  never run uak plan.

## Server-side verification after the agent exits (the real guarantee, harness-independent)
- HEAD unchanged; only .uak/TASKS.md and .uak/OWNERS.md changed (snapshot hashes of PROJECT.md and the rest before
  the run); Backlog-Approved not newly set; the server itself runs `uak lint` and requires LINT_OK.
- Any violation: discard nothing silently; show what changed and refuse approval until the human resolves it.

## Approval (human, in the UI)
- Two steps: review cards, then type the project name. Sets Backlog-Approved: yes, commits exactly IDEA.md,
  .uak/TASKS.md, .uak/OWNERS.md, .uak/PROJECT.md with the local Git identity ("approved by <name> in local setup"),
  pushes to the base. Refuses on failing lint, other staged files, or a rejected push, with the recovery.

## Open risks to confirm in the red phase
- `$uak-plan` inside `codex exec`; exec behavior when a command needs approval; exit codes.
- `uak lint` with .git read-only and no network (Codex sandbox).
- uak-plan.md pins `model: opus` (cost); the Stop hook may hold the end of a run on unread inbox messages.
