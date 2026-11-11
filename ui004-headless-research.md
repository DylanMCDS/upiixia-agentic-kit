# UI-004 research: running /uak-plan headless from the setup UI

Docs checked on 2026-11-10. Local versions seen on this machine: Claude Code 2.1.322 and codex-cli 0.167.1. `gemini` and `cursor-agent`/`agent` are not installed here, so nothing about them was tested locally.
Anything marked **UNVERIFIED** was not confirmed in the official docs.

## 0. Findings that change the design (read first)

1. **Claude `-p` ignores the project's `permissions.allow` until the folder is trusted.** The kit's `.claude/settings.json` allows `Bash(bash .uak/bin/uak:*)`, `git add`, `git commit` and `mcp__uak`. In a `claude -p` run, in a folder nobody trusted interactively, none of those allow rules apply. Claude prints "this workspace has not been trusted" to stderr. Deny and ask rules, hooks, the `env` block, `.mcp.json` servers and a skill's `allowed-tools` **do** still apply. Once the folder *is* trusted (the user opened `claude` there before), all of those allows apply, including `git commit` and `mcp__uak`. The fixed argv therefore has to (a) grant what the planner needs through CLI flags and (b) deny commit, push and `uak plan` through `--disallowedTools`, because a deny beats an allow from any level. Source: https://code.claude.com/docs/en/permissions ("Project allow rules and workspace trust", "What runs before you trust a folder").
2. **Codex `workspace-write` makes `.git`, `.agents` and `.codex` read-only and turns network off by default.** So `git commit` and `git push` cannot succeed inside the sandbox. That is a useful hard guarantee for "never commit/push". It also means `uak graph`'s `git fetch <remote> claims` fails. The fetch is guarded (`if git fetch …`), so graph falls back to local TASKS.md. Whether `uak lint` needs any write to `.git` or the network was not checked: **test it**. Project `.codex/` layers (config.toml, hooks.json, rules) load only when the project is trusted, and hooks also need per-hash hook trust. In a fresh project, the kit's Codex guard hooks most likely do **not** run under `codex exec`.
3. **Gemini headless cannot run shell commands without extra policy.** `run_shell_command` defaults to `ask_user`, and in non-interactive mode `ask_user` is treated as `deny`. Workspace policies (`.gemini/policies`) are **disabled**, so the project cannot grant it. Also, Gemini CLI **stopped serving Google AI Pro/Ultra and free individual users on 2026-06-18**. It only works with paid Gemini API keys or Enterprise, and the replacement is Antigravity CLI.
4. **Cursor's headless docs say file writes require `--force`. `--yolo` is an alias of `--force`, so this is the bypass flag.** Without it, "changes are only proposed, not applied". Another Cursor page says "Cursor has full write access in non-interactive mode". The docs contradict each other, so this is UNVERIFIED either way. As documented, Cursor cannot meet "edits allowed, no bypass flag".
5. **Recommendation for all four harnesses:** the UI server runs `bash .uak/bin/uak graph` and `bash .uak/bin/uak lint` itself after the agent exits, and checks that TASKS.md and OWNERS.md exist and that `git status` shows no commit. The agent is *asked* to run them, but the UI does not depend on it. This removes the need to allow any shell command in Gemini and Cursor.

## 1. What the kit already configures (worktree ui-001, `kit/`)

