# UI-002 design draft (claude-Dylan, prepared while UI-001 is in review)

Not in the repo. Becomes the task's tests and stub once UI-001 is integrated and UI-002 is claimable.

## Live-URL ("Your app")
- Key: `Live-URL:` in `.uak/PROJECT.md`, default `-` in both templates (PROJECT.sprint.md, PROJECT.marathon.md), documented in CLI.md's field list.
- Finding: the dashboard reads config from claims `meta/config.md`, which the engine writes from a fixed allowlist
  (`uak-coordination` coord_config, lines ~130-161). Adding the key there would be an engine change outside
  UI-002's Paths. Instead `dash.py` reads `Live-URL` from the base branch's PROJECT.md that `snapshot()` already
  fetches (`refs/uak/dash-base:.uak/PROJECT.md`), and from the local file in local mode. The static `uak dash`
  export gets it the same way. No engine change.
- Validation (server and dash.py, one function): absolute `https://`, host present, no userinfo (`@` before the host),
  no whitespace or control characters, at most 2048 chars; anything else is treated as absent.
- Setup write: `Live-URL` joins the allowlist with this validator; `save_settings` must INSERT the key into the
  executable block when an older PROJECT.md lacks it (today it refuses a missing key), still atomic and preserving
  every other byte.
- Render: an anchor with `textContent` = the URL host + path, `href` set only after validation, `target=_blank`,
  `rel="noopener noreferrer"`. Without a URL: "Not deployed yet" + the deploy step text (no guessed URL).

## Guided Beginner
- One step per screen: the step = `guidance` from UI-001 (`/api/status`, `/api/dashboard`), never computed in JS.
- Checklist of completed steps = the OK lines of the last `uak start`, as text.
- Auto re-check: on `visibilitychange` to visible and every 30 s while a todo step is shown; never while busy.
- Copy only `guidance.commands` (the exact claim command), already enforced by UI-001.

## Tests (named in the task)
| Test | Kind | Asserts |
|---|---|---|
| live_url_is_https_only | unit | http:, javascript:, data:, `https://u:p@h`, spaces, 3000 chars -> None; `https://app.example.com/x` -> kept |
| live_url_link_is_shown_when_set | HTTP | PROJECT.md with Live-URL -> `/api/dashboard` has `live_url`; absent/invalid -> null; saving via `/api/settings` inserts the key atomically and keeps unrelated bytes |
| next_action_matches_real_state | HTTP | dashboard `guidance` equals status `guidance` for todo/ready/frozen fixtures |
| copy_command_is_exact | unit | only `bash .uak/bin/wt new ID` reaches `commands` |
| beginner_shows_one_action | markup+HTTP | one primary button in the beginner step region; guidance has one kind |
| hostile_content_is_text | HTTP | task titles and Live-URL with markup come back verbatim; page code has no innerHTML on them |
| static_dashboard_remains_offline | CLI | `uak dash` export opens from file:// with live_url and no network references |
| beginner_profile_persists / advanced_profile_preserves_details / ready_opens_progress | browser evidence (UI-003 journey) + markup contract named honestly |
