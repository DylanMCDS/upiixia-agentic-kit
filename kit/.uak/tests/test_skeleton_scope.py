#!/usr/bin/env python3
"""UAK-097: the walking skeleton can merge the files the kit itself generates. Dylan's live run (2026-11-19,
turno-cafeteria-3): HACK-001 ran `uak deploy --write` and `uak init-smoke` as its acceptance asked, and the merge gate
sent it to the human queue: deploy --write wrote a .dockerignore the plan never listed, and the smoke adapter
(.uak/bin/smoke-project and its provenance) is a shared resource even when the approved plan names it.

`uak lint` asks for .dockerignore wherever a task's Paths name Dockerfile or render.yaml. The scope check of
`uak merge` (rm_gate_scope, called by a harness as test_gate_scope.py does) lets a task ADD the adapter when the base
has none and its Paths name both files exactly; editing an existing adapter, or adding it without those exact Paths,
still goes to a human, and the reason says which. Real Git."""
import argparse
import concurrent.futures
import tempfile
import time
from pathlib import Path

from test_hack import Runner, expect, resolve_binary
from test_coordination import hack
from test_v571 import push_tasks

HARNESS = r'''# $1 the engine's .uak/bin, $2 the candidate (changes staged over $3), $3 the base SHA, $4 the claims tree,
# $5 TASKS.md, $6 the merge temp dir. Prints SCOPE OK or SCOPE REFUSED: the reason.
UAK_BIN=$1
for l in lib/core.sh uak-coordination lib/config.sh lib/backlog.sh lib/review-merge.sh; do . "$UAK_BIN/$l" || exit 9; done
RM_BUILD=$2 RM_BASE_TIP=$3 TX=$4 BACKLOG=$5 TXROOT=$6 ID=HACK-001 BASE=main RECORD=$4/tasks/HACK-001.md
if rm_gate_scope; then printf 'SCOPE OK\n'; else printf 'SCOPE REFUSED: %s\n' "$RM_REASON"; fi
'''

ADAPTER = ".uak/bin/smoke-project"
PROVENANCE = ".uak/bin/.smoke-project.provenance"
SKELETON_PATHS = "app.py, Dockerfile, .dockerignore, render.yaml, %s, %s" % (ADAPTER, PROVENANCE)
SKELETON_FILES = {"app.py": "print('hola')\n", "Dockerfile": "FROM python:3.12-slim\n", ".dockerignore": ".git\n",
                  "render.yaml": "services: []\n", ADAPTER: "#!/usr/bin/env bash\nexit 0\n",
                  PROVENANCE: "generated-by: uak init-smoke\n"}


def scene(r, name, paths, base_files, files):
    """A candidate repo: base_files committed, then files written and staged (as `uak merge` leaves it); HACK-001's
    Paths are `paths`. Returns the harness arguments."""
    d = r.scratch / name
    repo, tx, tmp = d / "repo", d / "tx", d / "tmp"
    for p in (repo, tx / "tasks", tmp):
        p.mkdir(parents=True)
    (tx / "tasks/HACK-001.md").write_text("ID: HACK-001\nState: REVIEW\nPaths: %s\n" % paths, encoding="utf-8")
    (d / "TASKS.md").write_text("# Tasks\n\n## HACK-001 · Walking skeleton\n- **Paths:** %s\n" % paths, encoding="utf-8")
    (tmp / "coord-source").write_text("# Project\nAdditive-Paths: -\n", encoding="utf-8")

    def put(rel, text):
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    r.g(repo, "init", "-q")
    for rel, text in dict({"README.md": "fixture\n"}, **base_files).items():
        put(rel, text)
    r.g(repo, "add", "-A")
    r.g(repo, "-c", "user.name=fixture", "-c", "user.email=fixture@example.test", "commit", "-q", "-m", "base")
    base = r.g(repo, "rev-parse", "HEAD").stdout.strip()
    for rel, text in files.items():
        put(rel, text)
    r.g(repo, "add", "-A")
    h = d / "harness.sh"
    h.write_text(HARNESS, encoding="utf-8", newline="\n")
    return d, [h.as_posix(), (r.package / ".uak/bin").as_posix(), repo.as_posix(), base, tx.as_posix(),
               (d / "TASKS.md").as_posix(), tmp.as_posix()]


def verdict(r, name, paths, base_files, files):
    d, args = scene(r, name, paths, base_files, files)
    out = r.run([r.bash] + args, cwd=d, allowed=None)
    text = out.stdout.strip()
    expect(out.returncode == 0 and text.startswith("SCOPE "), "the harness ran rm_gate_scope: " + (out.stdout + out.stderr)[-600:])
    return text


def dockerfile_paths_need_dockerignore(r):
    """Paths with Dockerfile and render.yaml but no .dockerignore: lint fails and names it (deploy --write writes all
    three). With .dockerignore in the Paths, lint says nothing about it."""
    f = r.fixture("skeleton-lint", paths={"HACK-001": "app.py, Dockerfile, render.yaml"}, count=1)
    out = hack(f, 0, "lint", allowed=None)
    text = out.stdout + out.stderr
    expect(out.returncode != 0 and "HACK-001" in text and ".dockerignore" in text and "deploy --write" in text,
           "lint names the missing .dockerignore: " + text[-1500:])
    push_tasks(f, lambda t: t.replace("app.py, Dockerfile, render.yaml", "app.py, Dockerfile, .dockerignore, render.yaml", 1))
    ok = hack(f, 0, "lint", allowed=None)
    text = ok.stdout + ok.stderr
    expect(".dockerignore" not in text, "with .dockerignore in Paths lint is quiet about it: " + text[-1500:])
    push_tasks(f, lambda t: t.replace("app.py, Dockerfile, .dockerignore, render.yaml", "app.py, render.yaml", 1))
    static = hack(f, 0, "lint", allowed=None)
    text = static.stdout + static.stderr
    expect(static.returncode != 0 and ".dockerignore" in text, "render.yaml alone asks for it too: " + text[-1500:])
    return "refused without it, quiet with it"


