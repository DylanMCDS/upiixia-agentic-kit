"""Browser QA for UI-001 guidance: real install in a disposable repo; `uak start` output is scripted."""
import importlib.util
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

WORKTREE = Path(sys.argv[1])
SHOTS = Path(sys.argv[2])
SHOTS.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("wizard", WORKTREE / "kit/.uak/bin/lib/setup.py")
wizard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wizard)

TODO = ("OK    1. kit installed (sprint)\nTODO  2. approve the plan: Backlog-Approved is not yes on main\n"
        "         set Backlog-Approved: yes in .uak/PROJECT.md and push it to main\n\n"
        "START · 1 thing to do before the first claim. Then run uak start again.\n")
READY = "OK    1. kit installed (sprint)\nOK    2. plan approved\n\nSTART READY · bash .uak/bin/wt new APP-001   (branch + worktree + claim; then your agent in it)\n"
script = {"start": TODO}


def run(command, cwd=None, timeout=120, **kwargs):
    if command[-1] == "start":
        out = script["start"]
        return subprocess.CompletedProcess(command, 0 if "START READY" in out else 1, out, "")
    return wizard.run_command(command, cwd=cwd, timeout=timeout)


errors = []
with tempfile.TemporaryDirectory(prefix="uak-qa-") as folder:
    target = Path(folder) / "hack project"
    target.mkdir()
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    server = wizard.make_server("", run=run)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/#%s" % (server.server_port, server.token)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge", headless=True)
        for width, height in ((1280, 720), (390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce",
                                    locale="en-US")
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.goto(url)
            if width == 1280:
                page.click("#begin")
                page.fill("#target", str(target))
                page.click("#project-form button[type=submit]")
                page.check("input[name=mode][value=sprint]")
                for box in page.query_selector_all("input[name=harness]"):
                    if box.is_checked():
                        box.uncheck()
                page.check("input[name=harness][value=claude]")
                page.click("#workflow-form button[type=submit]")
                page.click("#install")
                expect(page.locator("#result-title")).to_contain_text("installed", timeout=90000)
                # Blocked: the dashboard's step is the gate's first TODO, never "Start the next task".
                page.click("#check")
                expect(page.locator("#checks")).to_contain_text("approve the plan", timeout=20000)
                page.click("#open-dashboard")
                expect(page.locator("#next-heading")).to_contain_text("approve the plan", timeout=20000)
                expect(page.locator("#next-steps")).to_contain_text("Backlog-Approved: yes")
                expect(page.locator("#next-command-box")).to_be_hidden()
                assert "Start the next task" not in page.inner_text("#next-heading")
                page.screenshot(path=str(SHOTS / "guidance-todo-1280.png"), full_page=True)
                # Ready: the check started from the dashboard returns there with the exact command.
                script["start"] = READY
                page.click("#next-check")
                try:
                    expect(page.locator("#next-heading")).to_contain_text("Start the next task", timeout=20000)
                except AssertionError:
                    print("DEBUG state", {k: server.state.get(k) for k in ("phase", "ready", "next_command", "error")})
                    print("DEBUG status", page.inner_text("#dashboard-status"))
                    print("DEBUG disabled", page.is_disabled("#next-check"), "errors", errors)
                    raise
                expect(page.locator("#next-command")).to_have_text("bash .uak/bin/wt new APP-001")
                expect(page.locator("#next-command-box")).to_be_visible()
                page.screenshot(path=str(SHOTS / "guidance-ready-1280.png"), full_page=True)
                # From Configuration: a ready check opens project progress by itself.
                page.click("#open-setup")
                page.click("#check")
                expect(page.locator("#dashboard-shell")).to_be_visible(timeout=20000)
            else:
                page.click("#open-dashboard")
                try:
                    expect(page.locator("#next-heading")).to_contain_text("Start the next task", timeout=20000)
                except AssertionError:
                    print("DEBUG390 heading", page.inner_text("#next-heading"), "|", page.inner_text("#dashboard-status"),
                          "| visible", page.is_visible("#open-dashboard"), {k: server.state.get(k) for k in ("phase", "ready")})
                    page.screenshot(path=str(SHOTS / "debug-390.png"), full_page=True)
                    raise
                expect(page.locator("#dashboard-shell")).to_be_visible()
                expect(page.locator("#next-heading")).to_be_visible()
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                assert not overflow, "no horizontal scroll at 390px"
                page.screenshot(path=str(SHOTS / "guidance-ready-390.png"), full_page=True)
            page.close()
        browser.close()
    server.shutdown()
print("QA_GUIDANCE errors=%d %s" % (len(errors), errors[:5]))
print("QA_GUIDANCE_RESULT " + ("PASS" if not errors else "FAIL"))
