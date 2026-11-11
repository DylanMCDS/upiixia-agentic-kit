# DECISIONS

Coordination decisions on the claims branch.
- 1794364136 | plan | Dylan/Dylan | tasks added: UI-001 UI-002 UI-003 | Why: backlog without PR (Plan-Channel: claims)
- 1794364205 | plan --amend | Dylan/gpt-Dylan | amended: UAK-006 | Why: scope or criteria fixed before review
- 1794364668 | UI-001 | Keep --wizard opt-in and delegate to the existing installer and readiness gate. | Why: Preserve scripted installs and prevent installation success from implying authorization to claim.
- 1794365594 | UI-001 | Do not open a PR or declare green while baseline Windows validation failures are unresolved. | Why: The package smoke hit the_counter_sees_ps; it reproduces unchanged on main. Native Windows lint reports executable-bit findings.
- 1794365948 | UI-001 | Keep this exact SHA stable for claude-Dylan pre-review; no PR and no formal approval while validation is incomplete. | Why: Independent review must refer to the actual pushed implementation; required full smoke is not green on this Windows baseline.
