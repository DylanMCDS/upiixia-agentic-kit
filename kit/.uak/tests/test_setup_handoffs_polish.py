#!/usr/bin/env python3
"""UI-033: polish of UI-027's hand-offs. Fake claims records (by hand, as the engine leaves them), real HTTP and real
Git with a local bare remote; the page's own code runs in Node over a fake DOM of setup.html (test_setup_feedback).
Evidence (claude-Dylan-r's P3s on UI-027 at 6285def): the PR link accepted any https host, so an agent could store a
phishing link in claims; on the board the human-queue reason appeared twice (next step and hand-off box, against
"said once", A-F15); the close-old-session note picked the newest integrated task by string sort (APP-999 after
APP-1000) and stayed after later integrations while nothing was claimed."""
import argparse
import importlib.util
import inspect
import json
import os
import shutil
import tempfile
import time
from pathlib import Path

import test_setup_feedback as tf
import test_setup_handoffs as th
import test_setup_planning as tp
import test_setup_resume as tr
import test_setup_team as team
import test_setup_wizard as wizard

MODULE = None
PR = th.PR  # https://github.com/acme/app/pull/1
TIP = th.TIP
FORGE_LINE = ("Open its pull request on your forge (the recorded link does not point to this project's remote, so it "
              "is not shown).")


def records(pr=PR):
    """The claims records of one approved merge in the human queue, as read_claims builds them."""
    return {"tasks": {"APP-001": {"state": "REVIEW", "owner": "claude-ana", "pr": pr, "tip": TIP}},
            "queue": {"APP-001": {"state": "HUMAN", "reason": "Smoke failed: PRODUCT_UNVERIFIED"}},
            "reviews": {"APP-001": {"verdict": "approve", "sha": TIP}}}


# --- pr_link_must_match_origin_host -----------------------------------------------------------------------------------


def pr_link_must_match_origin_host(root, tmp):
    assert "origin" in inspect.signature(MODULE.human_queue).parameters, \
        "human_queue knows the origin remote's URL, to compare the PR link's host with it"
    home = tmp / "project"
    home.mkdir()

    def item(origin, pr=PR):
        return MODULE.human_queue(records(pr), home, "ana", origin=origin)[0]

    for origin in ("https://github.com/acme/app.git", "https://ana@GitHub.com/acme/app", "git@github.com:acme/app.git",
                   "ssh://git@github.com:22/acme/app.git", "https://github.com/acme/app.git\r\n"):
        got = item(origin)
        assert got.get("pr") == PR and not got.get("pr_elsewhere"), \
            "a PR on the origin's forge is a link (origin %r): %r" % (origin, got)
    for origin in ("https://gitlab.com/acme/app.git", "git@gitlab.com:acme/app.git", "ssh://git@bitbucket.org/acme/app",
                   ""):
        got = item(origin)
        assert got.get("pr") == "" and got.get("pr_elsewhere") is True, \
            "a PR on another host (origin %r) is no link: %r" % (origin, got)
    for pr in ("https://github.com.evil.example/acme/app/pull/1", "https://github.com@evil.example/acme/app/pull/1",
               "https://evil.example/github.com/acme/app/pull/1"):
        got = item("https://github.com/acme/app.git", pr)
        assert got.get("pr") == "" and got.get("pr_elsewhere") is True, "a look-alike host is no link: %r" % got
    unrecorded = item("https://github.com/acme/app.git", "")
    assert unrecorded.get("pr") == "" and not unrecorded.get("pr_elsewhere"), unrecorded

    # The server passes the origin remote's URL (git remote get-url, no network call) to both the team view and the
    # board: an origin on another forge drops the link in both.
    target, remote = team.ready_project(root, tmp)
    runner = team.Team()
    with tp.live(target, runner) as srv:
        runner.srv = srv
        team.ready_team(srv, target)
        th.human_queue_state(remote, tmp, TIP)
        assert hasattr(MODULE, "remote_url"), "one helper reads the origin remote's URL"
        real = MODULE.remote_url
        MODULE.remote_url = lambda git, name: "git@gitlab.com:acme/app.git" if real(git, name) is not None else None
        try:
            view, dash = th.fresh_views(srv)
        finally:
            MODULE.remote_url = real
    for where, item_ in (("team", (view.get("human_queue") or [{}])[0]),
                         ("board", ((dash.get("guidance") or {}).get("handoff") or {}))):
        assert item_.get("task") == "APP-001" and item_.get("pr") == "" and item_.get("pr_elsewhere") is True, \
            "the %s's hand-off has no link to another forge: %r" % (where, item_)
        assert PR not in json.dumps(item_), "the foreign link is not sent to the page at all: %r" % item_

    es = tf.catalog()
    assert es.get(FORGE_LINE), "Spanish for %r" % FORGE_LINE
    out = th.draw_handoff({"task": "APP-001", "plain": "", "pr": "", "pr_elsewhere": True, "approved": False,
                           "wait": th.WAIT, "integrate": ""})
    if out is not None:
        assert out["links"] == [] and PR not in out["text"], "no link at all: %r" % out
        assert es[FORGE_LINE] in out["text"], "the card says to open the PR on the forge: %r" % out["text"]