| Harness | Command/skill the planner uses | Permissions / trust as shipped | Hooks |
|---|---|---|---|
| Claude | `.claude/commands/uak-plan.md`. Frontmatter has `model: opus` and **no** `allowed-tools`. Steps 4 (set `Backlog-Approved`) and 5 (commit `plan: backlog v1`, push to main) are in the body. | `.uak/settings/settings.{sprint,marathon}.json` is installed as `.claude/settings.json`. allow: `Bash(bash .uak/bin/uak:*)`, `git add/commit`, `git push origin feat/*`, `mcp__uak`, and more. deny: force push, `git push origin main:*`, `gh pr merge`, `.env` reads, and more. Marathon adds ask rules (`npm install`, `curl`, `WebFetch`, and others). | SessionStart, UserPromptSubmit (`guard prompt`, a secret scan), PreToolUse Bash/PowerShell (`guard bash claude`), PostToolUse tick/output, **Stop (`hook stop` blocks ending the turn once per batch of unhandled inbox messages)**, SessionEnd. `.mcp.json` declares the `uak` MCP server. |
| Codex | `.agents/skills/uak-plan/SKILL.md` (generated, `disable-model-invocation: true`) plus `agents/openai.yaml` `policy.allow_implicit_invocation: false`, so explicit `$uak-plan` is required. | `.uak/settings/codex.{mode}.toml` is installed as `.codex/config.toml`: model, `[agents]`, `[mcp_servers.uak]`. **No sandbox_mode, approval_policy or `.codex/rules`.** | `.codex/hooks.json`: SessionStart, UserPromptSubmit, PreToolUse guard, PostToolUse, Stop, and others. |
| Gemini | `.gemini/commands/uak-plan.toml` (generated; `prompt` has **no `{{args}}`**). | `.gemini/settings.json`: hooks plus `mcpServers.uak` (`trust: false`). **No policies.** | SessionStart, BeforeTool `run_shell_command` guard/wrap, AfterTool, SessionEnd. |
| Cursor | `/uak-plan` from `.agents/skills` (per `.cursor/rules/uak.mdc`). | **No `.cursor/cli.json`** (no CLI permissions). `.cursor/mcp.json` has uak. | `.cursor/hooks.json`: beforeShellExecution guard, preToolUse wrap, beforeSubmitPrompt, stop, and others. |

## 2. Constant planner prompt (same text for all four)

Each harness gets the text below with its own prefix: Claude `/uak-plan `, Codex `$uak-plan `, Gemini `/uak-plan `, Cursor `/uak-plan `.
The text avoids `% ^ & | < > "` and backticks, so it survives a Windows `.cmd` shim (see section 7). In argv it is a single element and is never passed through a shell.

```
HEADLESS RUN started by the kit setup UI. Nobody can answer questions or approve prompts: never ask, decide and note assumptions in TASKS.md. Do only steps 1 to 3 of the plan script: write .uak/TASKS.md and .uak/OWNERS.md, then run bash .uak/bin/uak graph and bash .uak/bin/uak lint and fix the backlog until lint prints LINT_OK. Do NOT do steps 4 and 5: never set Backlog-Approved, never run git add, git commit or git push, never run uak plan, uak deploy or any wt command, and edit no file other than .uak/TASKS.md and .uak/OWNERS.md. If a command is denied, do not retry it: stop and report. Finish by printing the one-screen table of step 4 so the human can review it in the UI.
```

How each harness passes this text to the command:
- **Claude:** documented. If the skill has no `$ARGUMENTS` placeholder (uak-plan.md has none), Claude Code appends `ARGUMENTS: <input>` to the skill content, so the override reaches the model. Source: https://code.claude.com/docs/en/skills
- **Gemini:** the kit's TOML has no `{{args}}`. How Gemini handles arguments for a command without `{{args}}` is **UNVERIFIED**. I did not fetch that section, but I recall it appends them.
- **Codex and Cursor:** the text follows the skill mention in the same prompt.
- **Weak point everywhere:** the override competes with steps 4 and 5 in the skill body. The real guards are the deny rules and the sandbox, not the prompt.

## 3. Claude Code CLI (`claude`)

Sources: https://code.claude.com/docs/en/headless · https://code.claude.com/docs/en/cli-reference · https://code.claude.com/docs/en/permissions · https://code.claude.com/docs/en/permission-modes · https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/setup

