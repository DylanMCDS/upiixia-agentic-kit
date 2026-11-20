#!/usr/bin/env python3
"""UI-031: Team tab polish (follow-up of UI-025).
Evidence (claude-Dylan-r's P3s on UI-025 at da6df3b and on UI-024): a 400 from /api/team showed "Your team starts once
the plan is approved... Finish Configuration first" above the real reason although the plan was approved; at 390 px
the tab labels ended in "..." with no tooltip; the collapsed Technical details (#output) showed the engine's raw
"START READY · bash .uak/bin/wt new APP-001" before the reviewer was registered. The page's own code runs in Node over
a fake DOM of setup.html (the helpers of test_setup_feedback and test_setup_resume); without Node the sources are only
read."""
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
    """SCENARIO over the page's feedback and resume blocks plus the Team tab and Technical details code."""
    node = shutil.which("node")
    if not node:
        print("  note: no Node.js here, so the page logic is checked by reading it only")
        return None
    html = page()
    script = tf.script(html)
    sources = [tr.shim(language), tf.lib("workspace.js"), tf.PRELUDE, tr.EXTRA,
               "var teamReady = false, teamTool = 'Claude Code', teamView = null, lastStepTitle = '', gone = false,"
               " loadTeamCalls = 0, teamRefused = '';"
               " function loadTeam() { loadTeamCalls += 1; }"]
    sources += [tf.page_function(script, name) for name in ("el", "isBusy", "operationBusy", "error", "api")]
    sources += [tf.block(script), tr.block(script)]
    sources += [tf.page_function(script, name) for name in ("openSection", "teamAvailable", "drawTeamTab", "teamRefusal",
                                                            "openTeam", "reviewerReady", "tabTitles",
                                                            "technicalDetails")]
    with tempfile.TemporaryDirectory(prefix="uak-team-polish-js-") as folder:
        program = Path(folder) / "run.js"
        program.write_text(tf.NODE_PROGRAM, encoding="utf-8")
        done = subprocess.run([node, str(program)], input=json.dumps({"language": language, "sources": sources,
                                                                      "tree": tf.tree(html), "scenario": scenario,
                                                                      "reduced": False}),
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert done.returncode == 0, "the page logic runs: %s" % done.stderr[-2000:]
    return json.loads(done.stdout)


APPROVED = '{installed: true, phase: "setup", target: "/p/a", ready: true, resume: {step: "team", plan_approved: true}}'
PLANNING = '{installed: true, phase: "setup", target: "/p/a", ready: false, resume: {step: "plan", plan_approved: false}}'


def team_400_shows_only_its_reason(root, tmp):
    html = page()
    wait = section(html, "team-wait")
    assert 'id="team-wait-text"' in wait and 'id="team-why"' in wait, \
        "the wait sentence and the refusal's reason are separate parts of the tab's one notice"
    words = " ".join(re.sub(r"<[^>]+>", " ", section(html, "team-wait-text")).split())
    assert "plan is approved" in words and tf.catalog().get(words), "the wait sentence keeps its Spanish: %r" % words
    out = run("""
        function look(data, why) {
          state = data;
          teamRefused = "";
          openTeam();
          teamRefusal(why);
          return {notice: !el("team-wait").hidden, wait: !el("team-wait-text").hidden, why: !el("team-why").hidden,
                  text: el("team-why").textContent, step: !el("team-step").hidden,
                  described: el("open-team").getAttribute("aria-describedby")};
        }
        return {approved: look(%s, "Save your name first."), planning: look(%s, "Save your name first."),
                waiting: look(%s, "")};
    """ % (APPROVED, PLANNING, PLANNING), language="es")
    if out is None:
        return
    reason = tf.catalog().get("Save your name first.", "Save your name first.")
    assert out["approved"] == {"notice": True, "wait": False, "why": True, "text": reason, "step": False,
                               "described": "team-wait"}, \
        "an approved plan refused by a 400 shows only the reason, never the stale wait text: %r" % out["approved"]
    assert out["planning"]["wait"] and out["planning"]["why"], \
        "a plan really not approved still says why it waits, with the reason: %r" % out["planning"]
    assert out["waiting"]["wait"] and not out["waiting"]["why"], "no reason, no empty line: %r" % out["waiting"]


def short_tabs_have_full_titles(root, tmp):
    script = code()
    assert re.search(r"tabTitles\(\)", tf.page_function(script, "fitBar")), \
        "the titles follow every redraw of the bar (resize, language, the bar's own size)"
    out = run("""
        // The fake DOM has no TreeWalker: the labels are translated as UAKWorkspace.apply() does, one text at a time.
        ["open-setup", "open-team", "open-dashboard"].forEach(function (id) {
          el(id).textContent = "\\n  " + UAKWorkspace.t(el(id).textContent.trim()) + "\\n";
        });
        tabTitles();
        var es = ["open-setup", "open-team", "open-dashboard"].map(function (id) {
          return {title: el(id).getAttribute("title"), text: el(id).textContent.replace(/\\s+/g, " ").trim()};
        });
        return {es: es};
    """, language="es")
    if out is None:
        return
    es = tf.catalog()
    for item, english in zip(out["es"], ("Configuration", "Team", "Dashboard")):
        assert item["title"] == es[english], "the %s tab's title is its full Spanish label: %r" % (english, item)
        assert item["title"] == item["text"], "the title is the label's whole text: %r" % item


def technical_details_hide_claims_before_reviewer(root, tmp):
    render = tf.page_function(code(), "render")
    assert re.search(r'if \(data\.details && !reviewerReady\(\)\) el\("output"\)\.textContent = technicalDetails\(data\);',
                     render), "before the reviewer, Technical details are written through technicalDetails()"
    raw = ("OK    1. kit installed (sprint, uak 6.4.0)\\n"
           "\\nSTART READY · bash .uak/bin/wt new APP-001\\n"
           "NOTE  or let another agent take it: bash .uak/bin/wt new APP-002 --agent claude-ana\\n"
           "claude --permission-mode acceptEdits 'Implement APP-001'\\n"
           "codex exec 'Review APP-001'\\n")
    out = run("""
        var raw = "%s";
        function look(data, view) { state = data; teamView = view; return technicalDetails(data); }
        var named = look({details: raw, human: "ana", reviewer: {registered: false}}, null);
        var locked = look({details: raw, human: "ana", reviewer: {}},
                          {registered: {registered: false}, locked: {reason: "Register ana-r first (step 1): agents start only once a reviewer can review their work."}});
        var nameless = look({details: raw, reviewer: {}}, null);
        var ready = look({details: raw, human: "ana", reviewer: {registered: true}}, null);
        var empty = look({details: "", human: "ana", reviewer: {}}, null);
        return {named: named, locked: locked, nameless: nameless, ready: ready, empty: empty};
    """ % raw, language="es")
    if out is None:
        return
    reason = "Registra primero a ana-r (paso 1): los agentes empiezan solo cuando hay un revisor que pueda revisar su trabajo."
    for name in ("named", "locked", "nameless"):
        text = out[name]
        assert "wt new" not in text and "START READY" not in text, "%s: no claim command: %r" % (name, text)
        assert not re.search(r"(?m)^\s*(claude|codex|cursor-agent|gemini)\b", text), "%s: no agent launch: %r" % (name, text)
        assert "kit installed" in text, "%s: the rest of the output stays: %r" % (name, text)
    for name in ("named", "locked"):
        assert reason in out[name] and out[name].count(reason) == 1, \
            "%s: the Team tab's lock reason, once, in the page's language: %r" % (name, out[name])
    nameless = tf.catalog()["Next: register your reviewer in the Team tab."]
    assert nameless in out["nameless"], "without a name, the reviewer step is named: %r" % out["nameless"]
    assert "wt new APP-001" in out["ready"], "once the reviewer is registered, the engine's output is untouched"
    assert out["empty"] == "", "no output stays no output (render says so): %r" % out["empty"]


TESTS = [team_400_shows_only_its_reason, short_tabs_have_full_titles, technical_details_hide_claims_before_reviewer]


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
        tmp = Path(tempfile.mkdtemp(prefix="uak-team-polish-"))
        try:
            test(root, tmp)
            print("PASS %s" % test.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL %s: %s: %s" % (test.__name__, type(exc).__name__, str(exc)[:1500]))
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)
    print("SETUP_TEAM_POLISH_RESULT failed=%d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
