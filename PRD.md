# Product Requirements Document (PRD)

**Project:** מבוא לסכיזופרניה: פסיכוביולוגיה, תפיסה וטכנולוגיה
**Repository:** https://github.com/OmriAbel6/schizophrenia-vibe-project
**Version:** 3.2 · **Date:** 2026-11-06 · **Status:** Submission candidate (tile-based patient agent, 20 slides, liquid-glass design)

---

## 0. Product Philosophy – "האויב של הטוב הוא הטוב ביותר"

The course's guiding sentence, *"the enemy of good is the best"*, shaped every iteration of this product.
We did not stop at a presentation that *meets* the brief; each cycle asked what a senior clinical-UX team
would ship, and rebuilt toward that:

| Minimum requirement | What this product does instead |
|---|---|
| 20 static slides in Hebrew | 20 slides with RTL-perfect typography, vertically distributed layouts, staggered entry animations, floating biological nodes and a text-free "shaking brain" bridge before the finale |
| A 3D media container | A first-person Three.js walk from the home to the street with breathing walls, detaching shadows, peripheral silhouettes that vanish when looked at, chromatic fringing, and a synthesised spatial-anxiety soundscape |
| A Python script that exports JSON | A FastAPI patient agent with two psychiatrically grounded personas, a curated 10 × 2 × 2 dialogue bank, an identical offline bank in the browser, an optional LLM path, and the Neuro-Sim dopamine model behind it |
| Readable slides | An Apple-inspired **Liquid Glass** design system: fluid mesh background with drifting blurred blobs, surfaces at 45 % white with 24 px backdrop blur, hairline white borders, 24 px radii, Heebo/Assistant hierarchy, and zero-overflow slides verified by screenshots |
| A bibliography slide | A standard-library PDF writer that typesets 24 references, linked from a glass pill button |
| Commit the code | Eleven numbered prompt logs, a dated Hebrew change log, incremental conventional commits, and headless-Chrome verification for every visual change |

"Good" would have passed; "best" is the only grade we tried to design for.

## 1. Background & Problem Statement

Schizophrenia is a heterogeneous psychotic disorder whose clinical, neurobiological and perceptual
dimensions are usually taught in isolation. Static slides cannot convey the perceptual distortion patients
describe, nor the way dopamine pathways and receptor blockade explain why antipsychotics relieve some
symptoms while worsening others. This capstone delivers an interactive, Hebrew-language web presentation
that integrates the three dimensions and demonstrates a reproducible computational model (the Neuro-Sim
dopamine engine) behind the neurobiology slides.

## 2. Goals

| # | Goal | Success signal |
|---|---|---|
| G1 | Teach the clinical, neurobiological and perceptual dimensions in 20 slides of academic Hebrew | Slide outline reviewed; every claim cited in slide 20 |
| G2 | Let the audience *experience* perceptual distortion safely | Slide 8 renders an interactive 3D scene with adjustable intensity and an opt-in auditory layer |
| G3 | Let the audience *question* a simulated patient and feel the difference treatment makes | Slide 18 hosts a tile-based interview with the patient agent in two clinical states, answered by the FastAPI backend from a curated bank (no API key needed), with an identical offline bank in the browser |
| G4 | Meet the course engineering standards | RTL/BiDi correct, PEP 8, modular code, incremental Git history, prompt logs, PRD |
| G5 | Exceed the minimum ("האויב של הטוב הוא הטוב ביותר") | Premium liquid-glass design, first-person 3D experience, tile-based patient agent with offline parity, screenshots in the README, headless-Chrome verification |

## 3. Non-Goals

- No real patient data; all metrics are synthetic and labelled as such.
- No diagnostic or clinical-decision-support use.
- No accounts or analytics. The only backend is the local FastAPI agent; nothing is stored server-side.
- No build toolchain: the deck must open from disk or any static server.

## 4. Users & Use Cases

| User | Use case |
|---|---|
| Presenting students | Drive the deck with keyboard/touch, run the 3D simulation live, toggle chart views |
| Course lecturer / graders | Open the repo, run `python/main.py`, read the PRD, prompt logs and commit history |
| Audience (students) | Read Hebrew slides, hover charts for exact values, open table views |

## 5. Functional Requirements

### 5.1 Presentation (web/)

