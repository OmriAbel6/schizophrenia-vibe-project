# Product Requirements Document (PRD)

**Project:** מבוא לסכיזופרניה: פסיכוביולוגיה, תפיסה וטכנולוגיה
**Repository:** https://github.com/OmriAbel6/schizophrenia-vibe-project
**Version:** 1.0 · **Date:** 2026-10-30 · **Status:** Submitted

---

## 1. Background & Problem Statement

Schizophrenia is a heterogeneous psychotic disorder whose clinical, neurobiological and perceptual
dimensions are usually taught in isolation. Static slides cannot convey the perceptual distortion patients
describe, nor the way standardised scales such as the PANSS turn symptoms into numbers that drive clinical
decisions. This capstone delivers an interactive, Hebrew-language web presentation that integrates the
three dimensions and demonstrates a reproducible computational pipeline behind the clinical metrics.

## 2. Goals

| # | Goal | Success signal |
|---|---|---|
| G1 | Teach the clinical, neurobiological and perceptual dimensions in 20 slides of academic Hebrew | Slide outline reviewed; every claim cited in slide 20 |
| G2 | Let the audience *experience* perceptual distortion safely | Slide 8 renders an interactive 3D scene with adjustable intensity and an opt-in auditory layer |
| G3 | Show how symptom scores become clinical decisions | Slides 16–18 render metrics produced by the Python tool, with the decision rules visible |
| G4 | Meet the course engineering standards | RTL/BiDi correct, PEP 8, modular code, incremental Git history, prompt logs, PRD |

## 3. Non-Goals

- No real patient data; all metrics are synthetic and labelled as such.
- No diagnostic or clinical-decision-support use.
- No backend, accounts, or analytics.
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
| F-11 | Slides 16–18 load `metrics.json` via `fetch`, falling back to `metrics.js` when opened from disk | Must |
| F-12 | Charts: grouped columns by PANSS domain (baseline/endpoint), trajectory line chart with crosshair tooltip and relapse markers, assessment cards | Must |
| F-13 | Every multi-series chart has a legend and a table view; direct labels are selective | Must |
| F-14 | Slide 20 lists academic references in APA style | Must |

### 5.2 Python tool (python/)

| ID | Requirement | Priority |
|---|---|---|
| P-01 | `schizophrenia_analysis.py` models the 30-item PANSS (1–7) with validation and domain totals | Must |
| P-02 | Treatment profiles with per-domain efficacy, build-up half-life, relapse hazard, adherence | Must |
| P-03 | `TrajectorySimulator` produces weekly assessments with relapse events and rater noise, seeded | Must |
| P-04 | Metrics: % reduction of adjusted total, responder 20/50 %, Andreasen remission (26 weeks), severity band, dominant dimension, clinical flags | Must |
| P-05 | `main.py` CLI: `--weeks`, `--seed`, `--output`, `--web-dir`, `--no-js`, `--no-mirror`, `--quiet` | Must |
| P-06 | Writes `metrics.json` and `metrics.js` to `python/` and mirrors them to `web/` | Must |
| P-07 | Standard library only; `requirements.txt` present; PEP 8 (≤ 88 chars, black-compatible) | Must |

## 6. Non-Functional Requirements

| ID | Requirement |
|---|---|
| N-01 | Dark clinical theme: `#0f172a` surfaces, `#38bdf8` / `#818cf8` accents, Heebo typography |
| N-02 | Chart palette validated for colour-vision deficiency and ≥ 3:1 contrast on the dark surface |
| N-03 | Usable at phone width (single-column layout, 16 px gutters, no horizontal scroll) |
| N-04 | `prefers-reduced-motion` lowers default simulation intensity and disables drift |
| N-05 | Simulation renders only while slide 8 is visible and the tab is active |
| N-06 | Deck works from `file://` and from any static HTTP server, no build step |
| N-07 | External dependencies limited to Google Fonts and the Three.js CDN (r128) |

## 7. Content Architecture (20 slides)

1 Title · 2 Clinical definition & epidemiology · 3 DSM-5-TR criteria · 4 Positive vs. negative symptoms ·
5 Dopamine hypothesis · 6 Glutamate / NMDA hypofunction · 7 Prefrontal hypofunction ·
8 **3D hallucination simulation** · 9 Cognitive impairment (MATRICS) · 10 Affective symptoms & suicide risk ·
11 Functional decline · 12 Course & prognosis · 13 Antipsychotics (FGA/SGA) · 14 Psychotherapy & rehabilitation ·
15 Digital health · 16 **PANSS & tool architecture + domain chart** · 17 **Trajectory simulation chart** ·
18 **Algorithmic assessment** · 19 Ethics, stigma, future tech · 20 Summary, Q&A, references.

## 8. Data Contract (`metrics.json`)

```
meta: { generated_at, generator, weeks, seed, disclaimer_he, scale{...}, thresholds{...}, references[] }
scenarios[]: {
  key, name, name_he, treatment{...},
  baseline{positive, negative, general, total, severity, items{P1..G16}},
  endpoint{positive, negative, general, total, severity},
  trajectory[]: {week, positive, negative, general, total, composite_index, remission_threshold},
  relapses[]: {week, magnitude, duration_weeks},
  assessment{severity, response, remission, dominant_dimension, relapse_count, flags[]}
}
```

## 9. Engineering Process Requirements

- Incremental, modular Git history (docs → python → web → change log), pushed to `main`.
- `prompts/` holds the AI prompt interaction logs; `PRD.md` holds this document.
- `README.md` follows the course template with student details, repo link, run instructions and change log.

## 10. Verification Plan & Results

| Check | Method | Result |
|---|---|---|
| Python compiles, runs, PEP 8 line length | `py_compile`, character-length scan | Pass |
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
