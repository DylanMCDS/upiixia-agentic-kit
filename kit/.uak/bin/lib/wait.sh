# wait: one call that returns when something happens on claims, instead of polling.
# Sourced by .uak/bin/uak (docs/ARCHITECTURE.md: where to change what). Bash 3.2+, POSIX tools.

# One call that blocks until something happens on claims, instead of an agent polling status/inbox.
# A cheap `git ls-remote` every WAIT_EVERY s (0.4 s with SSH reuse); claims are read only when their tip moves.
# Why (MLB hackathon): 225 `status` and 172 `inbox` calls, most of them an agent checking whether its review,
# a dependency or a reply had arrived; every call re-sends its output into the agent's context.
#   approve     your REVIEW task (or ID): exit 0 on approve or INTEGRATED, 3 on reject
#   integrated  ID becomes INTEGRATED (a dependency): exit 0
#   message     a new unread message for you: printed, exit 0
# Timeout (default 540 s, under a 10-min tool limit): WAIT_TIMEOUT, exit 4. The third empty timeout in a row of one
# identity (Idle-Stop-Waits) is IDLE_STOP, exit 5: the agent ends its turn instead of waiting again (UAK-100).
wait_run() {
  local wait_rc=0
  wait_poll || wait_rc=$?
  # Something happened (an event, an approval, a reject): the idle count starts over.
  case "$wait_rc" in 0|3) wait_idle_reset;; esac
  return "$wait_rc"
}
# Idle stop. Why (2026-11-19, the kit's own repo): a Codex session blocked on a human authorization ran about 200
# `uak wait --for message --timeout 540` cycles over 9 h; each timeout handed control back to the model, which waited
# again: 757 model turns, about 129M cached input tokens, the human's whole session. A wait is one bounded call for an
# event, never a loop. The count lives in the git dir, per identity; a loop the human started (UAK_LOOP=1, /uak-loop,
# docs/LOOPS.md) keeps its own pacing.
wait_loop_mode() { case "${UAK_LOOP:-}" in ''|0|no|off|false) return 1;; *) return 0;; esac; }
wait_idle_file() {
  local gd
  gd=$(cd "$ROOT" 2>/dev/null && cd "$(git rev-parse --git-common-dir 2>/dev/null)" 2>/dev/null && pwd -P) || return 1
  mkdir -p "$gd/uak-idle" 2>/dev/null || return 1
  printf '%s/uak-idle/%s' "$gd" "$(printf '%s' "${AGENT:-anonymous}" | tr -c 'A-Za-z0-9._-' '_')"
}
wait_idle_reset() { local f; f=$(wait_idle_file) || return 0; rm -f "$f"; }
# What this identity holds: a claim taken or released, a state or a verdict that moved resets the count.
wait_idle_sig() {
  local c id s=
  for c in "$TX"/claims/*.md; do
    [ -f "$c" ] && [ "$(field "$c" Owner)" = "$AGENT" ] || continue
    id=$(field "$c" ID)
    s="$s $id:$(field "$c" State):$(field "$TX/reviews/$id.md" Verdict)@$(field "$TX/reviews/$id.md" SHA)"
  done
  printf '%s' "${s:- none}"
}
# The last message this identity sent to human that no later message to it (or to that task) answered.
wait_human_blocker() {
  [ -f "$TX/$MSG_LOG" ] || return 0
  awk -F' [|] ' -v me="$AGENT" -v now="$(date +%s)" '
    /^- [0-9]/ {
      n = substr($1, 3) + 0; nt = split($4, t, ","); tohuman = 0; tome = 0
      for (i = 1; i <= nt; i++) {
        if (t[i] == "human") tohuman = 1
        if (t[i] == "agent:" me || (task != "" && t[i] == "task:" task)) tome = 1
      }
      if (b && $3 != me && tome) b = 0
      if ($3 == me && tohuman) { b = n; bt = $2 + 0; task = ($6 == "-") ? "" : $6; txt = $7; sub(/\r$/, "", txt); txt = substr(txt, 1, 160) }
    }
    END { if (b) { m = int((now - bt) / 60); if (m < 0) m = 0; printf "#%d (%d min ago): %s", b, m, txt } }' "$TX/$MSG_LOG"
}
# The timeout: exit 4 with one line that never says to wait again, or IDLE_STOP (exit 5) at the cap.
wait_idle_timeout() {
  local f cnt= first= osig= sig max now blk mins
  if wait_loop_mode; then
    say "WAIT_TIMEOUT ${ID:+$ID }$WAIT_FOR after $WAIT_TIMEOUT s: nothing yet (UAK_LOOP: your loop paces the next iteration)."
    return 4
  fi
  [ -d "${TX:-/nonexistent}" ] || { ATTEMPT=wait-end; fresh_state; }
  now=$(date +%s); sig=$(wait_idle_sig)
  if f=$(wait_idle_file); then
    [ ! -f "$f" ] || { IFS= read -r cnt; IFS= read -r first; IFS= read -r osig; } < "$f"
  fi
  case "$cnt" in ''|*[!0-9]*) cnt=0;; esac
  case "$first" in ''|*[!0-9]*) first=;; esac
  [ "$osig" = "$sig" ] && [ -n "$first" ] || { cnt=0; first=$((now - WAIT_TIMEOUT)); }
  cnt=$((cnt + 1))
  [ -z "$f" ] || printf '%s\n%s\n%s\n' "$cnt" "$first" "$sig" > "$f" 2>/dev/null || true
  coord_cfg Idle-Stop-Waits 3; max=$coord_v; case "$max" in ''|*[!0-9]*|0) max=3;; esac
  if [ "$cnt" -ge "$max" ]; then
    mins=$(( (now - first) / 60 )); blk=$(wait_human_blocker)
    say "IDLE_STOP: nothing happened in $mins min. End your turn now and stop; a human or the lead restarts you with a message.${blk:+ Blocked on a human act: $blk}"
    return 5
  fi
  say "WAIT_TIMEOUT ${ID:+$ID }$WAIT_FOR after $WAIT_TIMEOUT s: nothing yet (empty wait $cnt of $max). Nothing else to do: end your turn; a human or the lead restarts you with a message. Only one bounded wait for a specific event: uak wait ID --for approve."
  return 4
}
wait_poll() {
  local deadline last= tip n=0 rv st c left
  deadline=$(( $(date +%s) + WAIT_TIMEOUT ))
  if [ "$WAIT_FOR" = approve ] && [ -z "$ID" ]; then
    ATTEMPT=wait-0; fresh_state
    for c in "$TX"/claims/*.md; do
      [ -f "$c" ] && [ "$(field "$c" Owner)" = "$AGENT" ] && [ "$(field "$c" State)" = REVIEW ] && { ID=$(field "$c" ID); break; }
    done
    [ -n "$ID" ] || die "wait --for approve: you have no task in REVIEW; name one: uak wait ID --for approve"
  fi
  [ "$WAIT_FOR" = message ] || [ -n "$ID" ] || die "wait --for $WAIT_FOR needs an ID."
  say "WAITING ${ID:+$ID }for $WAIT_FOR (up to $WAIT_TIMEOUT s; checks every $WAIT_EVERY s)"
  local wait_base= wait_rc0= wait_new
  # Unread messages from before the wait are answered now, not by waiting.
  if [ "$WAIT_FOR" = message ]; then
    ATTEMPT=wait-0; fresh_state
    wait_base=$(awk '/^- [0-9]/ { n = $2 + 0; if (n > m) m = n } END { print m + 0 }' "$TX/$MSG_LOG" 2>/dev/null || echo 0)
    # The reviewable work already waiting is not news: only a task that enters REVIEW after this point wakes the wait.
    wait_rc0=; [ ! -f "$TX/roles/reviewers/$AGENT.md" ] || { coord_review_candidate; wait_rc0=$coord_rc; }
    c=$(msg_select unread | grep -c '^#' || true)
    [ "${c:-0}" -eq 0 ] || say "($c unread from before this wait: uak inbox shows them; the wait returns only for new ones.)"
  fi
  while :; do
    tip=$(git -C "$ROOT" ls-remote "$REMOTE" refs/heads/claims 2>/dev/null | awk '{print $1; exit}')
    if [ -n "$tip" ] && [ "$tip" != "$last" ]; then
      last=$tip; n=$((n + 1)); ATTEMPT="wait-$n"; [ -n "${UAK_NOW:-}" ] || NOW=$(date +%s)
      fresh_state
      case "$WAIT_FOR" in
        approve)
          st=$(field "$TX/tasks/$ID.md" State); rv="$TX/reviews/$ID.md"
          if [ "$st" = INTEGRATED ]; then say "INTEGRATED $ID ($(field "$TX/tasks/$ID.md" Merge-Commit | cut -c 1-7))"; return 0; fi
          if [ -f "$rv" ] && [ "$(field "$rv" SHA)" = "$(field "$TX/tasks/$ID.md" Task-Tip)" ]; then
            case "$(field "$rv" Verdict)" in
              approve) say "APPROVED $ID by $(field "$rv" Reviewer) on $(field "$rv" SHA | cut -c 1-7). Next: bash .uak/bin/uak merge $ID"; return 0;;
              reject) say "REJECTED $ID by $(field "$rv" Reviewer) on $(field "$rv" SHA | cut -c 1-7). Read it: bash .uak/bin/uak inbox --task $ID"; return 3;;
            esac
          fi;;
        integrated)
          st=$(field "$TX/tasks/$ID.md" State)
          if [ "$st" = INTEGRATED ]; then say "INTEGRATED $ID ($(field "$TX/tasks/$ID.md" Merge-Commit | cut -c 1-7)). git fetch origin && git merge --no-edit origin/$BASE"; return 0; fi;;
        message)
          # Only what arrives after the wait started. Why (audit, Oct 2026): 15 unread messages already shown made
          # every wait return in a second, and the agent polled.
          [ -n "$wait_base" ] || wait_base=$(awk '/^- [0-9]/ { n = $2 + 0; if (n > m) m = n } END { print m + 0 }' "$TX/$MSG_LOG" 2>/dev/null || echo 0)
          c=$(msg_select unread | awk -v b="${wait_base:-0}" '/^#[0-9]/ { n = substr($1, 2) + 0; keep = n > b } keep')
          if [ -n "$c" ]; then say "NEW for $AGENT:"; say "$c"; say "Handle them, then uak inbox --ack."; return 0; fi
          # A registered reviewer also wakes when a task it may review enters REVIEW, whoever was asked (UAK-038, DevDay).
          if [ -f "$TX/roles/reviewers/$AGENT.md" ] && [ ! -f "$TX/meta/retired/$AGENT.md" ]; then
            coord_review_candidate
            if [ -n "$coord_rc" ] && [ "$coord_rc" != "$wait_rc0" ]; then
              say "REVIEW waiting: ${coord_rc#* } of ${coord_rc%% *}: /uak-review ${coord_rc%% *}"; return 0
            fi
          fi;;
      esac
    fi
    left=$((deadline - $(date +%s)))
    [ "$left" -gt 0 ] || { wait_idle_timeout; return; }
    # Never past the deadline: --timeout 3 used to sleep the whole 15 s check interval.
    [ "$left" -ge "$WAIT_EVERY" ] || { sleep "$left"; continue; }
    sleep "$WAIT_EVERY"
  done
}