| ID | Requirement | Priority |
|---|---|---|
| F-01 | Single-page application with exactly 20 `<section>` slides, vanilla HTML5/CSS3/JS | Must |
| F-02 | `<html lang="he" dir="rtl">`; global `direction: rtl; text-align: right; unicode-bidi: isolate;` | Must |
| F-03 | Latin terms, code and references isolated with `<bdi>` or `dir="ltr"` blocks | Must |
| F-04 | Navigation: ←/→ respecting RTL, Space/PageUp/PageDown, Home/End, click buttons, touch swipe | Must |
| F-05 | Progress bar, counter `שקופית X / 20`, slide title, fullscreen toggle (button + `F`) | Must |
| F-06 | URL hash `#N` reflects and restores the current slide | Should |
| F-07 | Slide 8: Three.js WebGL scene – morphing geometry, floating objects, particles, camera drift, FOV distortion | Must |
| F-08 | Slide 8 controls: intensity, drift toggle, wireframe, audio toggle, pause, reset | Must |
| F-09 | Slide 8 auditory layer synthesised with Web Audio, started only on user gesture | Should |
| F-10 | 2D canvas fallback when Three.js/WebGL is unavailable | Should |
| F-11 | Slide 18 "סימולציה קלינית חיה": liquid-glass chat container, state toggle (ללא טיפול / תחת טיפול תרופתי), message list and a **grid of question tiles** (no free-text input); a tile click posts `{question_id, clinical_state}` to `/api/chat` (relative when served by the backend) with a glass spinner while waiting, RTL bubbles; when the server is unreachable the identical bank in `web/dialogue.js` answers locally | Must |
| F-12 | Chat history is kept per clinical state in memory only; answers rotate through the variants of each tile | Should |
| F-16 | Slide 5 – positive-symptoms deep dive (hallucinations, delusions, paranoia) with liquid-glass infographics of how perception and daily life are disrupted; Slide 6 – negative-symptoms deep dive (avolition, anhedonia, flat affect, alogia) mapping the cascade to isolation and functional decline; exactly 20 slides | Must |
| F-13 | Every multi-series chart has a legend and a table view; direct labels are selective | Must |
| F-14 | Slide 20: three-point summary, Q&A prompt, "תודה על ההקשבה!" with presenters, and a button to `references.pdf` (generated by `python/generate_references_pdf.py`, standard library only) | Must |
| F-15 | Slide 5: horizontal RTL interactive flowchart below the text; hover/click highlights a node, animates the connector and reveals a clinical insight | Must |

### 5.2 Python backend – FastAPI live AI patient agent (python/)

| ID | Requirement | Priority |
|---|---|---|
| P-01 | `main.py` is a FastAPI app; `POST /api/chat` accepts `{question_id?, message?, clinical_state: "untreated"\|"treated", history[]}` and returns `{reply, clinical_state, state_label_he, question_id, question_he, mode: "tiles"\|"llm"\|"demo", model}`; `GET /api/questions` lists the tiles; `GET /api/dialogue` returns the whole bank | Must |
| P-09 | `dialogue.py` is the single source of truth for the tiles: 10 questions × 2 states × 2 variants, distinct per question *and* state (untreated: internal stimuli, paranoia, loose associations; treated: reality-tested with flat affect, avolition, alogia, withdrawal); `python3 dialogue.py --export` writes `web/dialogue.js` | Must |
| P-02 | Two Hebrew system prompts for a fictional patient (דני כהן, 24): active untreated psychosis (auditory hallucinations, loose associations, persecutory ideas, high anxiety, low insight) and six months on a second-generation antipsychotic (coherent, insight into past hallucinations, slight blunted affect, side effects) | Must |
| P-03 | Shared safety rules in both prompts: break character and refer to ער"ן 1201 / 101 on personal distress or self-harm; no medical or dosing advice; respectful, non-sensational portrayal | Must |
| P-04 | LLM via the OpenAI API with `OPENAI_API_KEY` (model from `OPENAI_MODEL`, default `gpt-4o-mini`); without a key the server runs a scripted demo mode and labels responses `mode: "demo"` | Must |
| P-05 | CORS middleware allowing any origin so the deck works from `file://`, a dev server or the backend itself; `GET /api/health` reports mode and model | Must |
| P-06 | The Neuro-Sim model (`schizophrenia_analysis.py`) stays as a library: `GET /api/neuro-sim` serves it and its numbers ground the personas | Should |
| P-07 | `requirements.txt`: fastapi, uvicorn, pydantic, openai; PEP 8 (≤ 88 chars) | Must |
| P-08 | The backend serves `web/` at `/` so one `uvicorn` process hosts both deck and API | Should |

## 6. Non-Functional Requirements

