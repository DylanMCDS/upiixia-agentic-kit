#!/usr/bin/env python3
"""UI-027: the page walks the human through each hand-off of the first task. Real HTTP and real Git with a local bare
remote (the claims branch is written by hand, as the engine leaves it: the fake forge state of the human queue); the
page's own code runs in Node over a fake DOM of setup.html (test_setup_feedback), or is only read without Node.
Evidence (Dylan's live run 2026-11-19, turno-cafeteria-3; he had to ask the lead at every hand-off): (a) after publish
`git pull` said "There is no tracking information for the current branch"; (b) a merge in the human queue showed no
steps; (c) he merged PR #1 on GitHub before the reviewer approved it and nothing warned him; (d) when HACK-001 was
integrated and HACK-002 became free, nothing said that the running session sits in HACK-001's folder and a new
terminal is needed; (e) a freeze 25 minutes away was saved with no warning."""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
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
PR = "https://github.com/acme/app/pull/1"
TIP = "1f" * 20
OLD = "2e" * 20
WAIT = "Wait for the reviewer's approval before you merge."
WAIT_ES = "Espera la aprobación del revisor antes de hacer merge."


def run(scenario, functions, language="en", extra=""):
    """SCENARIO (an async function body) over workspace.js, the page's feedback and resume blocks and FUNCTIONS of the
    page, with a fetch the scenario controls. None without Node."""
    node = shutil.which("node")
    if not node:
        print("  note: no Node.js here, so the page logic is checked by reading it only")
        return None
    html = tf.page()
    script = tf.script(html)
    sources = [tr.shim(language), tf.lib("workspace.js"), tf.PRELUDE, tr.EXTRA, extra]
    sources += [tf.page_function(script, name) for name in ("el", "isBusy", "error", "api")]
    sources += [tf.block(script), tr.block(script)]
    sources += [tf.page_function(script, name) for name in functions]
    with tempfile.TemporaryDirectory(prefix="uak-handoffs-js-") as folder:
        program = Path(folder) / "run.js"
        program.write_text(tf.NODE_PROGRAM, encoding="utf-8")
        done = subprocess.run([node, str(program)], input=json.dumps({"language": language, "sources": sources,
                                                                      "tree": tf.tree(html), "scenario": scenario,
                                                                      "reduced": False}),
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert done.returncode == 0, "the page logic runs: %s" % done.stderr[-2000:]
    return json.loads(done.stdout)


def git(cwd, *args, check=True):
    return tp.git(cwd, *args, check=check)


def clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("UAK_")}


def write_claims(remote, tmp, files, remove=()):
    """FILES ({path: text}) on the remote's claims branch, as the engine would leave them."""
    work = Path(tempfile.mkdtemp(prefix="claims-edit-", dir=str(tmp)))
    git(tmp, "clone", "-q", "--branch", "claims", str(remote), str(work))
    for path, text in files.items():
        (work / path).parent.mkdir(parents=True, exist_ok=True)
        (work / path).write_text(text, encoding="utf-8")
    for path in remove:
        if (work / path).exists():
            git(work, "rm", "-q", "--", path)
    git(work, "add", "-A")
    git(work, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "fixture")
    git(work, "push", "-q", "origin", "claims")


def human_queue_state(remote, tmp, review_sha):
    files = {
        "tasks/APP-001.md": "ID: APP-001\nState: REVIEW\nOwner: claude-ana\nPR: %s\nTask-Tip: %s\n" % (PR, TIP),
        "queue/APP-001.md": "ID: APP-001\nState: HUMAN\nOwner: claude-ana\nUpdated: 1\n"
                            "Reason: Smoke failed: PRODUCT_UNVERIFIED (log: /home/ana/x.log)\n",
    }
    if review_sha:
        files["reviews/APP-001.md"] = "ID: APP-001\nVerdict: approve\nReviewer: ana-r\nSHA: %s\nReviewed: 1\n" % review_sha
    write_claims(remote, tmp, files)


def fresh_views(srv):
    """The team view and the dashboard, read again from the remote (no 15 s cache in between)."""
    with srv.lock:
        srv.remote_cache.clear()
        srv.team_cache.clear()
    status, view = tp.get(srv, "/api/team")
    assert status == 200, view
    status, dash = tp.get(srv, "/api/dashboard")
    assert status == 200, dash
    return view, dash


def draw_handoff(item, language="es"):
    return run("""
        var copied = [];
        copyText = function (text) { copied.push(text); };
        var box = el("next-handoff");
        drawHandoff(box, %s);
        var links = box.querySelectorAll("a"), codes = box.querySelectorAll("code"), buttons = box.querySelectorAll("button");
        buttons.forEach(function (b) { b.onclick(); });
        return {hidden: box.hidden, text: box.textContent, links: links.map(function (a) { return a.getAttribute("href"); }),
                codes: codes.map(function (c) { return c.textContent; }),
                buttons: buttons.map(function (b) { return b.textContent; }), copied: copied};
    """ % json.dumps(item), ("drawHandoff",), language=language, extra="function copyText() {}")


