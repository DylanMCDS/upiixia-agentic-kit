#!/usr/bin/env python3
"""UAK-100: an idle agent stops instead of paying for empty waits. Evidence (2026-11-19, the kit's own repo): a Codex
session blocked on a human authorization ran about 200 `uak wait --for message --timeout 540` cycles over 9 h (757
model turns, about 129M cached input tokens): every timeout printed "run the same wait again" and the idle lines of
`uak next` said "wait for a message". Now the third empty wait in a row prints IDLE_STOP (exit 5), an event resets the
count, no idle line says to wait again, a loop the human started (UAK_LOOP=1) keeps its pacing, and IDLE_STOP names the
human act the agent is blocked on. Real Git, a local bare remote, a 2-s timeout."""
import argparse
import concurrent.futures
import re
import tempfile
import threading
import time
from pathlib import Path

from test_hack import Runner, expect, resolve_binary

# What sent the Codex session back into the loop.
AGAIN = re.compile(r"wait again|same wait|rerun|re-run|keep waiting|wait for a message|wait --for message|wait for one|"
                   r"run .*uak wait.* again", re.I)


def env(agent, **extra):
    # Never inherit the caller's identity, base or loop mode (UAK_BASE in the shell broke tests before).
    e = {"UAK_AGENT": agent, "UAK_HUMAN": "", "UAK_REMOTE": "origin", "UAK_DEDUPE": "off", "UAK_WAIT_EVERY": "1",
         "UAK_LOOP": "", "UAK_BASE": "", "UAK_TASK": ""}
    e.update(extra)
    return e


def empty_wait(r, cwd, agent="agent-2", **extra):
    out = r.run([r.bash, ".uak/bin/uak", "wait", "--for", "message", "--timeout", "2"], cwd=cwd, env=env(agent, **extra), allowed=None)
    return out.returncode, out.stdout + out.stderr


def third_empty_wait_says_stop(r):
    f = r.fixture("idle-third", count=2)
    got = [empty_wait(r, f.clones[1]) for _ in range(3)]
    for rc, text in got[:2]:
        expect(rc == 4 and "WAIT_TIMEOUT" in text and "IDLE_STOP" not in text, "the first two empty waits time out: rc %d %s" % (rc, text[-500:]))
    rc, text = got[2]
    expect(rc == 5, "the third empty wait in a row exits 5: rc %d %s" % (rc, text[-500:]))
    expect(re.search(r"IDLE_STOP: nothing happened in [0-9]+ min\. End your turn now and stop; a human or the lead restarts you with a message", text),
           "IDLE_STOP line: " + text[-500:])
    # Per identity: another identity on the same clone starts from zero.
    rc, text = empty_wait(r, f.clones[1], agent="agent-9")
    expect(rc == 4 and "IDLE_STOP" not in text, "another identity has its own count: rc %d %s" % (rc, text[-400:]))
    return "4, 4, 5; another identity 4"


def event_resets_the_idle_count(r):
    f = r.fixture("idle-reset", count=2)
    for _ in range(2):
        rc, text = empty_wait(r, f.clones[1])
        expect(rc == 4, "empty wait: rc %d %s" % (rc, text[-400:]))
    box = {}

    def waiter():
        out = r.run([r.bash, ".uak/bin/uak", "wait", "--for", "message", "--timeout", "40"], cwd=f.clones[1], env=env("agent-2"), allowed=None)
        box["out"] = (out.returncode, out.stdout + out.stderr)
    t = threading.Thread(target=waiter)
    t.start()
    time.sleep(4)
    f.hack(0, "msg", "agent-2", "the contract is ready", now=int(time.time()))
    t.join(60)
    expect("out" in box, "the wait returned")
    rc, text = box["out"]
    expect(rc == 0 and "the contract is ready" in text, "a message wakes the wait: rc %d %s" % (rc, text[-400:]))
    for i in range(2):
        rc, text = empty_wait(r, f.clones[1])
        expect(rc == 4 and "IDLE_STOP" not in text, "after an event the count restarts (wait %d): rc %d %s" % (i + 1, rc, text[-400:]))
    # A claim also counts as something happening.
    f.claim(1, "HACK-002", now=int(time.time()))
    rc, text = empty_wait(r, f.clones[1])
    expect(rc == 4 and "IDLE_STOP" not in text, "after a claim the count restarts: rc %d %s" % (rc, text[-400:]))
    rc, text = empty_wait(r, f.clones[1])
    expect(rc == 4, "second empty wait after the claim: rc %d %s" % (rc, text[-400:]))
    rc, text = empty_wait(r, f.clones[1])
    expect(rc == 5 and "IDLE_STOP" in text, "three empty waits after the claim stop: rc %d %s" % (rc, text[-400:]))
    return "message and claim reset"


