# Round D · UX and accessibility audit · kit 4df3acb (UI-018 head) · saved by the lead from the auditor's reply

Method: real setup server + Playwright Chromium; fixtures from kit/.uak/tests helpers; 1280/390/1440, en/es, light/dark, keyboard, contrast, names, live regions. Raw data D/data/phase_*.json, screenshots D/shots/.

Works: focus rings, no overflow at 390, skip link, UI-018 busy states and toasts (Esc, Go there), video (no autoplay, captions), reduced motion, no unnamed controls, dark setup contrast.

## Top 10
1. P1 Field errors (name, schedule, idea) go to a global #error box ~2,900 px below the field; focus falls to body; no aria-invalid/aria-describedby (WCAG 3.3.1). Fix: per-field error under the field + focus it. (e-name-error-viewport-en.png)
2. P1 Invalid time zone ("Mars/Base") accepted (HTTP 200) and a Freeze-Epoch computed. Fix: validate with zoneinfo, datalist prefilled with browser zone.
3. P2 Configuration shows every step at once (3,774–5,578 px); Check what's next at the very bottom. Fix: collapse completed steps, open only the current one.
4. P2 Team step shows implement/review launch commands before the reviewer is registered. Fix: gate steps 2–3 on registration.
5. P2 During an operation, Check/Repair/Choose project/Save are natively disabled with no reason or toast (UI-018 gap). Fix: aria-disabled + blocked reason + toast.
6. P2 After a planner rule break: "Done at …" + green "lint passes" box under the red violation box; conflicting advice ("undo those changes" vs "ask for changes"). Fix: "Finished with problems", hide lint-pass, one undo instruction with command.
7. P2 English in Spanish UI: gate lines, violation list, raw git stderr when offline (misleading "check your connection"), native validation bubbles. Fix: server-side translation + mapped git errors + setCustomValidity.
8. P2 Contrast: setup --muted 4.45:1 / 4.19:1; dashboard --muted 3.26–3.5:1. Fix: darken to ≥4.5:1.
9. P2 WCAG 2.5.3: "View" label vs accessible name "Interface profile"; 2.5.8: dashboard task-ID buttons 53x19 px. Fix: drop aria-label; min-height 24 px.
10. P2 "Set up my project" below the fold (755 px at 1280x720); two different 1–5 step models (journey bar vs sidebar). Fix: move CTA up; one step model.

## Other findings
- P2 Event times as weekdays without dates, in reversed order ("stops Wed 06:24; take the first task by Tue 11:55").
- P2 Jargon for novices (lint, wave, worktree, MCP, freeze, origin); "Nothing to test first: no (scaffold)" double negative.
- P2 Headings: "Proposed plan" H3 inside H3; H2 replaced by a raw gate line; dashboard views have no headings, H1 hidden.
- P3 Esc does not close approval/publish confirmations; approval hint never updates after a correct entry; dashboard skip link says "Skip to setup"; dashboard tabs not ARIA tabs, names run into counts ("Board2"); tab strip cut at 390; "Agents online" green dot at 0; 3–4 console 400s on a fresh folder; two result texts for Save name; journey bar does not mark completed steps; Spanish register mixes ustedes/tú; relative path error wording; red identity box after a normal install; one blocked reason shown 3 times; trust note shown when Claude Code is not the selected planner; launch commands unexplained for beginners; theme select has no visible label; up to 27 live regions.