def skeleton_adds_the_smoke_adapter(r):
    """The base has no smoke adapter; the skeleton's Paths name both adapter files exactly: its merge passes scope."""
    got = verdict(r, "adds", SKELETON_PATHS, {}, SKELETON_FILES)
    expect(got == "SCOPE OK", "a first adapter named in Paths: expected SCOPE OK, got: " + got)
    return got


def editing_the_adapter_still_needs_a_human(r):
    """The base has an adapter: changing it (or adding a provenance beside it) needs a human, and the reason says the
    adapter already exists."""
    base = {ADAPTER: "#!/usr/bin/env bash\nexit 0\n", PROVENANCE: "generated-by: uak init-smoke\n"}
    got = verdict(r, "edit", SKELETON_PATHS, base, {ADAPTER: "#!/usr/bin/env bash\nexit 1\n"})
    expect(got.startswith("SCOPE REFUSED: Shared resource/CI needs a human: " + ADAPTER) and "already has" in got,
           "editing the adapter: expected a human with 'already has', got: " + got)
    got = verdict(r, "edit-provenance", SKELETON_PATHS, {ADAPTER: "#!/usr/bin/env bash\nexit 0\n"},
                  {PROVENANCE: "generated-by: me\n"})
    expect(got.startswith("SCOPE REFUSED: Shared resource/CI needs a human: " + PROVENANCE) and "already has" in got,
           "a provenance beside an existing adapter: expected a human, got: " + got)
    return "refused twice"


def adapter_outside_paths_still_needs_a_human(r):
    """No adapter in the base, but the Paths do not name it exactly (missing, or only its directory, or one of the two
    files): a human, and the reason names the exact Paths that would let it through."""
    # The provenance comes first in diff order (".smoke" sorts before "smoke"), so it is the file the reason names.
    cases = [("missing", "app.py, Dockerfile, .dockerignore, render.yaml", PROVENANCE),
             ("directory", "app.py, Dockerfile, .dockerignore, render.yaml, .uak/bin/", PROVENANCE),
             ("glob", "app.py, Dockerfile, .dockerignore, render.yaml, .uak/bin/*", PROVENANCE),
             ("one-of-two", "app.py, Dockerfile, .dockerignore, render.yaml, " + ADAPTER, PROVENANCE),
             ("other-one", "app.py, Dockerfile, .dockerignore, render.yaml, " + PROVENANCE, ADAPTER)]
    wrong = []
    for name, paths, refused in cases:
        got = verdict(r, "outside-" + name, paths, {}, SKELETON_FILES)
        if not (got.startswith("SCOPE REFUSED: Shared resource/CI needs a human: " + refused)
                and "Paths name" in got and ADAPTER in got.split(refused, 1)[1] and PROVENANCE in got):
            wrong.append("%s: %s" % (name, got))
    # Other shared files are untouched by this rule: a workflow in Paths still goes to a human.
    got = verdict(r, "outside-workflow", SKELETON_PATHS + ", .github/workflows/ci.yml", {},
                  dict(SKELETON_FILES, **{".github/workflows/ci.yml": "on: push\n"}))
    if got != "SCOPE REFUSED: Shared resource/CI needs a human: .github/workflows/ci.yml":
        wrong.append("workflow: " + got)
    expect(not wrong, "\n".join(wrong))
    return "%d cases refused" % (len(cases) + 1)


TESTS = [dockerfile_paths_need_dockerignore, skeleton_adds_the_smoke_adapter, editing_the_adapter_still_needs_a_human,
         adapter_outside_paths_still_needs_a_human]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    tests = [t for t in TESTS if not args.case or t.__name__ in args.case]
    with tempfile.TemporaryDirectory(prefix="uak-skeleton-scope-") as tmp:
        runner = Runner(args.package.resolve(), Path(tmp), resolve_binary("bash"), resolve_binary("git"))
        # The shell that runs the suite may be inside a task (UAK_BASE=next, UAK_AGENT): fixtures never inherit it.
        for k in [k for k in runner.env if k.startswith("UAK_") and k not in ("UAK_DEDUPE", "UAK_HARNESS", "UAK_KIT_HOME",
                  "UAK_KIT_URL", "UAK_EXTERNAL_SKILLS_TSV", "UAK_TASTE_HOME")]:
            runner.env.pop(k, None)

        def one(test):
            started = time.monotonic()
            try:
                note = test(runner)
                return test.__name__, True, "%s, %.2fs" % (note, time.monotonic() - started)
            except Exception as exc:  # noqa: BLE001
                return test.__name__, False, str(exc)[:2500]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(one, tests))
    for name, ok, info in results:
        print(("PASS " if ok else "FAIL ") + name + " (" + info + ")")
    passed = sum(1 for _, ok, _ in results if ok)
    print("SKELETON_SCOPE_RESULT %s passed=%d failed=%d" % ("PASS" if passed == len(results) else "FAIL", passed,
                                                            len(results) - passed))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
