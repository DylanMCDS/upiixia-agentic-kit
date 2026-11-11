"""Browser QA for UI-002: guided Beginner step, checklist, Your app link. Real install; `uak start` is scripted."""
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

TODO = ("OK    1. kit installed (sprint)\nOK    2. remote origin\nTODO  3. approve the plan: Backlog-Approved is not yes on main\n"
        "         set Backlog-Approved: yes in .uak/PROJECT.md and push it to main\n\nSTART · 1 thing to do.\n")


def run(command, cwd=None, timeout=120, **kwargs):
    if command[-1] == "start":
        return subprocess.CompletedProcess(command, 1, TODO, "")
    return wizard.run_command(command, cwd=cwd, timeout=timeout)


errors = []
with tempfile.TemporaryDirectory(prefix="uak-qa2-") as folder:
    target = Path(folder) / "hack project"
    target.mkdir()
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    server = wizard.make_server("", run=run)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/#%s" % (server.server_port, server.token)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720}, reduced_motion="reduce", locale="en-US")
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(url)
        page.click("#begin")
        page.fill("#target", str(target))
        page.click("#project-form button[type=submit]")
        page.check("input[name=mode][value=sprint]")
        for box in page.query_selector_all("input[name=harness]"):
            if box.is_checked():
                box.uncheck()
        page.check("input[name=harness][value=claude]")
        page.click("#workflow-form button[type=submit]")
        expect(page.locator("#summary")).to_contain_text("Claude Code")
        expect(page.locator("#summary")).to_contain_text(".mcp.json")
        page.click("#install")
        expect(page.locator("#result-title")).to_contain_text("installed", timeout=90000)
        page.click("#check")
        # D1: Configuration's headline is the gate's first step, not fixed text.
        expect(page.locator("#result-title")).to_contain_text("approve the plan", timeout=20000)
        page.click("#open-dashboard")
        expect(page.locator("#next-heading")).to_contain_text("approve the plan", timeout=20000)
        expect(page.locator("#beginner-why")).to_contain_text("Agents cannot start")
        expect(page.locator("#beginner-checklist")).to_contain_text("kit installed")
        expect(page.locator("#live-url-empty")).to_be_visible()
        expect(page.locator("#live-url-link")).to_be_hidden()
        primaries = page.locator("#beginner-step button.primary:visible").count()
        assert primaries == 1, "one primary action in the guided step, found %d" % primaries
        page.screenshot(path=str(SHOTS / "ui002-guided-1280.png"), full_page=True)
        # Save the deploy link in Configuration; the dashboard shows it as a safe link.
        page.click("#open-setup")
        page.fill("#live-url-input", "http://insecure.example.com")
        page.click("#save")
        expect(page.locator("#error")).to_contain_text("https://")
        page.fill("#live-url-input", "https://demo.example.com")
        page.click("#save")
        expect(page.locator("#save-status")).to_contain_text("saved", timeout=10000)
        assert "Live-URL: https://demo.example.com" in (target / ".uak/PROJECT.md").read_text(encoding="utf-8")
        page.click("#open-dashboard")
        link = page.locator("#live-url-link")
        expect(link).to_be_visible(timeout=20000)
        expect(link).to_have_attribute("href", "https://demo.example.com")
        expect(link).to_have_attribute("rel", "noopener noreferrer")
        page.screenshot(path=str(SHOTS / "ui002-yourapp-1280.png"), full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce", locale="es-MX")
        mobile.on("pageerror", lambda e: errors.append(str(e)))
        mobile.goto(url)
        mobile.click("#open-dashboard")
        expect(mobile.locator("#dashboard-shell")).to_be_visible()
        expect(mobile.locator("#live-url-link")).to_be_visible(timeout=20000)
        expect(mobile.locator("#your-app-heading")).to_have_text("Tu app")
        assert not mobile.evaluate("document.documentElement.scrollWidth > window.innerWidth"), "no overflow at 390"
        mobile.screenshot(path=str(SHOTS / "ui002-guided-es-390.png"), full_page=True)
        browser.close()
    server.shutdown()
print("QA_UI002 errors=%d %s" % (len(errors), errors[:5]))
print("QA_UI002_RESULT " + ("PASS" if not errors else "FAIL"))
