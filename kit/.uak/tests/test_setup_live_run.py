#!/usr/bin/env python3
"""UI-026: fixes from Dylan's live run on turno-cafeteria-3 (2026-11-19, kit next 9998cb4). Real HTTP and real Git
with a local bare remote where the server matters; the page's own code runs in Node over a fake DOM of setup.html
(test_setup_feedback), or is only read without Node.
Evidence: (a) after a successful publish step 3 kept "Espera: se está publicando el kit.", "Listo a las 07:35." and
"Revisar los archivos"; (b) with Claude Code's trust ✓ the note still said "Hasta entonces ignora los permisos … el
plan se detiene antes de tiempo"; (c) "Creando el plan…" gave no idea of its 4-5 minutes; (d) `uak start` alone took
~31 s, hit the 45 s bound and the page blamed "origin no respondió en 45 s" while origin answered in 0.4 s; (e) the
implementer command was pasted inside the Claude Code session opened for the trust step; (f) the implementer stopped
before /uak-ship, so the task never reached REVIEW; (g) the board card said "0 commit(s) desde que se tomó" while
feat/hack-001 had 2 pushed commits."""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

import test_setup_feedback as tf
import test_setup_planning as tp
import test_setup_prepare as prep
import test_setup_resume as tr
import test_setup_team as team
import test_setup_wizard as wizard
from test_hack import resolve_binary

MODULE = None
ROOT = None
NEW_TERMINAL = "Paste it in a new terminal, not inside Claude or Codex."
NEW_TERMINAL_ES = "Pégalo en una terminal nueva, no dentro de Claude ni Codex."


def page():
    return tf.page()


def code():
    return tf.script(page())


