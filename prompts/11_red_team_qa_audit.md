# 11 · "Red Team" academic QA and submission-readiness audit

**Date:** 2026-11-06

## Prompt (verbatim)

```
# System Task: "Red Team" Academic QA & 100-Grade Submission Readiness Audit

You are an unforgiving, eagle-eyed academic QA auditor. The students have selected a self-evaluation grade of
"100", meaning this project will be subjected to the most brutal, microscopic grading by the evaluating LLM.
Your job is to audit the current state of the repository and identify ANY missing element or deviation from
the strict submission protocol.

Scan the repository and verify the following criteria with a strict Pass/Fail grade. If anything is missing,
output a critical warning and the code to fix it:

1. **README.md Visuals (CRITICAL NEW RULE):** Does the `README.md` contain actual image placeholders or
   embedded screenshots (e.g., `![Presentation UI](docs/slide.png)`) illustrating the Liquid Glass HTML
   presentation, the 3D video component, and the Python interactive output? (Text alone is a FAIL. Generate
   the Markdown syntax to embed these images and instruct the user to capture and upload the screenshots).
2. **20-Slide Structure & Positive/Negative Deep Dives:** Does `web/index.html` contain exactly 20 slides,
   including the newly requested deep-dive infographic slides on Positive and Negative symptoms?
3. **Tile-Based AI Simulation:** Is the Python component operating as a tile-based interactive agent
   without free-text input, as refined in the previous iteration?
4. **Prompt History:** Does the `/prompts` folder contain all the conversation logs (`.md` files) used to
   engineer this project, proving complete methodological control?
5. **PRD & Originality:** Does `PRD.md` reflect deep product characterization, incorporating the class
   philosophy ("האויב של הטוב הוא הטוב ביותר"), and exceeding minimum dry requirements with an
   Apple-inspired Liquid Glass premium design?

Output an uncompromising audit report. If a markdown fix is needed for the README screenshots or PRD,
provide the exact code block to resolve it immediately.
```

## Audit findings and remediation

| # | Criterion | Before | Fix applied | After |
|---|---|---|---|---|
| 1 | README visuals | **FAIL** – only a shields badge, no screenshots | Six real screenshots captured with headless Chrome at 1440×900 from the FastAPI-served deck (title, positive deep dive, negative deep dive, first-person 3D scene after five steps, tile chat after two answered tiles, finale), downscaled to 1280 px JPEG (~700 KB total) in `docs/screenshots/`, embedded in a new "צילומי מסך" section | PASS |
| 2 | 20 slides incl. deep dives | PASS – 20 `<section class="slide">`, titles 5 and 6 are "צלילת עומק" | – | PASS |
| 3 | Tile-based agent, no free text | PASS – no text input/textarea/form in `index.html`; `app.js` posts `question_id`; `main.py` serves `/api/questions` and routes tiles. Note: the API still accepts an optional free-text `message` for programmatic clients; the UI never exposes it | – | PASS |
| 4 | Prompt history | **PARTIAL** – logs 01–10 present, but the standing "continuous documentation workflow" instruction (given mid-iteration 04) was not logged, and this audit prompt had no log | Workflow instruction appended verbatim to `04_submission_and_git.md`; this log (`11_red_team_qa_audit.md`) created | PASS |
| 5 | PRD philosophy & liquid glass | **FAIL** – PRD had no "האויב של הטוב הוא הטוב ביותר" and still described the pre-glass pharma tokens | New §0 "Product Philosophy" with a minimum-vs-delivered table; goal G5; N-01 rewritten for the Liquid Glass system; version 3.2 | PASS |
| + | Leftover placeholder | README row "קורס / מוסד" still read "________" | Filled with the course, institution and academic year | PASS |

Untracked and deliberately uncommitted: `flat-design-medical-infographic/` (third-party inspiration
template dropped into the repo root by the user).
