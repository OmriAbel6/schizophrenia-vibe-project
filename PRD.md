# Product Requirements Document (PRD)

**Project:** מבוא לסכיזופרניה: פסיכוביולוגיה, תפיסה וטכנולוגיה
**Repository:** https://github.com/OmriAbel6/schizophrenia-vibe-project
**Version:** 2.0 · **Date:** 2026-10-30 · **Status:** Iteration 2 (Neuro-Sim & UX overhaul)

---

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
| G3 | Show how dopamine pathway imbalance and receptor blockade produce and relieve symptoms | Slides 16–18 render large, code-free interactive visuals driven by the Python Neuro-Sim output |
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
| F-12 | Slide 16: animated side-by-side pathway gauges (healthy vs. untreated psychosis) with ≥ 18 px Hebrew labels; Slide 17: medication simulator with state buttons (ללא טיפול / דור 1 / דור 2) that animate pathway, symptom and side-effect charts; Slide 18: functioning-over-time curve with hoverable milestone cards. No code or terminal output on these slides | Must |
| F-13 | Every multi-series chart has a legend and a table view; direct labels are selective | Must |
| F-14 | Slide 20 lists academic references in APA style | Must |

### 5.2 Python tool – Neuro-Sim dopamine & medication engine (python/)

| ID | Requirement | Priority |
|---|---|---|
| P-01 | Model the mesolimbic pathway (hyperactivity > 100 % → positive symptoms) and the mesocortical pathway (hypoactivity < 100 % → negative/cognitive symptoms) | Must |
| P-02 | Receptor model: D2 blockade removes a fraction of pathway signalling; 5-HT2A blockade releases cortical dopamine; EPS emerge above ~80 % striatal D2 occupancy | Must |
| P-03 | Four clinical states: healthy (100/100), untreated psychosis (185/45), first-generation antipsychotic (broad D2 blockade), second-generation antipsychotic (D2 + 5-HT2A) | Must |
| P-04 | Per state: steady-state signalling, symptom profile (positive, hallucinations, delusions, anxiety, negative, cognitive, EPS, metabolic, functioning), 12-week time course and milestone takeaways in Hebrew | Must |
| P-05 | Occupancy sweep (0–100 % D2) per drug generation for the interactive simulator | Must |
| P-06 | `main.py` CLI: `--weeks`, `--output`, `--web-dir`, `--no-js`, `--no-mirror`, `--quiet`; writes `metrics.json`/`metrics.js` to `python/` and mirrors them to `web/` | Must |
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
8 **First-person 3D hallucination experience** · 9 Cognitive impairment (MATRICS) · 10 Affective symptoms & suicide risk ·
11 Functional decline · 12 Course & prognosis · 13 Antipsychotics (FGA/SGA) · 14 Psychotherapy & rehabilitation ·
15 Digital health · 16 **Dopamine storm: mesolimbic vs. mesocortical gauges** · 17 **Real-time medication simulator** ·
18 **Brain balance & quality of life over time** · 19 Ethics, stigma, future tech · 20 Summary, Q&A, references.

## 8. Data Contract (`metrics.json`)

```
meta: { generated_at, generator, weeks, healthy_signaling, disclaimer_he, model{...},
        pathways{mesolimbic, mesocortical}, symptom_labels_he{...}, references[] }
states[]: {
  key, name_he, summary_he,
  drug{key, name, name_he, generation, d2_occupancy, ht2a_occupancy, metabolic_burden},
  raw{mesolimbic, mesocortical},
  steady{mesolimbic, mesocortical, d2_occupancy, ht2a_occupancy,
         symptoms{positive, hallucinations, delusions, anxiety, negative, cognitive, eps, metabolic, functioning}},
  timeline[]: {week, mesolimbic, mesocortical, d2_occupancy, ht2a_occupancy, ...symptoms},
  milestones[]: {week, title_he, takeaway_he}
}
occupancy_sweep[]: {d2_occupancy, fga{mesolimbic, mesocortical, positive, negative, eps, functioning}, sga{...}}
```

## 9. Engineering Process Requirements

- Incremental, modular Git history (docs → python → web → change log), pushed to `main`.
- `prompts/` holds the AI prompt interaction logs; `PRD.md` holds this document.
- `README.md` follows the course template with student details, repo link, run instructions and change log.

## 10. Verification Plan & Results

| Check | Method | Result |
|---|---|---|
| Python compiles, runs, PEP 8 line length (Neuro-Sim engine) | `py_compile`, character-length scan | Pass |
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
