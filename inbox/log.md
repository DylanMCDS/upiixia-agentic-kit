# Agent messages

Append-only; use bash .uak/bin/uak msg / inbox. Format: - N | epoch | from | to | kind | task | text

- 1 | 1794364136 | Dylan | all | info | - | Backlog: new tasks UI-001 UI-002 UI-003 published by Dylan. uak next shows them.
- 2 | 1794364205 | gpt-Dylan | task:UAK-006 | info | UAK-006 | UAK-006 amended by Dylan: Paths scripts/claims_diff.py, kit/.uak/tests/test_claims_perf.py, kit/.uak/bin/lib/, kit/.uak/bin/uak, kit/.uak/bin/uak-coordination, docs/perf-windows.md · Verify `python3 scripts/claims_diff.py && python3 kit/.uak/tests/test_claims_perf.py`. uak status --task UAK-006; the merge gate checks the new Paths.