# --- queue_reason_said_once -------------------------------------------------------------------------------------------


def queue_reason_said_once(root, tmp):
    es = tf.catalog()
    home = tmp / "project"
    home.mkdir()
    item = MODULE.human_queue(records(), home, "ana", **({"origin": "https://github.com/acme/app.git"} if "origin" in
                              inspect.signature(MODULE.human_queue).parameters else {}))[0]
    plain = item.get("plain") or ""
    assert es.get(plain), "the reason has a Spanish sentence: %r" % plain
    guide = MODULE.guidance({"installed": True, "needs_human": [item]}, {})
    assert guide.get("kind") == "human" and guide.get("detail") == plain and guide.get("handoff"), guide
    script = tf.script(tf.page())
    assert "guide.detail" in tf.page_function(script, "drawAdvancedNext"), "the next step says the reason (detail)"
    out = th.run("""
        drawHandoffs(%s);
        drawHumanQueue([%s]);
        return {board: el("next-handoff").textContent, advanced: el("advanced-next-handoff").textContent,
                boardHidden: el("next-handoff").hidden, team: el("team-human-list").textContent};
    """ % (json.dumps(guide), json.dumps(item)), ("drawHandoff", "drawHandoffs", "drawHumanQueue"), language="es",
                 extra="function copyText() {}")
    if out is None:
        return
    assert not out["boardHidden"] and es["Open the pull request:"] in out["board"], "the board keeps the steps: %r" % out
    for where in ("board", "advanced"):
        assert es[plain] not in out[where], \
            "the %s's hand-off box does not repeat the reason its next step already says: %r" % (where, out[where])
    assert out["team"].count(es[plain]) == 1, "the team step's queue (no next-step text) says it once: %r" % out["team"]


# --- close_note_uses_latest_integration -------------------------------------------------------------------------------


def integrated(task, owner, updated):
    return "ID: %s\nState: INTEGRATED\nOwner: %s\nPR: %s\nTask-Tip: %s\nUpdated: %d\n" % (task, owner, PR, TIP, updated)


def close_note_uses_latest_integration(root, tmp):
    target, remote = team.ready_project(root, tmp)
    runner = team.Team(ready=team.READY_OUT.replace("APP-001", "APP-002"))
    seen = {}
    with tp.live(target, runner) as srv:
        runner.srv = srv
        team.ready_team(srv, target)
        # APP-1000 was integrated after APP-999: a string sort puts APP-999 last.
        th.write_claims(remote, tmp, {"tasks/APP-999.md": integrated("APP-999", "claude-ana", 1795000100),
                                      "tasks/APP-1000.md": integrated("APP-1000", "claude-ana", 1795000200)})
        seen["by_time"], _ = th.fresh_views(srv)
        th.write_claims(remote, tmp, {"tasks/APP-999.md": integrated("APP-999", "claude-ana", 1795000300)})
        seen["reversed"], _ = th.fresh_views(srv)
        # A later integration (someone else's) since the one the note announced: the note is old news.
        th.write_claims(remote, tmp, {"tasks/APP-1001.md": integrated("APP-1001", "codex-bob", 1795000400)})
        seen["later"], _ = th.fresh_views(srv)
        # The person claims again: the session moved on.
        th.write_claims(remote, tmp, {"tasks/APP-1001.md": integrated("APP-1001", "codex-bob", 1795000000),
                                      "claims/APP-1002.md": "ID: APP-1002\nState: CLAIMED\nOwner: claude-ana\n"})
        seen["claimed"], _ = th.fresh_views(srv)
    assert team.by_id(seen["by_time"]).get("implement", {}).get("task") == "APP-002", seen["by_time"].get("commands")
    assert seen["by_time"].get("next_after") == {"done": "APP-1000", "task": "APP-002"}, \
        "the note names the task integrated most recently by time: %r" % seen["by_time"].get("next_after")
    assert seen["reversed"].get("next_after") == {"done": "APP-999", "task": "APP-002"}, \
        "time decides, not the ID: %r" % seen["reversed"].get("next_after")
    assert not seen["later"].get("next_after"), \
        "a later integration hides the note: %r" % seen["later"].get("next_after")
    assert not seen["claimed"].get("next_after"), \
        "a new claim of the person hides the note: %r" % seen["claimed"].get("next_after")


TESTS = [pr_link_must_match_origin_host, queue_reason_said_once, close_note_uses_latest_integration]


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
    spec = importlib.util.spec_from_file_location("handoffs_polish_setup", root / ".uak/bin/lib/setup.py")
    MODULE = th.MODULE = wizard.MODULE = team.MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)
    spec = importlib.util.spec_from_file_location("handoffs_polish_planning", root / ".uak/bin/lib/planning.py")
    tp.PLANNING = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tp.PLANNING)
    failed = 0
    saved = os.environ.get("CLAUDE_CONFIG_DIR")
    for test in TESTS:
        if args.case and test.__name__ not in args.case:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="uak-handoffs-polish-"))
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
    print("SETUP_HANDOFFS_POLISH_RESULT failed=%d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
