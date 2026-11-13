# UI-006 — Windows Git Bash prompt check

- Date: 2026-11-12
- Branch / SHA checked: `origin/feat/ui-006` @ `57b397d` (PR #16)
- Shell: Git Bash — `GNU bash, version 5.3.15(2)-release (x86_64-pc-cygwin)`
- `uname -a`: `MINGW64_NT-10.0-26200 DESKTOP-0U931LO 3.6.10-5a1665c8.x86_64 2026-09-28 10:40 UTC x86_64 Msys`
- `claude --version`: `2.1.322 (Claude Code)`
- `codex --version`: `codex-cli 0.167.1`
- Native Python used: `py` (Python 3.13.7). `python` on this machine is the Microsoft Store alias stub (exit 49, not installed), so the step used `py` as instructed.
- All commands run from `kit/`.

## Step 2 — what a native Windows program receives — PASS

Command (both setup-page prompts, single-quoted, as copied):

```
py -c "import sys; print(sys.argv[1:])" 'Run /uak-start for APP-001. Work only in this worktree.' 'You are the reviewer dylan-r. Run bash .uak/bin/uak next; when it names a task to review, run $uak-review with that task ID. Never write code for a task.'
```

Exact output:

```
['Run /uak-start for APP-001. Work only in this worktree.', 'You are the reviewer dylan-r. Run bash .uak/bin/uak next; when it names a task to review, run $uak-review with that task ID. Never write code for a task.']
```

Both strings identical. `/uak-start` was NOT rewritten by MSYS path conversion; `$uak-review` was not expanded.

## Step 3 — Claude Code (`--model haiku --max-turns 2 --permission-mode plan`) — PASS

Process exit 1 = `error_max_turns` (expected with `--max-turns 2`). Key lines:

- `system/init`: `"uak-start"` present in `slash_commands` (True).
- assistant tool_use: Glob `.claude/commands/uak-start*` -> result `.claude\commands\uak-start.md`
- assistant tool_use: Read `kit\.claude\commands\uak-start.md` -> `description: Use at the start of a session with no task in hand: take the next task (uak next) and get its worktree ready, claim included.`
- final: `result error_max_turns`, num_turns 3.

The prompt reached Claude Code intact and the model recognised `/uak-start` and opened its command file.
Observation (not a failure): init reported `claude-haiku-5-5`, but the assistant messages carry `"model":"claude-sonnet-5-5"`.

## Step 4 — Codex (`codex exec -s read-only`, `UAK_AGENT=dylan-r`) — PASS

Process exit 0. Key lines:

- `user` echo: `You are the reviewer dylan-r. Run bash .uak/bin/uak next; when it names a task to review, run $uak-review with that task ID. Never write code for a task.` (intact, `$uak-review` unexpanded)
- `codex`: `I'll run uak next as reviewer dylan-r and follow the review instructions for the task it selects.`
- exec: `$env:UAK_AGENT='dylan-r'; bash .uak/bin/uak next` -> exited 1: `.uak/bin/uak: line 104: ../.git/uak-blackbox.calls: Permission denied` / `GIT_ERROR: Cannot create temp dir.` (read-only sandbox — expected)
- exec (skill lookup) resolved `C:\Users\dylan\uak-win-check\kit\.agents\skills\uak-review\SKILL.md` and read `.claude/commands/uak-review.md`.
- final: `No review task was returned, so I couldn't start $uak-review. No code was changed.`

Codex acted as dylan-r, located the `uak-review` skill, and wrote no code. It could not go further because `uak next` needs write access (sandbox), so the actual review flow was not exercised.

## Verdict

| Step | Result |
|---|---|
| 2 — native argv | PASS |
| 3 — Claude Code | PASS |
| 4 — Codex | PASS (skill located; flow stopped by read-only sandbox, expected) |
| **Overall** | **PASS** |