# --- publish_sets_upstream --------------------------------------------------------------------------------------------


def publish_sets_upstream(root, tmp):
    target, remote = prep.installed(root, tmp)
    with tp.live(target, tp.FakePlanner()) as srv:
        prep.ready_to_publish(srv, target)
        prep.publish(srv)
    head = prep.remote_head(remote)
    assert head, "the kit reached origin's main"
    assert git(target, "config", "--get", "branch.main.remote", check=False) == "origin", \
        "publish sets main's upstream remote"
    assert git(target, "config", "--get", "branch.main.merge", check=False) == "refs/heads/main", \
        "publish sets main's upstream branch"
    pulled = subprocess.run([resolve_binary("git"), "-C", str(target), "pull", "-q", "--ff-only"], capture_output=True,
                            text=True, env=clean_env())
    assert pulled.returncode == 0, "a plain git pull works after publishing: %s" % (pulled.stderr or pulled.stdout)
    # An upstream the person set already is theirs: publishing never rewrites it.
    target2, remote2 = prep.installed(root, team.fresh(tmp, "second"), name="kept upstream")
    git(target2, "config", "branch.main.remote", "origin")
    git(target2, "config", "branch.main.merge", "refs/heads/trunk")
    with tp.live(target2, tp.FakePlanner()) as srv:
        prep.ready_to_publish(srv, target2)
        prep.publish(srv)
    assert git(target2, "config", "--get", "branch.main.merge", check=False) == "refs/heads/trunk", \
        "an existing upstream is kept"


# --- human_queue_shows_steps ------------------------------------------------------------------------------------------


def human_queue_shows_steps(root, tmp):
    target, remote = team.ready_project(root, tmp)
    home = team.physical(target)
    command = "cd %s && UAK_HUMAN=ana bash .uak/bin/uak integrate APP-001" % team.q(home)
    runner = team.Team()
    with tp.live(target, runner) as srv:
        runner.srv = srv
        team.ready_team(srv, target)
        human_queue_state(remote, tmp, TIP)
        view, dash = fresh_views(srv)
    queue = view.get("human_queue") or []
    assert [i.get("task") for i in queue] == ["APP-001"], "the team step lists the human queue: %r" % view.get("human_queue")
    item = queue[0]
    assert item.get("pr") == PR and item.get("approved") is True, item
    assert item.get("integrate") == command, "the exact integrate command for a normal terminal: %r" % item
    assert "/home/ana" not in json.dumps(item), "no absolute path from the engine's reason: %r" % item
    assert team.translated(item.get("plain", "")), "the reason is a plain sentence with Spanish: %r" % item
    guide = dash.get("guidance") or {}
    assert guide.get("kind") == "human" and (guide.get("handoff") or {}).get("integrate") == command, \
        "the board's next step carries the same steps: %r" % guide
    assert ((dash.get("needs_human") or [{}])[0]).get("pr") == PR, dash.get("needs_human")

    html = tf.page()
    es = tf.catalog()
    script = tf.script(html)
    assert re.search(r"drawHandoff\(el\(\"next-handoff\"\)", tf.page_function(script, "drawHandoffs")), \
        "the board's next step draws the hand-off"
    for caller in ("drawDashboard", "drawTeam"):
        assert "drawHandoffs(" in tf.page_function(script, caller), "%s draws the board's hand-off" % caller
    assert "drawHumanQueue(" in tf.page_function(script, "drawTeam"), "the team step draws the human queue"
    assert 'id="team-human"' in html and 'id="next-handoff"' in html, "both places have a hand-off box"
    for line in ("Open the pull request:", "Merge it there, on GitHub.",
                 "Then record the merge: paste this in a new terminal, not inside Claude or Codex."):
        assert es.get(line), "Spanish for %r" % line
    out = draw_handoff(item)
    if out is not None:
        assert not out["hidden"] and out["links"] == [PR], "the PR is a link: %r" % out
        assert out["codes"] == [PR, command] or out["codes"] == [command], out
        assert out["copied"] == [PR, command], "Copy buttons for the PR link and the integrate command: %r" % out
        assert all(b == "Copiar" for b in out["buttons"]), out
        for line in ("Open the pull request:", "Merge it there, on GitHub.",
                     "Then record the merge: paste this in a new terminal, not inside Claude or Codex."):
            assert es[line] in out["text"], "the step %r shows in Spanish: %r" % (line, out["text"])
        assert out["text"].index(es["Open the pull request:"]) < out["text"].index(es["Merge it there, on GitHub."]) \
            < out["text"].index(command), "in the order they happen: %r" % out["text"]
        assert es[item["plain"]] in out["text"], "the reason in Spanish: %r" % out["text"]
    lists = run("""
        drawHumanQueue([%s]);
        return {hidden: el("team-human").hidden, items: el("team-human-list").querySelectorAll("li").length};
    """ % json.dumps(item), ("drawHumanQueue", "drawHandoff"), language="es", extra="function copyText() {}")
    if lists is not None:
        assert lists == {"hidden": False, "items": 1}, lists
        empty = run("drawHumanQueue([]); return el('team-human').hidden;", ("drawHumanQueue", "drawHandoff"))
        assert empty is True, "no queue, no block"


