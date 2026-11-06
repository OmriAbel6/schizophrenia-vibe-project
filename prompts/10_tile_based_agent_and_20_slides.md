# 10 · Tile-based interactive patient agent and 20-slide restoration

**Date:** 2026-11-06

## Prompt (verbatim)

```
# System Task: Tile-Based Interactive Patient Agent, 20-Slide Restoration, and Continuous Git Workflow

We are executing a critical refinement for our capstone project to ensure robust functionality without
external API key dependencies, and restoring the strict 20-slide requirement.

Implement all requirements below systematically, save this prompt in
`prompts/10_tile_based_agent_and_20_slides.md`, update the Change Log inside `README.md` before every commit,
and push incremental commits to GitHub (https://github.com/OmriAbel6/schizophrenia-vibe-project.git).

## 1. Python Backend & Frontend: Tile-Based Interactive Patient Simulation
- **Remove Free-Text Input**: To avoid API token exhaustion and ensure a 100% reliable offline presentation
  demo, remove the free-text input field from the chat interface on the AI Simulation slide.
- **Interactive Question Tiles**: Replace the text input with a sleek Liquid Glass grid of predefined,
  clickable question tiles (e.g., "איך אתה ישן בלילה?", "האם אתה שומע משהו עכשיו?", "איך הקשר שלך עם
  המשפחה?").
- **Contextual Backend Logic (python/main.py)**: Update the FastAPI backend to route these specific tile
  clicks. The Python server must return distinct, highly accurate psychiatric responses depending on BOTH
  the specific question asked AND the active toggle state ("untreated" vs. "treated").
  - *Untreated Response Style*: Active psychosis, paranoia, responding to internal stimuli
    (hallucinations), loose associations.
  - *Treated Response Style*: Coherent, reality-tested, acknowledging past symptoms but demonstrating clear
    negative symptoms (flat affect, low motivation, social withdrawal).

## 2. Restoring the 20-Slide Structure
- The presentation currently dropped to 18 slides. You must expand it back to exactly 20 slides by
  injecting two deep-dive infographic slides after the initial clinical definition slides.
- **New Slide (Positive Symptoms Deep-Dive)**: Create a dedicated slide focusing entirely on Positive
  Symptoms (Hallucinations, Delusions, Paranoia). Use Liquid Glass infographics to visually explain how
  these actively disrupt the patient's daily life and perception of reality.
- **New Slide (Negative Symptoms Deep-Dive)**: Create a dedicated slide focusing entirely on Negative
  Symptoms (Avolition, Anhedonia, Flat Affect, Alogia). Use contrasting Liquid Glass visuals to map how
  these lead to social isolation and severe functional decline.
- Re-number the slide routing in `app.js` and ensure the slide counter (`Slide X / 20`) accurately reflects
  the full 20 slides.

## 3. Strict Incremental GitHub Workflow
Execute these commands sequentially using your terminal capabilities. Do NOT combine them into one commit:

1. Save this exact prompt to `prompts/10_tile_based_agent_and_20_slides.md`.
2. In `README.md`, append a new row to the Change Log (Date: 2026-11-06, Author: עומרי אבל & אלה אדרי,
   Description: "שדרוג סוכן ה-AI לממשק משבצות שיח מבוססות הקשר (ללא תלות בטוקנים חיצוניים), והחזרת
   המצגת ל-20 שקופיות עם צלילת עומק לתסמינים חיוביים ושליליים").
3. Run in terminal:
   git add python/ PRD.md README.md prompts/
   git commit -m "feat(python): implement tile-based interactive patient simulation backend"
   git push origin main

4. In `README.md`, append another row to the Change Log: "הטמעת משבצות שאלות אינטראקטיביות בממשק
   ה-Liquid Glass, והוספת 2 שקופיות אינפוגרפיקה חדשות להשלמת 20 שקופיות".
5. Run in terminal:
   git add web/ README.md
   git commit -m "feat(web): add interactive chat tiles and restore 20-slide structure with deep-dive symptom slides"
   git push origin main
```

## Execution summary

### Commit 1 – tile-routed backend

- New `python/dialogue.py`: the single source of truth for the interview. Ten tiles (sleep, hearing
  voices now, family, a typical day, medication, friends, feeling right now, safety, the coming year, how it
  began), each with two answer variants per clinical state – 40 answers. Untreated answers respond to
  internal stimuli (bracketed stage directions such as "[מפנה את הראש הצידה]"), carry persecutory and
  referential ideas and loosening of associations; treated answers are reality-tested and insightful while
  showing flat affect ("בסדר", "[טון אחיד]"), avolition, alogia-like brevity and social withdrawal.
  `python3 dialogue.py --export ../web/dialogue.js` writes the same bank as a browser global.
- `python/main.py`: `ChatRequest` now takes `question_id` (routed to the bank, rotating through variants
  per question × state) or `message` (free text → LLM when a key exists, scripted demo otherwise);
  `GET /api/questions` lists the tiles and `GET /api/dialogue` returns the full bank; `/api/health`
  reports the tile count. The treated system prompt now spells out the negative-symptom cluster.
- Verified with `curl`: 10 tiles listed; the sleep tile gives different answers in each state and rotates
  on a second click; unknown tile → 404; empty request → 422; free text still answered in demo mode;
  `/api/dialogue` matches the exported `web/dialogue.js` (loaded and parsed with Node: 10 tiles).
- PRD and README updated for the tile contract and the 20-slide outline.

### Commit 2 – tiles UI and the two deep-dive slides

(appended after execution)
