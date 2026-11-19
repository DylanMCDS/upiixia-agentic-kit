#!/usr/bin/env python3
"""UI-025: the team has its own tab, and the top bar stays visible.
Evidence: Dylan's live run (2026-11-19, turno-cafeteria-3): "Start your team" (reviewer registration, tools and roles,
the implement and review commands) was drawn inside "Dashboard", so the progress board and the team setup competed on
one long page; the top bar (logo, language, view, theme, tabs) scrolled away, so switching tabs needed a scroll to the
top. The page's own code runs in Node over a fake DOM of setup.html (test_setup_feedback); without Node the sources are
only read."""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import test_setup_feedback as tf
import test_setup_resume as tr

ROOT = None


def page():
    return tf.page()


def code():
    return tf.script(page())


def section(html, ident):
    return tr.section(html, ident)


def run(scenario, language="en"):
    """SCENARIO over the page's feedback and resume blocks plus the section code (openSection, the Team tab)."""
    node = shutil.which("node")
    if not node:
        print("  note: no Node.js here, so the page logic is checked by reading it only")
        return None
    html = page()
    script = tf.script(html)
    sources = [tr.shim(language), tf.lib("workspace.js"), tf.PRELUDE, tr.EXTRA,
               "var teamReady = false, teamTool = 'Claude Code', teamView = null, lastStepTitle = '', gone = false,"
               " loadTeamCalls = 0, loadDashboardCalls = 0;"
               " function loadTeam() { loadTeamCalls += 1; }"
               " function loadDashboard() { loadDashboardCalls += 1; }"]
    sources += [tf.page_function(script, name) for name in ("el", "isBusy", "operationBusy", "error", "api")]
    sources += [tf.block(script), tr.block(script)]
    sources += [tf.page_function(script, name) for name in ("openSection", "teamAvailable", "drawTeamTab", "openTeam",
                                                            "reviewerReady", "teamGuide", "drawNext",
                                                            "drawAdvancedNext")]
    with tempfile.TemporaryDirectory(prefix="uak-team-tab-js-") as folder:
        program = Path(folder) / "run.js"
        program.write_text(tf.NODE_PROGRAM, encoding="utf-8")
        done = subprocess.run([node, str(program)], input=json.dumps({"language": language, "sources": sources,
                                                                      "tree": tf.tree(html), "scenario": scenario,
                                                                      "reduced": False}),
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert done.returncode == 0, "the page logic runs: %s" % done.stderr[-2000:]
    return json.loads(done.stdout)


APPROVED = '{installed: true, phase: "setup", target: "/p/a", ready: true, resume: {step: "team", plan_approved: true}}'


def team_has_its_own_tab(root, tmp):
    html = page()
    header = html[html.index('<header class="header">'):html.index("</header>")]
    order = [header.find('id="%s"' % i) for i in ("open-setup", "open-team", "open-dashboard")]
    assert all(i >= 0 for i in order) and order == sorted(order), \
        "the header has Configuration, Team and Dashboard, in that order: %r" % order
    label = " ".join(re.sub(r"<[^>]+>", " ", section(html, "open-team")).split())
    assert label == "Team" and tf.catalog().get(label) == "Equipo", "the tab reads Team / Equipo: %r" % label
    shell = section(html, "team-shell")
    assert shell.startswith("<main") and "hidden" in shell[:shell.index(">")], "the Team tab is its own hidden <main>"
    team = section(html, "team-step")
    assert team in shell, "the whole team step lives in the Team tab"
    assert 'id="team-step"' not in section(html, "dashboard-shell"), "the dashboard no longer embeds the team step"
    for ident in ("team-reviewer", "team-register", "team-roles", "team-implement", "team-review", "team-two-people",
                  "team-implement-trust", "team-review-trust", "team-locked-why", "team-name-block"):
        assert 'id="%s"' % ident in team, "the team step keeps #%s" % ident
    script = code()
    assert re.search(r'el\("open-team"\)\.onclick = openTeam', script), "the Team button opens the Team tab"
    out = run("""
        state = %s;
        openSection("team");
        var shown = {setup: el("setup-shell").hidden, team: el("team-shell").hidden, dash: el("dashboard-shell").hidden,
                     pressed: ["open-setup", "open-team", "open-dashboard"].map(function (id) {
                       return el(id).getAttribute("aria-pressed"); }),
                     skip: document.querySelector(".skip").href};
        var saved = readSaved("/p/a");
        var land = landing(state, saved);
        openSection("dashboard");
        var back = {team: el("team-shell").hidden, dash: el("dashboard-shell").hidden};
        var calls = loadTeamCalls;
        openTeam();
        return {shown: shown, saved: saved.section, land: land, back: back, opened: !el("team-shell").hidden,
                loads: loadTeamCalls - calls, section: currentSection};
    """ % APPROVED)
    if out is None:
        return
    assert out["shown"] == {"setup": True, "team": False, "dash": True, "pressed": ["false", "true", "false"],
                            "skip": "#team-shell"}, out["shown"]
    assert out["saved"] == "team" and out["land"]["section"] == "team", "the active tab survives a reload: %r" % out
    assert out["back"] == {"team": True, "dash": False}, "leaving the tab hides it: %r" % out["back"]
    assert out["opened"] and out["section"] == "team" and out["loads"] == 1, "openTeam shows and loads it: %r" % out


def dashboard_shows_only_progress(root, tmp):
    html = page()
    dash = section(html, "dashboard-shell")
    for ident in ("simple-completed", "next-heading", "simple-tasks", "dashboard-freeze", "your-app", "advanced-next"):
        assert 'id="%s"' % ident in dash, "the dashboard keeps #%s" % ident
    for ident in ("team-register", "team-roles", "team-implement-command", "team-review-command"):
        assert 'id="%s"' % ident not in dash, "the dashboard has no team control #%s" % ident
    assert 'id="next-team"' in section(html, "beginner-step"), "the next step links to the Team tab"
    assert 'id="advanced-next-team"' in section(html, "advanced-next"), "so does the Advanced next step"
    script = code()
    for ident in ("next-team", "advanced-next-team"):
        assert re.search(r'el\("%s"\)\.onclick = openTeam' % ident, script), "#%s opens the Team tab" % ident
    es = tf.catalog()
    for text in ("Open the Team tab", "Next: register your reviewer in the Team tab.",
                 "Use the Team tab: its first command claims this task for {tool}."):
        assert text in es, "%r has a Spanish translation" % text
    assert "Start your team above" not in script, "no step points to a team block above that is not there"
    out = run("""
        state = %s;
        state.reviewer = {registered: false};
        state.completed = [];
        var ready = {kind: "ready", title: "Ready", detail: "Next: run this in your coding tool's terminal.",
                     commands: ["bash .uak/bin/wt new APP-001"], steps: []};
        teamView = {registered: {registered: false}, locked: {reason: "x"}};
        drawNext(ready);
        document.body.dataset.profile = "advanced";
        drawAdvancedNext(ready);
        var locked = {link: !el("next-team").hidden, adv: !el("advanced-next-team").hidden,
                      text: el("next-description").textContent, label: el("next-team").textContent};
        state.reviewer = {registered: true};
        teamView = {registered: {registered: true}};
        teamReady = true;
        drawNext(ready);
        var started = {link: !el("next-team").hidden, text: el("next-description").textContent,
                       box: !el("next-command-box").hidden};
        drawNext({kind: "todo", title: "Save your name", detail: "", commands: [], steps: []});
        var todo = !el("next-team").hidden;
        checksKey = "";
        drawChecks({ready: true, guidance: {commands: ["bash .uak/bin/wt new APP-001"]},
                    reviewer: {registered: false}, checks: []});
        var go = el("checks").querySelectorAll("button").filter(function (b) {
          return b.textContent === "Register the reviewer"; })[0];
        openSection("setup");
        go.onclick();
        return {locked: locked, started: started, todo: todo, after: currentSection};
    """ % APPROVED)
    if out is None:
        return
    assert out["locked"]["link"] and out["locked"]["adv"], "before the reviewer, both next steps link: %r" % out
    assert "Team tab" in out["locked"]["text"] and out["locked"]["label"] == "Open the Team tab", out["locked"]
    assert out["started"]["link"] and "Team tab" in out["started"]["text"] and not out["started"]["box"], \
        "once the team is started, the next step sends there instead of a second claim command: %r" % out["started"]
    assert not out["todo"], "a step that is not the team's has no Team link"
    assert out["after"] == "team", "Register the reviewer in the checklist opens the Team tab: %r" % out["after"]


def team_tab_waits_for_the_plan(root, tmp):
    html = page()
    shell = section(html, "team-shell")
    wait = section(html, "team-wait")
    assert wait in shell and shell.index('id="team-wait"') < shell.index('id="team-step"'), "the reason comes first"
    words = " ".join(re.sub(r"<[^>]+>", " ", wait).split())
    assert "plan is approved" in words and tf.catalog().get(words), "the reason is said, with Spanish: %r" % words
    assert "drawTeamTab(" in tf.page_function(code(), "render"), "every status redraws the tab's availability"
    out = run("""
        function look(data) {
          state = data;
          el("team-step").hidden = false;
          var calls = loadTeamCalls;
          openTeam();
          return {available: teamAvailable(data), wait: !el("team-wait").hidden, step: !el("team-step").hidden,
                  loads: loadTeamCalls - calls, why: el("open-team").getAttribute("aria-describedby")};
        }
        return {
          fresh: look({installed: false, phase: "welcome", resume: {}}),
          planning: look({installed: true, phase: "setup", ready: false, resume: {step: "plan", plan_approved: false}}),
          approved: look(%s),
          planOnly: teamAvailable({installed: true, phase: "setup", resume: {step: "team", plan_approved: true}}),
        };
    """ % APPROVED)
    if out is None:
        return
    for name in ("fresh", "planning"):
        assert out[name] == {"available": False, "wait": True, "step": False, "loads": 0, "why": "team-wait"}, \
            "%s: the tab says why it waits and loads nothing: %r" % (name, out[name])
    assert out["approved"] == {"available": True, "wait": False, "step": True, "loads": 1, "why": None}, out["approved"]
    assert out["planOnly"] is True, "an approved plan opens the tab"


def header_stays_visible(root, tmp):
    found = tf.rules(page())
    base = [b for s, b in found if re.fullmatch(r"\.header", s)]
    css = " ".join(base)
    assert re.search(r"position:\s*sticky", css) and re.search(r"top:\s*0\b", css), "the top bar is sticky: %r" % css
    z = re.search(r"z-index:\s*(\d+)", css)
    assert z and int(z.group(1)) > 0, "above the content: %r" % css
    bg = re.search(r"background(?:-color)?:\s*([^;]+)", css)
    assert bg and "transparent" not in bg.group(1), "with an opaque background: %r" % css
    assert re.search(r"box-shadow:[^;]*100vmax", css) and re.search(r"clip-path:\s*inset\(", css), \
        "the background spans the window without widening the page (no horizontal scroll at 390 px): %r" % css
    for s, b in found:
        if s.endswith(".header") and re.search(r"position:", b):
            assert re.search(r"position:\s*sticky", b), "no width turns the bar back to static: %s {%s}" % (s, b)
        if ".header" in s:
            assert "100vw" not in b, "no 100vw: the scrollbar would add a horizontal scroll: %s" % s
    toast = [b for s, b in found if s == ".toast"]
    gone = [b for s, b in found if s == ".server-gone"]
    skip = [b for s, b in found if s == ".skip:focus"]
    for name, rule in (("toast", toast), ("server-gone banner", gone), ("skip link", skip)):
        other = re.search(r"z-index:\s*(\d+)", " ".join(rule))
        assert other and int(other.group(1)) > int(z.group(1)), "the %s stays above the bar" % name
    pad = [b for s, b in found if re.fullmatch(r"html", s) and "scroll-padding-top" in b]
    assert pad, "a focused or pointed-to control is never hidden under the bar (scroll-padding-top)"


TESTS = [team_has_its_own_tab, dashboard_shows_only_progress, team_tab_waits_for_the_plan, header_stays_visible]


def main():
    global ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    root = args.package.resolve()
    ROOT = tf.ROOT = tr.ROOT = root
    failed = 0
    for test in TESTS:
        if args.case and test.__name__ not in args.case:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="uak-team-tab-"))
        try:
            test(root, tmp)
            print("PASS %s" % test.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL %s: %s: %s" % (test.__name__, type(exc).__name__, str(exc)[:1500]))
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)
    print("SETUP_TEAM_TAB_RESULT failed=%d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