| Item | Finding |
|---|---|
| Headless syntax | `claude -p "<prompt>" [flags]`. Exit 0 on success and non-zero on failure. An invalid flag errors to stderr before the run. A failure inside the run (for example missing auth) is printed **as the result on stdout**. SIGTERM gives exit 143 and records no result. SIGINT ends the turn cleanly. |
| Slash commands / skills | Documented: "User-invoked skills and custom commands work. Include `/skill-name` in the prompt string and Claude Code expands it before running." `.claude/commands/*.md` files are equivalent to skills. `--bare` skips commands, skills, hooks and CLAUDE.md, so **do not use `--bare`**. `--disable-slash-commands` turns them off, so do not use that either. |
| Permissions in `-p` | Since v2.1.302, `-p` starts in Manual (`default`) mode when nothing sets a mode. A call that needs approval is **denied** unless an allow rule, a hook, or `--permission-prompt-tool` approves it. `--permission-mode acceptEdits` approves file writes plus `mkdir touch rm rmdir mv cp sed` inside the working directory. Protected paths (`.git`, `.claude`, `.mcp.json`, …) still prompt, which means they are denied in `-p`. `.uak/` is not protected. Other shell commands need `--allowedTools` or `permissions.allow`. `--permission-prompts none` (v2.1.259+) denies anything left over and tells Claude not to retry. Rule syntax: `Bash(cmd *)` and `Bash(cmd:*)` are equivalent prefix forms. Compound commands (`&&`, `;`, `\|`, …) need every part allowed. Deny and ask rules apply to any subcommand. Deny beats allow at every level, and CLI `--disallowedTools` adds to the deny list. |
| Trust caveat | See section 0, point 1. Project `permissions.allow` is ignored in `-p` until the folder is trusted. Hooks, `env`, `.mcp.json` servers and skill `allowed-tools` are used either way. To keep repo content out, docs suggest `--setting-sources user` or `--bare`. We need the project's commands and hooks, so do neither. |
| Install / auth detection (no side effects) | `claude --version` prints `2.1.322 (Claude Code)`. `claude auth status` prints JSON (`--text` for human-readable output) and **exits 0 if logged in, 1 if not**. `authMethod` is one of `none`, `claude.ai`, `oauth_token`, `api_key`, `api_key_helper`, `third_party`. `claude doctor` prints read-only diagnostics. |
| Output / streaming | `--output-format text\|json\|stream-json`. stream-json needs `--verbose`. `--include-partial-messages` adds token deltas. The first event is `system/init`, unless SessionStart hook events (`hook_started/progress/response`) come first, which they will with the kit's hooks. Events: `system/api_retry`, `assistant`/`user` messages with `parent_tool_use_id`, and a final `result` line with result text, `total_cost_usd`, `session_id`, `permission_denials`. With `--permission-prompts none`, denials stream as `permission_denied` system messages. |
| Windows | Native `claude.exe` lives in `%USERPROFILE%\.local\bin`, so `subprocess` can launch it directly. The npm install is the same native binary. The Bash tool needs Git for Windows (`CLAUDE_CODE_GIT_BASH_PATH` if it is not found). Without Git Bash, Claude uses the **PowerShell tool**, so Bash rules do not match and you need `PowerShell(bash .uak/bin/uak graph *)` rules as well. Rule paths are normalized to POSIX (`//c/...`). |

**Recommended fixed argv.** Run it with cwd set to the project root and stdin set to DEVNULL:

```
["claude", "-p", "/uak-plan <CONSTANT TEXT>",
 "--permission-mode", "acceptEdits",
 "--allowedTools", "Bash(bash .uak/bin/uak graph *)", "Bash(bash .uak/bin/uak lint *)", "Bash(bash .uak/bin/uak clock *)",
 "--disallowedTools", "Bash(git commit *)", "Bash(git push *)", "Bash(git add *)", "Bash(bash .uak/bin/uak plan *)", "Bash(bash .uak/bin/uak done *)", "Bash(bash .uak/bin/uak merge *)", "Bash(bash .uak/bin/wt *)", "mcp__uak",
 "--permission-prompts", "none",
 "--output-format", "stream-json", "--verbose",
 "--max-turns", "60"]
```

Notes on this argv:
- Put the prompt right after `-p`. `--allowedTools` and `--disallowedTools` take several values, so a prompt placed after them could be read as another rule.
- Whether `Bash(x *)` also matches a bare `x` with no arguments is **UNVERIFIED**. If needed, also add `Bash(bash .uak/bin/uak graph)` and `Bash(bash .uak/bin/uak lint)`.
- On Windows without Git Bash, add the same rules with the `PowerShell(...)` prefix.
- `mcp__uak` is denied because, in a trusted folder, its `uak_cli` tool would give the model an unrestricted route to any uak command.
- An alternative to the `--allowedTools` entries is to add `allowed-tools: Bash(bash .uak/bin/uak graph *) Bash(bash .uak/bin/uak lint *)` to `kit/.claude/commands/uak-plan.md`. Trust never gates it, but it then applies to every interactive `/uak-plan` too. That is a kit change, needs a WHY entry, and requires `kit_hashes.py` to be rerun.
- `--max-turns 60` is my choice. The docs set no default limit. `--max-budget-usd` is also available.
- `model: opus` in uak-plan.md switches that turn to Opus (cost).