def idle_lines_never_say_wait_again(r):
    f = r.fixture("idle-lines", paths={"HACK-001": "src/one.txt"}, count=2)
    lines = {}
    _, lines["wait timeout"] = empty_wait(r, f.clones[1])
    f.claim(0, "HACK-001")
    out = r.run([r.bash, ".uak/bin/uak", "next"], cwd=f.clones[1], env=env("idle-1"), allowed=None)
    lines["next idle"] = out.stdout + out.stderr
    f.hack(0, "register-reviewer", "agent-2", human=True)
    out = r.run([r.bash, ".uak/bin/uak", "next"], cwd=f.clones[1], env=env("agent-2"), allowed=None)
    lines["reviewer next"] = out.stdout + out.stderr
    expect("Nothing to review right now" in lines["reviewer next"], "reviewer line: " + lines["reviewer next"][-500:])
    expect("Idle:" in lines["next idle"], "idle line: " + lines["next idle"][-500:])
    for key, text in lines.items():
        bad = [l for l in text.splitlines() if AGAIN.search(l)]
        expect(not bad, "%s tells the agent to wait again: %s" % (key, bad))
        expect(re.search(r"end your turn", text, re.I), "%s says to end the turn: %s" % (key, text[-500:]))
    expect("--for approve" in lines["wait timeout"], "the timeout keeps one bounded wait for a specific event: " + lines["wait timeout"][-400:])
    return "wait timeout, next idle, reviewer next"


def loop_mode_keeps_waiting(r):
    f = r.fixture("idle-loop", count=2)
    for i in range(4):
        rc, text = empty_wait(r, f.clones[1], UAK_LOOP="1")
        expect(rc == 4 and "IDLE_STOP" not in text, "UAK_LOOP=1 keeps its pacing (wait %d): rc %d %s" % (i + 1, rc, text[-400:]))
    # The count did not grow in loop mode: out of it, the cap starts from zero.
    rc, text = empty_wait(r, f.clones[1])
    expect(rc == 4, "first capped wait after the loop: rc %d %s" % (rc, text[-400:]))
    doc = (r.package / ".uak/docs/LOOPS.md").read_text(encoding="utf-8")
    expect("UAK_LOOP=1" in doc and "IDLE_STOP" in doc, "LOOPS.md documents the cap and the loop mode")
    return "4 loop waits, no stop"


def idle_stop_names_the_human_blocker(r):
    f = r.fixture("idle-human", count=2)
    r.run([r.bash, ".uak/bin/uak", "msg", "human", "please authorize the deploy of HACK-002"], cwd=f.clones[1],
          env=env("agent-2", UAK_NOW=str(int(time.time()))))
    got = [empty_wait(r, f.clones[1]) for _ in range(3)]
    rc, text = got[2]
    line = [l for l in text.splitlines() if l.startswith("IDLE_STOP")]
    expect(rc == 5 and line, "IDLE_STOP after three empty waits: rc %d %s" % (rc, text[-500:]))
    expect("please authorize the deploy of HACK-002" in line[0] and "human" in line[0].lower(),
           "the IDLE_STOP line names the human act it waits on: " + line[0])
    # Without such a message the line names no blocker.
    g = r.fixture("idle-nohuman", count=2)
    text = [empty_wait(r, g.clones[1]) for _ in range(3)][2][1]
    expect("authorize" not in text and "Blocked on" not in text, "no blocker without a message to human: " + text[-400:])
    return "blocker named"