def run(scenario, functions, language="en", extra=""):
    """SCENARIO (an async function body) over workspace.js, the page's feedback and resume blocks and FUNCTIONS of the
    page, with a fetch the scenario controls (test_setup_resume.shim). None without Node."""
    node = shutil.which("node")
    if not node:
        print("  note: no Node.js here, so the page logic is checked by reading it only")
        return None
    html = page()
    script = tf.script(html)
    sources = [tr.shim(language), tf.lib("workspace.js"), tf.PRELUDE, tr.EXTRA, extra]
    sources += [tf.page_function(script, name) for name in ("el", "isBusy", "error", "api")]
    sources += [tf.block(script), tr.block(script)]
    sources += [tf.page_function(script, name) for name in functions]
    with tempfile.TemporaryDirectory(prefix="uak-live-run-js-") as folder:
        program = Path(folder) / "run.js"
        program.write_text(tf.NODE_PROGRAM, encoding="utf-8")
        done = subprocess.run([node, str(program)], input=json.dumps({"language": language, "sources": sources,
                                                                      "tree": tf.tree(html), "scenario": scenario,
                                                                      "reduced": False}),
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert done.returncode == 0, "the page logic runs: %s" % done.stderr[-2000:]
    return json.loads(done.stdout)


def git(cwd, *args):
    return tp.git(cwd, *args)


# --- publish_step_says_published --------------------------------------------------------------------------------------


def publish_step_says_published(root, tmp):
    target, remote = prep.installed(root, tmp)
    with tp.live(target, tp.FakePlanner()) as srv:
        prep.ready_to_publish(srv, target)
        status, preview = tp.get(srv, "/api/publish-kit")
        assert status == 200, preview
        # The worker refreshes the restore facts after its operation; hold that refresh, so the status the page reads
        # the moment publishing ends is the one it keeps (the page stops polling once nothing runs).
        gate, entered, real = threading.Event(), threading.Event(), srv.refresh_progress

        def held():
            entered.set()
            gate.wait(60)
            return real()

        srv.refresh_progress = held
        try:
            status, body = tp.post(srv, "/api/publish-kit", {"digest": preview["digest"]})
            assert status == 202, body
            assert entered.wait(120), "the publish worker ends"
            state = tp.get(srv, "/api/status")[1]
        finally:
            gate.set()
        tp.wait_idle(srv)
        head = prep.remote_head(remote)
        assert head and state["phase"] not in MODULE.BUSY and not state.get("error"), state.get("error")
        resume = state.get("resume") or {}
        assert resume.get("kit_on_main") is True and resume.get("base_sha") == head[:7], \
            "the status that ends publishing already says the kit is on main at %s: %r" % (head[:7], resume)

    out = run("""
        state = {installed: true, phase: "setup", human: "ana", resume: {kit_on_main: true, base_sha: "abc1234"},
                 guidance: {kind: "todo", action: "plan"}};
        lastButton = "publish-kit";
        // What the publishing run left: its busy reason, then its result line under Review the files.
        setWaiting(el("publish-preview"), "publishing");
        done(el("publish-kit"));
        drawDone(state);
        drawPublished(state);
        var line = el("publish-preview-result");
        return {done: !el("publish-done").hidden, text: el("publish-done-text").textContent,
                marked: el("publish-step").hasAttribute("data-done"), open: el("publish-step").hasAttribute("data-open"),
                why: !el("publish-preview-why").hidden, result: !!line && !line.hidden && line.textContent !== "",
                review: !el("publish-preview").hidden};
    """, ("drawPublished",), language="es")
    if out is not None:
        es = tf.catalog()
        assert es.get("Published on main (commit {sha}).", "").replace("{sha}", "abc1234") == out["text"], out
        assert out["done"] and out["marked"] and not out["open"], "step 3 is marked done: %r" % out
        assert not out["why"] and not out["result"] and not out["review"], \
            "no busy line, no result line and no Review the files button once published: %r" % out
    refresh = tf.page_function(code(), "refresh")
    assert re.search(r"isBusy\(was\)", refresh), "the page reads the status once more after an operation ends"


# --- trusted_hides_the_open_claude_note -------------------------------------------------------------------------------


def trusted_hides_the_open_claude_note(root, tmp):
    html = page()
    note = tr.section(html, "plan-trust")
    assert 'id="plan-trust-why"' in note, "the instruction to open Claude Code is its own element"
    out = run("""
        function look(trust) {
          planView = {trust_command: "cd '/p/a' && claude", trust: trust};
          drawPlanTrust();
          var command = el("plan-trust-command").closest(".next-command");
          return {why: !el("plan-trust-why").hidden, command: !command.hidden, help: el("plan-trust-help").textContent,
                  note: !el("plan-trust").hidden};
        }
        selectedPlanner = function () { return "claude"; };
        return {yes: look(true), no: look(false), unknown: look(null)};
    """, ("trustLine", "trustText", "drawPlanTrust"), extra="function selectedPlanner() { return 'claude'; }")
    if out is None:
        return
    assert out["yes"]["note"] and not out["yes"]["why"] and not out["yes"]["command"], \
        "trusted: only the ✓ line, no instruction to open Claude Code: %r" % out["yes"]
    assert out["yes"]["help"].startswith("✓") and "↓" not in out["yes"]["help"], out["yes"]
    for name in ("no", "unknown"):
        assert out[name]["note"] and out[name]["why"] and out[name]["command"], \
            "%s: the instruction and its command show: %r" % (name, out[name])


# --- plan_says_how_long -----------------------------------------------------------------------------------------------


def plan_says_how_long(root, tmp):
    html = page()
    es = tf.catalog()
    hint = re.search(r'<p class="hint" id="plan-duration"[^>]*>([\s\S]*?)</p>', html)
    assert hint, "the plan button has a duration hint"
    words = " ".join(hint.group(1).split())
    assert "about 5 minutes" in words and es.get(words), "it says how long, with Spanish: %r" % words
    assert html.index('id="plan-create"') < html.index('id="plan-duration"') < html.index('id="plan-progress"'), \
        "the hint sits under Create the plan, above the elapsed time"
    out = run("""
        drawPlanProgress({phase: "planning", plan_progress: {elapsed: 125, last: ""}});
        var running = el("plan-progress").textContent;
        return {running: running, shown: !el("plan-progress").hidden};
    """, ("drawPlanProgress", "tickPlanProgress"), extra="var planClock = null, gone = false;")
    if out is not None:
        assert out["shown"] and "2:05" in out["running"], "the elapsed time shows while it plans: %r" % out


# --- check_timeout_names_the_step -------------------------------------------------------------------------------------


class SlowStart(team.Team):
    """`uak start` prints its first steps, then setup's bound stops it (exit 124 with the partial output)."""

    def __init__(self, partial):
        super().__init__()
        self.partial, self.starts = partial, []

    def __call__(self, command, cwd=None, timeout=120, group=False, env=None, **kwargs):
        if len(command) >= 3 and command[-1] == "start" and str(command[-2]).endswith("uak"):
            self.starts.append(timeout)
            return subprocess.CompletedProcess(command, 124, self.partial, "The run took too long and was stopped.")
        return super().__call__(command, cwd=cwd, timeout=timeout, group=group, env=env, **kwargs)


def check_timeout_names_the_step(root, tmp):
    # Measured (UI-026): a normal `uak start` took ~31 s on Dylan's macOS run against GitHub; the bound has margin.
    assert MODULE.CHECK_TIMEOUT >= 2 * 31, "the bound covers a normal uak start with margin: %d" % MODULE.CHECK_TIMEOUT
    partial = "OK    1. kit installed (sprint, uak 6.4.0)\r\nOK    2. remote origin reachable\r\n"
    target, _ = team.ready_project(root, tmp)
    runner = SlowStart(partial)
    with tp.live(target, runner) as srv:
        runner.srv = srv
        assert tp.post(srv, "/api/inspect", {"target": str(target)})[0] == 200
        state = team.check(srv)
        assert runner.starts == [MODULE.CHECK_TIMEOUT], runner.starts
        error = state.get("error", "")
        assert "preflight (doctor)" in error and "%d s" % MODULE.CHECK_TIMEOUT in error, \
            "the timeout names the step that was running: %r" % error
        assert "did not answer" not in error and "origin" not in error, "origin answered; it is not blamed: %r" % error
        assert team.translated(error), "the message has Spanish: %r" % error
    steps = [MODULE.check_step(text) for text in ("", "OK    1. kit installed\n", partial,
                                                  partial + "OK    3. preflight: doctor clean\n",
                                                  partial + "OK    3. preflight: doctor clean\nTODO  4. push the kit to main\n",
                                                  partial + "OK    5. plan: 2 task(s), lint clean\n")]
    assert len(set(steps)) == len(steps), "each place names its own step: %r" % steps
    es = tf.catalog()
    assert all(es.get(s) for s in steps), "every step name has Spanish: %r" % [s for s in steps if not es.get(s)]

    out = run("""
        var calls = 0;
        api = function (path) { if (path === "check") calls += 1; return new Promise(function () {}); };
        document.body.dataset.profile = "beginner";
        state = {installed: true, phase: "setup", guidance: {kind: "todo"}};
        autoCheck();
        autoCheck();
        var during = calls;
        return {during: during};
    """, ("autoCheck", "operationBusy", "startCheck"),
        extra="var checkRequested = false, checkAuto = false, checkBefore = null, pointAfterCheck = false, gone = false,"
              " lastButton = '', autoPending = false;")
    if out is not None:
        assert out["during"] == 1, "the automatic check does not start while the previous one runs: %r" % out


# --- commands_say_new_terminal ----------------------------------------------------------------------------------------


def commands_say_new_terminal(root, tmp):
    html = page()
    es = tf.catalog()
    assert es.get(NEW_TERMINAL) == NEW_TERMINAL_ES, "the line has its Spanish pair: %r" % es.get(NEW_TERMINAL)
    for block, command in (("team-implement", "team-implement-command"), ("team-implement", "team-implement-resume"),
                           ("team-review", "team-review-command"), ("plan-trust", "plan-trust-command")):
        part = tr.section(html, block)
        at = part.index('id="%s"' % command)
        after = part[at:]
        follow = re.search(r'<p class="hint new-terminal">([\s\S]*?)</p>', after)
        assert follow and " ".join(follow.group(1).split()) == NEW_TERMINAL, \
            "#%s is followed by %r" % (command, NEW_TERMINAL)
        between = after[:follow.start()]
        assert "<code" not in between[5:], "the line belongs to #%s, not to a later command" % command
    trust = " ".join(re.sub(r"<[^>]+>", " ", tr.section(html, "plan-trust")).split())
    close = "Then close that Claude Code session (type /exit) before you paste any other command."
    assert close in trust and es.get(close), "the trust step says to close that session afterwards, with Spanish"


# --- implementer_prompt_ships -----------------------------------------------------------------------------------------


def implementer_prompt_ships(root, tmp):
    for prompt, ship, start in ((MODULE.IMPL_PROMPT, "/uak-ship", "/uak-start"),
                                (MODULE.IMPL_PROMPT_CODEX, "$uak-ship", "$uak-start")):
        assert prompt.startswith("Run %s for %%s." % start), prompt
        assert ship in prompt and "REVIEW" in prompt and "next task" in prompt, \
            "the prompt carries the task through %s to REVIEW, then the next task: %r" % (ship, prompt)
        assert prompt.index(start) < prompt.index(ship), prompt
        assert not re.search(r"[`'\"\\;&|<>()]", prompt), "no shell metacharacters: %r" % prompt
    command = MODULE.implement_command("claude", "/p/a b", "/p/a b-wt/app-001", "/p/a b/.git", "APP-001",
                                       "claude-ana", "ana")
    assert "/uak-ship" in command and "APP-001" in command, command
    html = page()
    es = tf.catalog()
    words = " ".join(re.sub(r"<[^>]+>", " ", re.search(r'<p class="hint" id="team-ships"[^>]*>([\s\S]*?)</p>',
                                                         tr.section(html, "team-implement")).group(1)).split())
    assert "In review" in words and "En revisión" in es.get(words, ""), \
        "the page says the task reaches In review by itself: %r -> %r" % (words, es.get(words))


# --- card_counts_branch_commits ---------------------------------------------------------------------------------------


def card_counts_branch_commits(root, tmp):
    target, remote = team.ready_project(root, tmp)
    git(target, "checkout", "-q", "-b", "feat/app-001")
    report = int(time.time()) - 600
    for n in (1, 2):
        (target / ("work%d.txt" % n)).write_text("x\n", encoding="utf-8")
        git(target, "add", "-A")
        git(target, "commit", "-q", "-m", "work %d" % n)
    git(target, "push", "-q", "origin", "feat/app-001")
    git(target, "checkout", "-q", "main")
    stale = "0 commit(s) since the claim · last: - · 0 uncommitted tracked file(s) · at %d" % report
    fresh = "2 commit(s) since the claim · last: abc work 2 (1 minute ago) · 0 uncommitted tracked file(s) · at %d" % (
        int(time.time()) + 60)

    def runner(*args):
        return subprocess.run([resolve_binary("git"), "-c", "color.ui=never", "-C", str(target)] + list(args),
                              capture_output=True, text=True, encoding="utf-8", errors="replace")

    data = {"tasks": [{"id": "APP-001", "state": "CLAIMED", "progress": stale},
                      {"id": "APP-002", "state": "CLAIMED", "progress": fresh},
                      {"id": "APP-003", "state": "AVAILABLE", "progress": ""}]}
    assert hasattr(MODULE, "pushed_progress"), "setup reads the task branch's pushed commits"
    MODULE.pushed_progress(runner, data)
    line = data["tasks"][0]["progress"]
    assert re.match(r"2 commit\(s\) pushed to feat/app-001 · last: [0-9a-f]{7,} work 2 \(\d+ (second|minute)s? ago\)$",
                    line), "the card shows the branch's pushed commits, not the older heartbeat: %r" % line
    assert data["tasks"][1]["progress"] == fresh, "a heartbeat newer than the branch stays as it is"
    assert data["tasks"][2]["progress"] == "", "a free task has no line"
    assert team.translated(line), "the line has Spanish: %r" % line
    out = run("return UAKWorkspace.t(%s);" % json.dumps(line), (), language="es")
    if out is not None:
        assert out.startswith("2 commit(s) subidos a feat/app-001 · último: ") and "hace" in out, out


TESTS = [publish_step_says_published, trusted_hides_the_open_claude_note, plan_says_how_long,
         check_timeout_names_the_step, commands_say_new_terminal, implementer_prompt_ships, card_counts_branch_commits]


def main():
    global MODULE, ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    root = args.package.resolve()
    ROOT = tf.ROOT = tr.ROOT = root
    for key in [k for k in os.environ if k.startswith("UAK_")]:
        del os.environ[key]  # the remote and base, and who acts, are the fixtures' own
    spec = importlib.util.spec_from_file_location("live_run_setup", root / ".uak/bin/lib/setup.py")
    MODULE = wizard.MODULE = team.MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)
    spec = importlib.util.spec_from_file_location("live_run_planning", root / ".uak/bin/lib/planning.py")
    tp.PLANNING = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tp.PLANNING)
    failed = 0
    saved = os.environ.get("CLAUDE_CONFIG_DIR")
    for test in TESTS:
        if args.case and test.__name__ not in args.case:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="uak-live-run-"))
        os.environ["CLAUDE_CONFIG_DIR"] = str(tmp / "no-claude-config")  # never the developer's own ~/.claude.json
        started = time.monotonic()
        try:
            test(root, tmp)
            print("PASS %s (%.1fs)" % (test.__name__, time.monotonic() - started))
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL %s: %s: %s" % (test.__name__, type(exc).__name__, str(exc)[:1500]))
        finally:
            if saved is None:
                os.environ.pop("CLAUDE_CONFIG_DIR", None)
            else:
                os.environ["CLAUDE_CONFIG_DIR"] = saved
            shutil.rmtree(str(tmp), ignore_errors=True)
    print("SETUP_LIVE_RUN_RESULT failed=%d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