| ID | Requirement |
|---|---|
| N-01 | **Liquid Glass (Apple-inspired) design system**: fluid mesh background (ice blue, mint, pearl, pale rose) with four drifting blurred blobs; every surface `rgba(255,255,255,0.45)` + `backdrop-filter: blur(24px)` + `1px rgba(255,255,255,0.6)` border + `0 8px 32px rgba(0,0,0,0.04)` shadow + 24 px radius; navy `#0F172A` headings, `#334155` body, `#64748B` captions, cobalt `#0284C7` / cerulean `#0EA5E9` accents, teal `#0D9488` for mechanisms, emerald/rose reserved for positive/negative; Heebo headings (tight tracking) + Assistant body; vertically centred, zero-overflow slides at 100vh |
| N-02 | Chart palette validated for colour-vision deficiency and ≥ 3:1 contrast on the dark surface |
| N-03 | Usable at phone width (single-column layout, 16 px gutters, no horizontal scroll) |
| N-04 | `prefers-reduced-motion` lowers default simulation intensity and disables drift |
| N-05 | Simulation renders only while slide 8 is visible and the tab is active |
| N-06 | Deck works from `file://` and from any static HTTP server, no build step; the chat slide degrades to scripted demo replies when the backend is down |
| N-07 | External dependencies limited to Google Fonts and the Three.js CDN (r128) |

## 7. Content Architecture (20 slides)

1 Title · 2 Clinical definition & epidemiology · 3 DSM-5-TR criteria · 4 Positive vs. negative symptoms ·
5 **Positive symptoms deep dive** · 6 **Negative symptoms deep dive** · 7 Dopamine hypothesis · 8 Glutamate · 9 Prefrontal hypofunction ·
10 First-person 3D experience · 11 Cognition · 12 Affective symptoms · 13 Functional decline · 14 Course · 15 Antipsychotics ·
16 Psychotherapy · 17 Digital health · 18 **Live clinical AI simulation (tile interview)** · 19 Ethics, stigma, future tech ·
20 Summary, thanks + references PDF. (Back to exactly 20 slides in iteration 3.1.)

## 8. API Contract (`python/main.py`)

```
POST /api/chat
  request : { question_id?: str, message?: str, clinical_state: "untreated" | "treated", history: [{role, content}] }
  response: { reply, clinical_state, state_label_he, question_id, question_he, mode: "tiles" | "llm" | "demo", model }
GET  /api/questions   -> [ { id, label_he, icon } ]
GET  /api/dialogue    -> { states, state_labels_he, openers, questions[] }   (mirrored by web/dialogue.js)
GET  /api/health      -> { status: "ok", mode, model, states, questions }
GET  /api/neuro-sim   -> Neuro-Sim document (states[], occupancy_sweep[]) from schizophrenia_analysis.py
GET  /                -> the presentation (static files from web/)
```

## 9. Engineering Process Requirements

- Incremental, modular Git history (docs → python → web → change log), pushed to `main`.
- `prompts/` holds the AI prompt interaction logs; `PRD.md` holds this document.
- `README.md` follows the course template with student details, repo link, run instructions and change log.

## 10. Verification Plan & Results

| Check | Method | Result |
|---|---|---|
| Backend: `/api/questions`, tile answers differ per state and rotate, 404 on unknown tile, 422 on empty request, free text still works | `uvicorn` in a venv + `curl` | Pass |
| Python compiles, PEP 8 line length | `py_compile`, character-length scan | Pass |
| JS syntax | `node --check app.js` | Pass |
| Chart palette | dataviz validator, dark mode, surfaces `#0f172a` and `#1e293b` | All six checks pass |
| Slide layouts | Headless Chrome screenshots of slides 1, 3, 5, 8, 12, 13, 16, 17, 18, 20 at 1440×900 | Pass |
| WebGL scene | Headless Chrome (SwiftShader) with auto-start harness | Renders |
| `file://` fallback | Headless Chrome opening `index.html` from disk | `metrics.js` source reported |
| Audio layer | Manual listen in a real browser | To be confirmed by presenters |

## 11. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| No internet during the talk → Three.js CDN missing | 2D canvas fallback; optionally vendor `three.min.js` locally |
| Motion/flashing sensitivity in audience | Warning text on slide 8; intensity slider; reduced-motion defaults |
| Synthetic data mistaken for real evidence | Disclaimer in JSON meta, on slides 16–18 and in README |
| Hebrew/Latin bidi glitches | `<bdi>` isolation, LTR code blocks, screenshot review |

## 12. Open Items

- Fill in presenter names and advisor on slide 1 and in README.
- Optional: vendor Three.js locally for offline presentation.