# --- no_integrate_before_approval -------------------------------------------------------------------------------------


def no_integrate_before_approval(root, tmp):
    target, remote = team.ready_project(root, tmp)
    runner = team.Team()
    with tp.live(target, runner) as srv:
        runner.srv = srv
        team.ready_team(srv, target)
        seen = []
        human_queue_state(remote, tmp, OLD)  # approved an earlier SHA
        seen.append(fresh_views(srv))
        write_claims(remote, tmp, {}, remove=("reviews/APP-001.md",))  # then no review at all
        seen.append(fresh_views(srv))
    for view, dash in seen:
        item = (view.get("human_queue") or [{}])[0]
        assert item.get("task") == "APP-001" and item.get("approved") is False, item
        assert not item.get("integrate") and "uak integrate" not in json.dumps(view), \
            "no integrate command before the approval: %r" % item
        assert item.get("pr") == PR, "the PR can still be read: %r" % item
        handoff = (dash.get("guidance") or {}).get("handoff") or {}
        assert handoff.get("approved") is False and not handoff.get("integrate"), handoff
        assert "uak integrate" not in json.dumps(dash.get("guidance")), dash.get("guidance")
    es = tf.catalog()
    assert es.get(WAIT) == WAIT_ES, "the wait line has its Spanish pair: %r" % es.get(WAIT)
    out = draw_handoff((seen[0][0].get("human_queue") or [{}])[0])
    if out is not None:
        assert WAIT_ES in out["text"], "the card says to wait for the approval: %r" % out["text"]
        assert "uak integrate" not in out["text"] and es["Merge it there, on GitHub."] not in out["text"], \
            "no merge step and no integrate command: %r" % out
        assert out["links"] == [PR], out


# --- next_task_needs_new_terminal -------------------------------------------------------------------------------------


def next_task_needs_new_terminal(root, tmp):
    target, remote = team.ready_project(root, tmp)
    runner = team.Team(ready=team.READY_OUT.replace("APP-001", "APP-002"))
    with tp.live(target, runner) as srv:
        runner.srv = srv
        team.ready_team(srv, target)
        write_claims(remote, tmp, {"tasks/APP-001.md": "ID: APP-001\nState: INTEGRATED\nOwner: claude-ana\nPR: %s\n"
                                                        "Task-Tip: %s\n" % (PR, TIP)})
        view, _ = fresh_views(srv)
        # Someone else's integrated task is not this person's session.
        write_claims(remote, tmp, {"tasks/APP-001.md": "ID: APP-001\nState: INTEGRATED\nOwner: codex-bob\n"})
        other, _ = fresh_views(srv)
    assert team.by_id(view).get("implement", {}).get("task") == "APP-002", view.get("commands")
    assert view.get("next_after") == {"done": "APP-001", "task": "APP-002"}, \
        "the team step knows the old session's task and the next one: %r" % view.get("next_after")
    assert not other.get("next_after"), other.get("next_after")
    es = tf.catalog()
    line = ("{done} is integrated: its agent session (in {done}'s folder) can be closed: type /exit there. {task} starts "
            "with the command below, in a new terminal.")
    assert es.get(line), "Spanish for %r" % line
    assert "drawNextTask(" in tf.page_function(tf.script(tf.page()), "drawTeam"), "the team step draws it"
    out = run("""
        drawNextTask(%s);
        var shown = {hidden: el("team-next-task").hidden, text: el("team-next-task").textContent};
        drawNextTask({});
        shown.after = el("team-next-task").hidden;
        return shown;
    """ % json.dumps(view), ("drawNextTask",), language="es")
    if out is not None:
        assert not out["hidden"] and out["after"], out
        text = out["text"]
        assert "APP-001" in text and "APP-002" in text and "/exit" in text and "terminal nueva" in text, text
    html = tf.page()
    block = tr.section(html, "team-implement")
    assert block.index('id="team-next-task"') < block.index('id="team-implement-command"'), \
        "the note sits above the next task's command"