**Risks**
- Once the folder is trusted, the broad kit allows apply. The `--disallowedTools` list is what keeps commit and push out.
- The kit's Stop hook can block the end of the run once if inbox messages exist.
- The SessionStart hook runs git and network activity.
- The PreToolUse guard still applies, which is good.
- `rm` is auto-approved by acceptEdits inside the project. Acceptable for this run, but note it.
- The run can hit a `Backlog-Approved` edit, because `.uak/PROJECT.md` is writable under acceptEdits. Only the prompt and post-run checks stop that. **Mitigation:** the UI snapshots `.uak/PROJECT.md` before the run, then verifies it after (or restores it).

## 4. OpenAI Codex CLI (`codex`)

Sources (developers.openai.com/codex/* now 308-redirects to learn.chatgpt.com/docs/*): https://learn.chatgpt.com/docs/non-interactive-mode · https://learn.chatgpt.com/docs/developer-commands?surface=cli · https://learn.chatgpt.com/docs/agent-approvals-security · https://learn.chatgpt.com/docs/config-file/config-basic · https://learn.chatgpt.com/docs/agent-configuration/rules · https://learn.chatgpt.com/docs/build-skills · https://learn.chatgpt.com/docs/hooks · https://learn.chatgpt.com/docs/windows/windows-sandbox. I also read local `codex exec --help` (0.167.1).

| Item | Finding |
|---|---|
| Headless syntax | `codex exec [OPTIONS] [PROMPT]`. With no prompt, or with `-`, it reads stdin. If stdin is piped **and** a prompt is given, stdin is appended as a `<stdin>` block, so pass stdin=DEVNULL. `-C/--cd DIR` sets the workspace root. Codex requires a git repo unless `--skip-git-repo-check`. `--ephemeral` saves no session files. |
| Skills / commands | Explicit `$skill-name` in the prompt invokes a skill. `allow_implicit_invocation: false` still allows explicit `$skill`. Repo skills are found in `.agents/skills` from cwd up to the repo root. **Whether `$uak-plan` works inside `codex exec` is UNVERIFIED**: the exec page does not mention skills. Fallback prompt text: "Read .agents/skills/uak-plan/SKILL.md and follow it", plus the constant text. |
| Permissions | `codex exec` defaults to a **read-only** sandbox. `--sandbox workspace-write` allows writes in the workspace and temp dirs. `.git`, `.agents`, `.codex` and `.aws` stay read-only, and network is off. `--full-auto` is **no longer supported**. `--approve-for-me` (alias `--not-so-yolo`) routes approval requests to automatic review. It is not a bypass flag, but it is an AI auto-approver, so I do not recommend it. `exec --help` lists **no `-a/--ask-for-approval`**. What exec does when a command needs escalation is **UNVERIFIED**; it is presumably not prompted, so the command fails inside the sandbox. Project rules (`.codex/rules/*.rules`, `prefix_rule(pattern=[...], decision="allow")`) run matching commands **outside** the sandbox. They load only for a trusted project and are experimental. The kit ships none, and none are needed: `bash .uak/bin/uak graph/lint` run inside workspace-write. Bypass flags to avoid: `--dangerously-bypass-approvals-and-sandbox`/`--yolo`, `--dangerously-bypass-hook-trust`, and `-s danger-full-access`. |
| Trust | Project `.codex/` layers (config, hooks, rules) load only when the project is trusted. Hooks also need a persisted per-hash trust given via `/hooks`. How trust is set and how exec behaves in an untrusted project are **UNVERIFIED**. |
| Install / auth detection | `codex --version` (local: `codex-cli 0.167.1`). `codex login status` prints the active auth mode and **exits 0 when logged in**. The logged-out exit code is undocumented; treat non-zero as logged out. `CODEX_API_KEY` works for exec. |
| Output / streaming | Default: progress goes to **stderr**, and only the final message goes to stdout. `--json` turns stdout into JSONL with events `thread.started`, `turn.started`, `turn.completed` (with usage), `turn.failed`, `item.*` (agent_message, reasoning, command_execution, file_change, mcp tool calls, plan updates) and `error`. `-o FILE` also writes the last message to a file. Exit codes are **UNVERIFIED** beyond "exits with an error" (for example when a required MCP server fails). |
| Windows | Native Windows with a PowerShell shell. The sandbox uses MXC (recommended, no admin), elevated (needs admin-approved setup, `codex sandbox setup --elevated`) or unelevated (legacy). How exec behaves on first run before sandbox setup is **UNVERIFIED**. `bash` from a PowerShell sandbox may resolve to WSL's `System32\bash.exe` (the kit already notes this). Whether `bash .uak/bin/uak` works under the Codex Windows sandbox is **UNVERIFIED; test it**. Locally the binary is at `%LOCALAPPDATA%\Programs\OpenAI\Codex\bin\codex`. |

**Recommended fixed argv.** Run it with cwd set to the project root and stdin set to DEVNULL:

```
["codex", "exec", "--cd", "<project-root>", "--sandbox", "workspace-write", "--json", "$uak-plan <CONSTANT TEXT>"]
```

- `<project-root>` comes from the UI's validated project path. It is the only variable element.
- Do not add `--skip-git-repo-check`. Codex refusing a non-git directory is a useful check.
- `$uak-plan` is literal because argv is not passed through a shell.

**Risks**
- The kit's Codex hooks (the guard) probably do not run (trust plus hook trust), so the sandbox is the only guard.
- `uak graph` loses the claims-branch view, because fetch is blocked.
- The model in `.codex/config.toml` applies only if the project is trusted. Otherwise the user's default model is used.
- `.agents/skills` is read-only, which is fine.

## 5. Gemini CLI (`gemini`)

Sources: https://geminicli.com/docs/cli/headless/ · https://geminicli.com/docs/cli/cli-reference/ · https://geminicli.com/docs/reference/policy-engine/ · https://geminicli.com/docs/cli/custom-commands/ · https://geminicli.com/docs/cli/trusted-folders/ · https://geminicli.com/docs/get-started/authentication/ · https://geminicli.com/docs/changelogs/ (latest v0.64.0, 2026-10-13) · https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli · https://github.com/google-gemini/gemini-cli/issues/21430

| Item | Finding |
|---|---|
| Status | Since 2026-06-18, Gemini CLI no longer serves Google AI Pro/Ultra or free individual users. It still works with paid Gemini API keys, Agent Platform keys and Code Assist Standard/Enterprise. The replacement is Antigravity CLI; its binary and headless mode are **UNVERIFIED** and were not researched. |
| Headless syntax | `gemini -p "<prompt>"` forces non-interactive mode. A non-TTY run also triggers it. |
| Custom commands headless | Changelog v0.7.0 (2025-09-22): "Run custom slash commands directly from the command line in non-interactive mode", example `gemini "/joke Chuck Norris"`. Issue #21430 was closed 2026-03-15; the maintainer said custom commands work and built-in slash commands "have never been supported". Project commands load from `.gemini/commands/*.toml`, but **not in an untrusted folder** (when folder trust is enabled). |
| Permissions | `--approval-mode default\|auto_edit\|yolo\|plan`. `yolo` and `-y/--yolo` are the bypass, so do not use them. `auto_edit`: "some write tools may be auto-approved"; exactly which are approved is **UNVERIFIED**. Write tools and `run_shell_command` default to `ask_user`, which **non-interactive treats as deny**. `--allowed-tools` is deprecated in favour of the Policy Engine. Policy tiers: Default, Extension, Workspace (**disabled**, "will not have any effect"), User `~/.gemini/policies/*.toml`, Admin. Changelog v0.30.0 added a `--policy` flag for user-defined policy files, but the current CLI reference does not list it, so it is **partially verified**. A UI-owned policy file passed with `--policy` could allow `run_shell_command` with `commandPrefix = "bash .uak/bin/uak lint"`. Whether commandPrefix splits compound commands is **UNVERIFIED**, so `... lint && git push` might match. Prefer the UI running graph and lint itself. |
| Trust | If `security.folderTrust.enabled` is on in user settings, a headless run in an untrusted folder throws `FatalUntrustedWorkspaceError` and exits. v0.41.0 enforced trust in headless mode. The overrides are `--skip-trust` and `GEMINI_CLI_TRUST_WORKSPACE=true`. That is a trust bypass, so do not pass it silently: surface the error and ask the user to trust the folder interactively. An untrusted folder also skips project `.gemini/settings.json` (the kit's hooks and MCP) and custom commands. |
| Install / auth detection | `gemini --version` / `-v`. There is **no documented auth-status command**. Headless uses cached credentials from a prior interactive login, or env (`GEMINI_API_KEY`, or Vertex: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, ADC or `GOOGLE_API_KEY`). The cache path is undocumented, so a side-effect-free auth check is **UNVERIFIED**. Best effort: env var present, or treat exit 1 / an auth `error` in JSON output as "not authenticated". |
| Output / exit codes | `--output-format text\|json\|stream-json`. `json` gives `{response, stats, error?}`. `stream-json` gives JSONL events `init`, `message`, `tool_use`, `tool_result`, `error`, `result`. Exit codes: **0** success, **1** general/API error, **42** input error, **53** turn limit exceeded. |
| Windows | The docs have no Windows notes; the admin policy path is `C:\ProgramData\gemini-cli\policies`. The `.cmd` npm-shim caveat in section 7 applies. |

**Recommended fixed argv** (stdin=DEVNULL):

```
["gemini", "-p", "/uak-plan <CONSTANT TEXT>", "--approval-mode", "auto_edit", "--output-format", "stream-json"]
```

The UI runs graph and lint afterwards, because shell commands are denied.

**Risks**
- auto_edit may still deny `write_file` in headless (UNVERIFIED). If so, Gemini produces nothing, and the UI should report "Gemini cannot plan headless; run /uak-plan interactively".
- The account-availability change above.
- Trust errors.

## 6. Cursor CLI (`agent`, formerly `cursor-agent`)

Sources: https://cursor.com/docs/cli/headless · https://cursor.com/docs/cli/reference/parameters · https://cursor.com/docs/cli/reference/permissions · https://cursor.com/docs/cli/reference/configuration · https://cursor.com/docs/cli/reference/output-format · https://cursor.com/docs/cli/reference/authentication · https://cursor.com/docs/cli/using · https://cursor.com/docs/cli/changelog (latest v2026.10.22)

| Item | Finding |
|---|---|
| Binary | Current docs use only **`agent`**. Whether `cursor-agent` still exists as an alias is **UNVERIFIED**: forum posts use it and the docs never mention it. Detect `agent` first, then `cursor-agent`. Because `agent` is a generic name, confirm with `agent --version`. |
| Headless syntax | `agent -p "<prompt>"` (`--print`). `--workspace <path>` sets the workspace. `--mode plan\|ask` makes the run read-only. Non-interactive runs in an untrusted workspace "fail with guidance unless `--trust` (or `--force`) is passed" (changelog, Jan 2026). |
| Skills / commands | Changelog (2026-05-07): "Skills load in interactive, headless, and editor-integration modes; `/skill-name` invocations work in `-p` print mode." The kit's `/uak-plan` lives in `.agents/skills`. |
| Permissions | Headless page: "Without --force, changes are only proposed, not applied." The `-f/--force` flag means "Force allow commands unless explicitly denied", and `--yolo` is its alias, so it **is the bypass**. The CLI "using" page contradicts this ("Cursor has full write access in non-interactive mode"). Allow/deny lists: `Shell(cmd)`, `Read(glob)`, `Write(glob)`, `WebFetch(...)`, `Mcp(server:tool)` in `<project>/.cursor/cli.json` (only `permissions` is allowed at project level) or in `~/.cursor/cli-config.json`, which also has `approvalMode: allowlist\|auto-review\|unrestricted`. Deny beats allow. Whether allow rules alone let a `-p` run write or execute without `--force` is **UNVERIFIED**. The Shell token granularity is `Shell(commandBase)`, so `bash .uak/bin/uak lint` could probably only be allowed as `Shell(bash)` (all bash). Changelog (March 2026) mentions a `permissions.json` allowlist shared with the IDE; **UNVERIFIED** detail. |
| Install / auth detection | `agent --version` / `-v`. `agent status` (alias `whoami`) shows auth status, account and endpoint; exit codes are **undocumented**. `CURSOR_API_KEY` or `--api-key` also authenticate. |
| Output / exit codes | `--output-format text\|json\|stream-json`. `--stream-partial-output` adds deltas (stream-json only). The json result has `type: "result"`, `subtype: "success"`, `is_error`, `result`, `session_id`, `duration_ms`. stream-json has system init, user, assistant, tool_call started/completed, and a final result. On failure the process exits non-zero, writes the error to stderr, emits no JSON object, and the stream may end without a result event. |
| Windows | Native Windows install via `irm 'https://cursor.com/install?win32=true' \| iex`. Shell commands run in PowerShell (UTF-8 since v2026.10.22). It works under restricted execution policy and detects Git Bash (Jan 2026). |

**Recommended fixed argv** (best effort, stdin=DEVNULL):

```
["agent", "-p", "--workspace", "<project-root>", "--output-format", "stream-json", "/uak-plan <CONSTANT TEXT>"]
```

- No `--force` and no `--yolo`.
- Pass `--trust` **only** after the user explicitly confirms trust in the UI. It trusts the workspace and is not a permission bypass, but it does make the project's hooks and config apply.
- Ship a `.cursor/cli.json` with `{"permissions":{"allow":["Write(.uak/TASKS.md)","Write(.uak/OWNERS.md)"],"deny":["Shell(git)"]}}`. This is a kit change, and whether it is enough without `--force` is UNVERIFIED.

**Risks**
- As documented, without `--force` the run only *proposes* changes. Expect "no files written" and handle it with the message "Cursor cannot plan headless without --force; open Cursor and run /uak-plan".
- `--force` would also auto-run every shell command not denied, including `git push`.

## 7. Cross-cutting notes for the stdlib server (general Python/Windows knowledge, not from harness docs)

- **Process launch:** use `subprocess.Popen(argv_list, cwd=root, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=False)`.
- **Resolve the executable** with `shutil.which(name)`. On Windows, npm-installed CLIs are `.cmd` shims. Launching a `.cmd` runs it through `cmd.exe` argument parsing (the "BatBadBut" class of issue), which is why the constant prompt avoids `% ^ & | < > "`. Prefer a real `.exe` when one exists: Claude native is `claude.exe`, and Codex local is under `Programs\OpenAI\Codex\bin`.
- **Read stdout line by line** for stream-json/JSONL, and drain stderr in a separate thread. A full pipe blocks the child. Codex writes progress to stderr.
- **Stop:** Claude ends the turn cleanly on SIGINT. On Windows use `CTRL_BREAK_EVENT` with `CREATE_NEW_PROCESS_GROUP`, else terminate; terminate gives Claude exit 143 with no result.
- **Post-run verification by the UI** (this is the real gate):
  - `.uak/TASKS.md` and `.uak/OWNERS.md` exist and are non-empty;
  - `bash .uak/bin/uak lint` prints `LINT_OK`;
  - `git rev-parse HEAD` is unchanged from before the run;
  - `git status --porcelain` shows changes only under `.uak/TASKS.md` and `.uak/OWNERS.md`;
  - `.uak/PROJECT.md` has no `Backlog-Approved: yes` that was not there before.
- **Detection without side effects:**

  | Harness | Installed | Authenticated |
  |---|---|---|
  | Claude | `claude --version` | `claude auth status`: exit 0 or 1 |
  | Codex | `codex --version` | `codex login status`: exit 0 means logged in |
  | Gemini | `gemini --version` | no command; UNVERIFIED |
  | Cursor | `agent --version` | `agent status`: exit code UNVERIFIED |

  These only read state. I believe none of them opens a browser, but that is UNVERIFIED for `agent status`.

## 8. UNVERIFIED summary

- **Claude:** whether `Bash(x *)` matches a bare `x` with no arguments.
- **Codex:**
  - `$skill` invocation inside `codex exec`;
  - exec behavior when a command needs approval;
  - exec exit codes;
  - exec in an untrusted project;
  - whether `uak lint` works with `.git` read-only and no network;
  - `bash` resolution under the Windows sandbox;
  - exit code of `codex login status` when logged out.
- **Gemini:**
  - which write tools `auto_edit` approves in headless;
  - how args are passed to a TOML command without `{{args}}`;
  - the `--policy` flag (only in the changelog);
  - commandPrefix behavior with compound commands;
  - an auth-status check;
  - Antigravity CLI.
- **Cursor:**
  - whether `-p` without `--force` can write (the docs contradict each other);
  - whether `cli.json` allow rules replace `--force`;
  - `Shell()` granularity;
  - the `cursor-agent` alias;
  - `agent status` exit codes.