def message_between_waits_resets_the_count(r):
    """Review of 00a9fd3 (claude-Dylan-r): a message that arrives between two waits, read with inbox --ack, is an event."""
    f = r.fixture("idle-between", count=2)
    for _ in range(2):
        rc, text = empty_wait(r, f.clones[1])
        expect(rc == 4, "empty wait: rc %d %s" % (rc, text[-400:]))
    f.hack(0, "msg", "agent-2", "between the waits", now=int(time.time()))
    r.run([r.bash, ".uak/bin/uak", "inbox", "--ack"], cwd=f.clones[1], env=env("agent-2"))
    rc, text = empty_wait(r, f.clones[1])
    expect(rc == 4 and "IDLE_STOP" not in text, "a message between waits restarts the count: rc %d %s" % (rc, text[-400:]))
    return "reset by a message between waits"


def idle_stop_starts_the_count_over(r):
    """After IDLE_STOP a restarted agent keeps its bounded wait: the count starts over."""
    f = r.fixture("idle-over", count=2)
    got = [empty_wait(r, f.clones[1])[0] for _ in range(3)]
    expect(got == [4, 4, 5], "4, 4, 5 first: %s" % got)
    got = [empty_wait(r, f.clones[1]) for _ in range(3)]
    expect([g[0] for g in got] == [4, 4, 5], "after IDLE_STOP the count starts over: %s" % [g[0] for g in got])
    expect(re.search(r"nothing happened in 0 min", got[2][1]), "N min counts from the new first wait: " + got[2][1][-300:])
    return "4, 4, 5, 4, 4, 5"


def blocker_text_has_no_control_characters(r):
    f = r.fixture("idle-ctrl", count=2)
    r.run([r.bash, ".uak/bin/uak", "msg", "human", "allow \x1b[31mHACK-002\x1b[0m\tnow"], cwd=f.clones[1],
          env=env("agent-2", UAK_NOW=str(int(time.time()))))
    text = [empty_wait(r, f.clones[1]) for _ in range(3)][2][1]
    line = [l for l in text.splitlines() if l.startswith("IDLE_STOP")]
    expect(line and "HACK-002" in line[0], "IDLE_STOP names the blocker: " + text[-400:])
    expect(not re.search(r"[\x00-\x1f\x7f]", line[0]), "no control characters in the line: %r" % line[0])
    return "clean"


def json_reports_idle_stop(r):
    f = r.fixture("idle-json", count=2)
    for _ in range(2):
        empty_wait(r, f.clones[1])
    out = r.run([r.bash, ".uak/bin/uak", "--json", "wait", "--for", "message", "--timeout", "2"], cwd=f.clones[1], env=env("agent-2"), allowed=None)
    expect(out.returncode == 5 and '"result":"IDLE_STOP"' in out.stdout, "--json reports IDLE_STOP: rc %d %s" % (out.returncode, out.stdout[:400]))
    cli = (r.package / ".uak/docs/CLI.md").read_text(encoding="utf-8")
    expect("`5`" in cli and "IDLE_STOP" in cli, "CLI.md documents exit 5")
    return "IDLE_STOP in json"


TESTS = [third_empty_wait_says_stop, event_resets_the_idle_count, idle_lines_never_say_wait_again,
         loop_mode_keeps_waiting, idle_stop_names_the_human_blocker,
         message_between_waits_resets_the_count, idle_stop_starts_the_count_over, blocker_text_has_no_control_characters,
         json_reports_idle_stop]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="uak-idle-stop-") as tmp:
        runner = Runner(args.package.resolve(), Path(tmp), resolve_binary("bash"), resolve_binary("git"))
        # The fixtures' own calls (f.hack, f.claim) use the runner's environment: no identity, base or loop mode leaks in.
        for k in ("UAK_BASE", "UAK_AGENT", "UAK_TASK", "UAK_HUMAN", "UAK_LOOP", "UAK_NOW", "UAK_WAIT_TIMEOUT", "UAK_WAIT_EVERY"):
            runner.env.pop(k, None)

        def one(test):
            started = time.monotonic()
            try:
                note = test(runner)
                return test.__name__, True, "%s, %.2fs" % (note, time.monotonic() - started)
            except Exception as exc:  # noqa: BLE001
                return test.__name__, False, str(exc)[:2500]
        selected = [t for t in TESTS if not args.case or t.__name__ in args.case]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(one, selected))
    for name, ok, info in results:
        print(("PASS " if ok else "FAIL ") + name + " (" + info + ")")
    passed = sum(1 for _, ok, _ in results if ok)
    print("IDLE_STOP_RESULT %s passed=%d failed=%d" % ("PASS" if passed == len(results) else "FAIL", passed, len(results) - passed))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