# --- near_freeze_asks_first -------------------------------------------------------------------------------------------


def near_freeze_asks_first(root, tmp):
    html = tf.page()
    es = tf.catalog()
    script = tf.script(html)
    assert "window.confirm" not in script and not re.search(r"[^.\w]confirm\(", script), \
        "the question is on the page, not a browser dialog an embedded browser may skip"
    form = tr.section(html, "schedule-form")
    assert 'id="schedule-confirm"' in form, "the question sits in the schedule step"
    for line in ("That freeze is in the past or less than an hour away. Save it anyway?", "Save anyway",
                 "Change the dates", "Freeze: {freeze}"):
        assert es.get(line), "Spanish for %r" % line
    assert re.search(r'el\("schedule-confirm-save"\)\.onclick = confirmSchedule', script), "Save anyway saves"
    assert re.search(r'el\("schedule-confirm-cancel"\)\.onclick = cancelSchedule', script), "Change the dates goes back"
    assert "saveSchedule(" in script[script.index('el("schedule-form").onsubmit'):][:1200], "the form saves through it"
    out = run("""
        var calls = [], soon = true;
        api = function (path, body) {
          calls.push(path + (body && body.preview ? ":preview" : ""));
          if (body && body.preview)
            return Promise.resolve({soon: soon, freeze: "Thu 10:35", epoch: 1, freeze_at: "Thu 2026-11-19 10:35"});
          return Promise.resolve({freeze_at: "Thu 2026-11-19 10:35", first_claim_at: "Thu 2026-11-19 08:30"});
        };
        startCheck = function () {}; refresh = async function () {}; dropDrafts = function () {};
        var body = {start: "2026-11-19 08:00", end: "2026-11-19 11:00", zone: "UTC"};
        var first = await saveSchedule(body);
        var asked = {result: first, shown: !el("schedule-confirm").hidden, when: el("schedule-confirm-when").textContent,
                     text: el("schedule-confirm-text").textContent, calls: calls.slice()};
        cancelSchedule();
        var cancelled = {hidden: el("schedule-confirm").hidden, calls: calls.slice()};
        calls.length = 0;
        await saveSchedule(body, true);
        var saved = {calls: calls.slice(), hidden: el("schedule-confirm").hidden};
        calls.length = 0; soon = false;
        await saveSchedule(body);
        var far = {calls: calls.slice(), hidden: el("schedule-confirm").hidden};
        return {asked: asked, cancelled: cancelled, saved: saved, far: far};
    """, ("saveSchedule", "askSchedule", "cancelSchedule"), language="es",
        extra="function startCheck() {} function dropDrafts() {} function refresh() {} var checkRequested = false,"
              " scheduleBody = null;")
    if out is None:
        return
    asked = out["asked"]
    assert asked["result"] is False and asked["shown"], "a near freeze asks first: %r" % asked
    assert asked["calls"] == ["schedule:preview"], "nothing is written before the answer: %r" % asked
    assert "2026-11-19 10:35" in asked["when"] and es["Freeze: {freeze}"].split("{")[0] in asked["when"], \
        "it states the freeze time: %r" % asked
    assert asked["text"] == es["That freeze is in the past or less than an hour away. Save it anyway?"], asked
    assert out["cancelled"] == {"hidden": True, "calls": ["schedule:preview"]}, out["cancelled"]
    assert out["saved"]["calls"][:1] == ["schedule"] and out["saved"]["hidden"], "Save anyway writes it: %r" % out["saved"]
    assert out["far"]["calls"][:2] == ["schedule:preview", "schedule"] and out["far"]["hidden"], \
        "a later freeze saves without asking: %r" % out["far"]


TESTS = [publish_sets_upstream, human_queue_shows_steps, no_integrate_before_approval, next_task_needs_new_terminal,
         near_freeze_asks_first]


def main():
    global MODULE
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    root = args.package.resolve()
    tf.ROOT = tr.ROOT = root
    for key in [k for k in os.environ if k.startswith("UAK_")]:
        del os.environ[key]  # the remote and base, and who acts, are the fixtures' own
    spec = importlib.util.spec_from_file_location("handoffs_setup", root / ".uak/bin/lib/setup.py")
    MODULE = wizard.MODULE = team.MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)
    spec = importlib.util.spec_from_file_location("handoffs_planning", root / ".uak/bin/lib/planning.py")
    tp.PLANNING = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tp.PLANNING)
    failed = 0
    saved = os.environ.get("CLAUDE_CONFIG_DIR")
    for test in TESTS:
        if args.case and test.__name__ not in args.case:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="uak-handoffs-"))
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
    print("SETUP_HANDOFFS_RESULT failed=%d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
