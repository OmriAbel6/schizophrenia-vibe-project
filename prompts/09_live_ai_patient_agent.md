# 09 · Live AI patient agent (FastAPI + LLM) and liquid-glass chat interface

**Date:** 2026-11-06

## Prompt (verbatim)

```
# System Task: Live AI Patient Agent Integration (FastAPI + LLM), Liquid Glass Chat Interface, and Continuous Git Workflow

We are executing the ultimate architectural upgrade for our capstone project. We are replacing the static
Python data generator with a **Live AI Psychiatric Patient Agent**.

Implement all requirements below systematically, save this prompt in `/prompts/09_live_ai_patient_agent.md`,
update the Change Log inside `README.md` before every commit, and push incremental commits to GitHub
(https://github.com/OmriAbel6/schizophrenia-vibe-project.git).

## 1. Python Backend: FastAPI Live LLM Agent (python/main.py, python/requirements.txt)
- Replace the old main.py with a lightweight FastAPI server.
- Create a POST /api/chat endpoint accepting a user message and clinical_state ("untreated" or "treated").
- Integrate a basic LLM structure (e.g., using OpenAI API with os.environ.get("OPENAI_API_KEY")).
- Define two psychiatric system prompts for the Agent:
  1. untreated_state: Schizophrenia patient in an active psychotic episode (auditory hallucinations, loose
     associations, high anxiety).
  2. treated_state: Same patient after 6 months of 2nd Generation Antipsychotics (coherent, acknowledging
     past hallucinations, slight blunted affect).
- Enable CORS middleware so the HTML presentation can fetch data from http://localhost:8000.
- Update requirements.txt with fastapi, uvicorn, pydantic, openai.

## 2. Frontend: Liquid Glass AI Chat Interface (web/index.html, web/style.css, web/app.js)
- Replace the static charts on Slides 16-18 with a single "Live Clinical AI Simulation" slide.
- Build a Liquid Glassmorphism chat container (background: rgba(255, 255, 255, 0.45); backdrop-filter:
  blur(24px); -webkit-backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04); border-radius: 24px;).
- Add a State Toggle Switch: "ללא טיפול" (Untreated) vs. "תחת טיפול תרופתי" (Treated).
- Add a message area, text input, and send button.
- In app.js, implement async fetch to http://localhost:8000/api/chat. Handle loading states with a liquid
  glass spinner, rendering user messages and AI responses in proper RTL Hebrew alignment.

## 3. Strict Incremental GitHub Workflow
Execute these commands sequentially using your terminal capabilities. Do NOT combine them into one commit:

1. Save this prompt to prompts/09_live_ai_patient_agent.md.
2. In README.md, append to the Change Log (Date: 2026-11-06, Author: עומרי אבל & אלה אדרי, Description:
   "שדרוג רכיב הפייתון לשרת FastAPI המריץ סוכן AI חי (LLM) המדמה מטופל סכיזופרני בשני מצבים קליניים").
3. Run in terminal:
   git add python/ PRD.md README.md prompts/
   git commit -m "feat(python): implement FastAPI live AI patient agent with dual psychiatric system prompts"
   git push origin main

4. In README.md, append to the Change Log: "הטמעת ממשק צ'אט אינטראקטיבי מזכוכית (Liquid Glass) במצגת,
   חיבור לשרת ה-FastAPI, והחלפת הגרפים הסטטיים בסימולציית זמן אמת".
5. Run in terminal:
   git add web/ README.md
   git commit -m "feat(web): build liquid glass AI chat interface and connect to FastAPI backend"
   git push origin main
```

## Execution summary

### Commit 1 – FastAPI live patient agent

- `python/main.py` rewritten as a FastAPI app (`uvicorn main:app --port 8000`):
  - `POST /api/chat` – `ChatRequest {message, clinical_state: "untreated"|"treated", history[≤20]}` →
    `ChatResponse {reply, clinical_state, state_label_he, mode, model}`; pydantic validation returns 422
    for an unknown state.
  - `GET /api/health` – mode (`llm` / `demo`) and model; `GET /api/neuro-sim` – the Neuro-Sim document
    from `schizophrenia_analysis.py`, which stays as a library and also grounds each persona with its
    dopamine/symptom numbers (internal background, "do not quote numbers").
  - `web/` is mounted at `/`, so one process serves deck and API; CORS allows any origin (the deck may be
    opened from `file://`, whose origin is `null`).
- Two Hebrew system prompts share a persona (דני כהן, 24, former design student from Haifa) and safety
  rules (break character and refer to ער"ן 1201 / 101 on distress or self-harm; no medical or dosing
  advice; respectful portrayal; 2–5 sentence replies). `untreated`: active psychosis for three weeks –
  three commenting/commanding voices, persecutory and referential ideas, moderate loosening of
  associations, high anxiety, little insight. `treated`: six months on risperidone – coherent, insight into
  past hallucinations, slight blunted affect, fatigue/weight gain, partial return to study and work.
- LLM: OpenAI Chat Completions with `OPENAI_API_KEY` / `OPENAI_MODEL` (default `gpt-4o-mini`), temperature
  0.95 untreated / 0.6 treated, max 260 tokens; failures surface as HTTP 502. Without a key the server runs
  a scripted **demo mode** (keyword-matched and rotating Hebrew replies per state) so the classroom demo
  never depends on connectivity; responses carry `mode: "demo"`.
- `requirements.txt`: fastapi, uvicorn[standard], pydantic, openai. `python/metrics.json`/`.js` deleted
  (no longer generated).
- Verified in a venv: health → `demo`; chat for both states (keyword "תרופות" picks the medication reply);
  invalid state → 422; OPTIONS preflight → `access-control-allow-origin: *`; `/index.html` → 200;
  `/api/neuro-sim?weeks=4` → 200; with a fake key health reports `llm`/`gpt-4o-mini` and chat returns a
  clean 502 wrapping OpenAI's 401.
- PRD §1, §2, §3, §5.1 F-11/F-12, §5.2, §6 N-06, §7, §8 and §10 updated for the agent and the 18-slide deck.

### Commit 2 – liquid-glass chat slide

(appended after execution)
