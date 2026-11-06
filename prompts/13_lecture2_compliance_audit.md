# 13 · "Red Team" Lecture-2 compliance audit

**Date:** 2026-11-06
**Attachment:** Dr. Yoram Segal's Lecture 2 summary (L02 – Pixels, Objects & Vectors), used as the rubric.

## Prompt (verbatim)

```
# System Task: "Red Team" Academic QA & 100-Grade Lecture 2 Compliance Audit

You are an unforgiving, eagle-eyed academic QA auditor ("Red Team"). The user is aiming for a perfect 100
grade on their "Vibe Coding & AI Agents" capstone project, based strictly on the Lecture 2 summary by Dr.
Yoram Segal. Your job is to audit the entire project repository and verify it meets EVERY single
requirement flawlessly. If anything is missing, incomplete, or incorrect, output a critical warning and the
exact steps or code to fix it.

Evaluate the project against the following strict criteria:

1. **Token Economy & Objects over Pixels (Core Philosophy):**
   - Does the project rely on code-generated objects (HTML, CSS, JavaScript) rather than heavy,
     pixel-by-pixel AI image generation or standard video files?

2. **HTML Presentation (The Deck):**
   - Is it built as a single HTML file?
   - Does it contain up to ~20 slides?
   - Does it include working navigation buttons (Next, Previous, Home) managed by JavaScript?
   - Is the layout strict RTL (Right-to-Left) with proper BiDi (Bidirectional) support for mixed
     English/Hebrew text?
   - Is Slide 1 a proper opening slide and the final slide a "Thank You" slide?

3. **3D Animation (Three.js):**
   - Is there a short 3D animated film (10 to 20 seconds) integrated into the project?
   - MUST it be built purely with `Three.js` (voxels/objects) and NOT as a standard flat video file (pixels)?
   - Does the animation include sound effects?

4. **Python Component:**
   - Is Python code actively integrated into the project (either as a visual effect within the
     presentation or as a background process manager/orchestrator)?

5. **Documentation & GitHub Management:**
   - **PRD.md**: Does this document exist and clearly define the product scope, features, tools, and
     slide count (acting as the "contract")?
   - **/prompts folder**: Does it contain the `.md` files of the prompt history, proving step-by-step
     engineering control over the AI?
   - **README.md**: Is it updated incrementally to reflect the progress and pushes?

Output a brutal Pass/Fail report for each section. For every 'Fail', provide the exact code, markdown, or
terminal commands to resolve the issue immediately so the user can secure their 100 grade.
```

## Audit findings and remediation

| # | Criterion | Before | Fix applied | After |
|---|---|---|---|---|
| 1 | Objects over pixels | PASS – `index.html` has no `<img>`/`<video>`; every visual is HTML/CSS/SVG/Three.js code; the only raster files are README screenshots | – | PASS |
| 2a | Single HTML file | **FAIL** – deck split into `index.html` + `style.css` + `app.js` + `dialogue.js` | New `python/build_single_file.py` inlines CSS and both scripts into `web/schizophrenia-deck.html` (only Google Fonts and the Three.js CDN stay external); verified 20 sections and no local `src`/`href` left | PASS |
| 2b | ≤ ~20 slides | PASS – exactly 20 | – | PASS |
| 2c | Next / Previous / Home buttons | **FAIL** – Home existed only as a keyboard key | `⌂` Home button added to the nav bar, wired in `app.js` to `goTo(0)` | PASS |
| 2d | Strict RTL + BiDi | PASS – `<html lang="he" dir="rtl">`, global `direction: rtl; unicode-bidi: isolate`, 57 `<bdi>` isolations, LTR code/reference blocks | – | PASS |
| 2e | Opening and thank-you slides | PASS – slide 1 "שער", slide 20 "תודה על ההקשבה" | – | PASS |
| 3a | 10–20 s 3D animated film | **FAIL** – the Three.js scene was interactive only (manual steps), no timed film | **Film mode**: "▶ סרט אנימציה (15 שניות, עם סאונד)" resets the scene, turns the soundscape on (user gesture), auto-steps the camera through all seven waypoints over 15 s with an on-screen countdown, then stops | PASS |
| 3b | Pure Three.js, not a video file | PASS – scene built from Three.js meshes/lights, no `<video>` | – | PASS |
| 3c | Sound effects | PARTIAL – available but opt-in | Film mode enables heartbeat, whispers, footsteps, door creak and ring automatically | PASS |
| 4 | Python integrated | PASS – FastAPI orchestrator serves the deck, answers the tile agent, exposes Neuro-Sim; `dialogue.py` exports the browser bank; PDF generator; new single-file bundler | – | PASS |
| 5a | PRD = contract (scope, features, tools, slide count) | PARTIAL – scope, features and "exactly 20 slides" present, **no tools section** | "Tools & Stack" table added; F-01/F-04/F-07 updated for the single-file build, Home button and film mode; version 3.4 | PASS |
| 5b | `/prompts` history | PASS – 13 numbered logs, each with the verbatim prompt and an execution summary | – | PASS |
| 5c | README updated incrementally | PASS – 19 dated change-log rows across 19 commits, screenshots, run instructions | – | PASS |
| 11.3 | GitHub collaborators (lecture §11.3) | **WARN** – repository is public with collaborators `OmriAbel6` and `elaedri`; the lecturer is not yet a collaborator (his GitHub handle/e-mail is published on Moodle, not available here) | Command for the students: `gh api -X PUT repos/OmriAbel6/schizophrenia-vibe-project/collaborators/<lecturer-handle> -f permission=pull` | Student action |

Verification after the fixes: `node --check` on `app.js`; the bundle builds (20 sections, no unresolved
local references); headless-Chrome run of film mode on the FastAPI-served deck confirmed the camera
reaches the street and the countdown hides at the end.
