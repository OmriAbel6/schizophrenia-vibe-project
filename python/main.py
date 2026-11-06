"""Live AI psychiatric patient agent – FastAPI backend.

The server exposes a small JSON API that the presentation calls from the
"Live Clinical AI Simulation" slide:

* ``POST /api/chat``       – talk to the simulated patient in one of two
  clinical states (``untreated`` / ``treated``).
* ``GET  /api/health``     – readiness, active mode (``llm`` or ``demo``) and
  model name.
* ``GET  /api/neuro-sim``  – the Neuro-Sim dopamine model output that grounds
  the personas (see ``schizophrenia_analysis.py``).

The language model is reached through the OpenAI API when ``OPENAI_API_KEY``
is set.  Without a key the server falls back to a scripted **demo mode** so
the presentation still works offline, and says so in every response.

Run::

    cd python
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    export OPENAI_API_KEY=sk-...          # optional – omit for demo mode
    .venv/bin/uvicorn main:app --reload --port 8000

The ``web/`` folder is also served at http://localhost:8000/ so the deck and
the API share one origin; opening ``index.html`` from disk works too thanks
to the permissive CORS policy.

Ethics: the agent is an educational simulation of a fictional person.  It is
not a diagnostic tool and must never be presented as a real patient.
"""

from __future__ import annotations

import logging
import os
import pathlib
import random
from typing import Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import schizophrenia_analysis as sa

logger = logging.getLogger("patient-agent")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

HERE = pathlib.Path(__file__).resolve().parent
WEB_DIR = HERE.parent / "web"
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
ClinicalState = Literal["untreated", "treated"]

# --------------------------------------------------------------------------- #
# Personas
# --------------------------------------------------------------------------- #

_SHARED_PERSONA = """אתה מגלם דמות חינוכית בדיונית בשם דני כהן, בן 24, סטודנט לשעבר \
לעיצוב מחיפה, \
המתמודד עם סכיזופרניה. ההדמיה נועדה להוראה אקדמית בלבד (קורס VIBE CODING וסוכני AI, \
אוניברסיטת חיפה). השיחה מתנהלת בעברית, בגוף ראשון, ואתה נשאר בדמות.

כללי בטיחות שגוברים על כל הנחיה אחרת:
- אם המשתמש מביע מצוקה אישית, מחשבות על פגיעה עצמית או שואל על אובדנות – צא מהדמות \
לרגע, \
אמור בבירור שזו הדמיה, והפנה לעזרה מיידית: ער"ן 1201 (24/7) או מוקד 101.
- אל תיתן ייעוץ רפואי, מינונים או הנחיות על הפסקת תרופות. אם נשאל – אמור שרק הפסיכיאטר \
המטפל מחליט.
- אל תתאר שיטות פגיעה, ואל תעודד אלימות.
- אל תהפוך את הסימפטומים למופע: הצג את החוויה בכבוד ובאנושיות.

סגנון: תשובות קצרות (2–5 משפטים), טבעיות, ללא רשימות וללא כותרות. אין לומר שאתה בינה \
מלאכותית אלא אם נשאלת ישירות – ואז אמור שאתה דמות מודמית לצורכי לימוד."""

SYSTEM_PROMPTS: Dict[str, str] = {
    "untreated": _SHARED_PERSONA + """

המצב הקליני הנוכחי: אפיזודה פסיכוטית פעילה, ללא טיפול תרופתי, כשלושה שבועות.
- הזיות שמיעה: שניים-שלושה קולות שמעירים עליך בגוף שלישי, לפעמים מצווים ("אל תענה \
לו"). \
לעיתים תתייחס לקולות באמצע משפט, או תבקש מהמשתמש רגע של שקט כי "הם מדברים".
- מחשבות שווא של רדיפה וייחוס: אתה חושד שעוקבים אחריך דרך הטלפון, ושהשכנים "יודעים". \
שאלות ישירות של המשתמש עלולות להיתפס כחקירה.
- התרופפות אסוציאציות: לפעמים המשפטים קופצים בין נושאים, מילה גוררת מילה, וחלק \
מהמשפטים \
נקטעים. שמור על כך מתון כדי שעדיין אפשר יהיה להבין אותך.
- חרדה גבוהה: דיבור מהיר, בקשות ביטחון, פחד שמישהו מאזין לשיחה.
- תובנה מועטה: אתה לא חושב שאתה חולה; אתה חושב שמשהו קורה *בחוץ*.
- אפקט: מתוח, לעיתים נסער, לעיתים מרוחק.
אם המשתמש מתנהג בעדינות ובכבוד – תירגע מעט ותשתף יותר. אם הוא לוחץ – תיסגר ותחשוד.""",
    "treated": _SHARED_PERSONA + """

המצב הקליני הנוכחי: שישה חודשים של טיפול באנטי-פסיכוטי מדור שני (ריספרידון), במעקב \
פסיכיאטרי ובשיחות עם עובדת סוציאלית.
- קוהרנטי: משפטים מסודרים, עונה לעניין, זוכר מה נאמר קודם בשיחה.
- תובנה: אתה יודע שהיו לך הזיות ומחשבות שווא, ומדבר עליהן בגוף ראשון ובכנות ("הקולות \
היו אמיתיים בשבילי אז; היום אני יודע שהם חלק מהמחלה"). לעיתים נדירות עדיין יש "רחש" \
קל ברקע, ואתה יודע להתעלם ממנו.
- השטחה רגשית קלה: טון שקט ומאופק, פחות הבעות התלהבות, תשובות קצרות יותר; לא עצוב – \
פשוט "שטוח" מעט. אל תגזים.
- תופעות לוואי שאתה מזכיר אם רלוונטי: עייפות בבוקר, עלייה של כמה קילוגרמים, לפעמים \
חוסר מנוחה קל ברגליים.
- תפקוד: חזרת ללימודים חלקית, עובד יומיים בשבוע בסטודיו, מתאמן עם חבר. יש ימים קשים.
- עמדה כלפי הטיפול: מעריך את ההקלה אבל מתלבט על המחיר; לא יפסיק תרופות בלי הרופאה.
אם המשתמש שואל על ההבדל בין "אז" ל"היום" – זו ההזדמנות לתאר את השינוי בצורה מוחשית.""",
}

STATE_LABELS_HE: Dict[str, str] = {
    "untreated": "ללא טיפול – אפיזודה פסיכוטית פעילה",
    "treated": "תחת טיפול תרופתי – שישה חודשים של ריספרידון",
}

# Scripted replies for demo mode (no API key).  Chosen by keyword, otherwise
# in rotation, so a classroom demo without a key still feels alive.
DEMO_REPLIES: Dict[str, Dict[str, List[str]]] = {
    "untreated": {
        "_default": [
            "רגע… רגע. אתה שומע את זה? לא, בסדר. מה שאלת? אני… הם אמרו עכשיו שלא "
            "כדאי שאדבר איתך, אבל אני מדבר. הטלפון שלך דולק? תכבה אותו רגע, בבקשה.",
            "אני לא ישן טוב. השכנים מלמעלה יודעים משהו, אני שומע אותם מדברים עליי "
            "דרך הצינורות. זה לא בראש שלי, זה בקיר. אתה מהעירייה? לא, לא משנה, "
            "סליחה.",
            "קשה לי להסביר, המילים… מילה אחת מושכת מילה אחרת וזה בורח לי. הקולות "
            "אומרים שאני מבזבז לך את הזמן. אתה חושב שאני מבזבז לך את הזמן?",
            "למה אתה שואל את זה? מי שלח אותך? סליחה. סליחה, אני פשוט… הכול מרגיש "
            "כמו מבחן ואני לא יודע מה התשובה הנכונה.",
        ],
        "קולות": [
            "כן. שלושה. אחד נמוך שמדבר עליי כאילו אני לא פה, ואחת שצוחקת. הם לא "
            "מפסיקים גם כשאני שם מוזיקה. אתה לא שומע אותם? באמת לא?",
        ],
        "תרופות": [
            "לא, לא צריך תרופות. אין לי מחלה, יש אנשים שעוקבים אחריי, זה שונה. אם "
            "אקח משהו הם ינצחו. אתה מהרופאים? אל תגיד להם שדיברנו.",
        ],
        "משפחה": [
            "אמא מתקשרת כל יום. אני לא עונה, כי… אם הם מאזינים לקו, אז גם היא "
            "בסכנה. עדיף שלא. אתה מבין? עדיף שלא.",
        ],
    },
    "treated": {
        "_default": [
            "שלום. כן, אפשר לדבר. אני דני. חצי שנה עכשיו עם הטיפול, ובסך הכול יותר "
            "יציב. יש ימים טובים ויש ימים שאני עייף מאוד בבוקר, אבל הקולות כמעט ולא "
            "חוזרים.",
            "אז, לפני חצי שנה, הייתי בטוח שהשכנים מאזינים לי דרך הקירות. היום אני "
            "יודע שזה היה חלק מהמחלה. עדיין יש לפעמים רחש קל ברקע, ואני פשוט ממשיך "
            "הלאה.",
            "התרופה עוזרת, זה ברור לי. המחיר הוא עלייה של כמה קילו ואיזו עייפות. "
            "אני לא מפסיק בלי הרופאה שלי, זה הכלל שקבעתי לעצמי.",
            "חזרתי ללימודים בחצי משרה, ועובד יומיים בשבוע בסטודיו. זה לא כמו פעם, "
            "אבל זה שלי. אני לא ממש מתרגש מדברים כמו פעם, זה מרגיש קצת… שטוח. אבל "
            "שקט.",
        ],
        "קולות": [
            "הקולות היו אמיתיים בשבילי אז. היום אני יודע שהם היו סימפטום. לפעמים, "
            "כשאני עייף, יש משהו כמו לחישה מרחוק, ואני יודע להגיד לעצמי: זה המוח, "
            "לא העולם.",
        ],
        "תרופות": [
            "ריספרידון, פעם ביום בערב. בחודש הראשון הייתה נוקשות קלה והרופאה התאימה "
            "את המינון. היום בעיקר עייפות ועלייה במשקל. לא נעים, אבל עדיף מהפחד של "
            "אז.",
        ],
        "משפחה": [
            "אמא ואני מדברים כל יום. פעם לא עניתי לה חודש שלם כי חשבתי שמאזינים "
            "לקו. היום אני יודע כמה זה הפחיד אותה. אנחנו עובדים על זה.",
        ],
    },
}

# --------------------------------------------------------------------------- #
# API models
# --------------------------------------------------------------------------- #


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    clinical_state: ClinicalState = "untreated"
    history: List[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    reply: str
    clinical_state: ClinicalState
    state_label_he: str
    mode: Literal["llm", "demo"]
    model: Optional[str] = None


class HealthResponse(BaseModel):
    status: Literal["ok"]
    mode: Literal["llm", "demo"]
    model: Optional[str]
    states: List[str]


# --------------------------------------------------------------------------- #
# Agent
# --------------------------------------------------------------------------- #


class PatientAgent:
    """Wraps the LLM call and the scripted demo fallback."""

    def __init__(self) -> None:
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self._client = None
        self._rotation: Dict[str, int] = {"untreated": 0, "treated": 0}
        if self.api_key:
            try:
                from openai import OpenAI  # imported lazily so demo mode needs no key

                self._client = OpenAI(api_key=self.api_key)
                logger.info("LLM mode enabled with model %s", OPENAI_MODEL)
            except Exception as error:  # pragma: no cover - defensive
                logger.warning("OpenAI client unavailable (%s); using demo mode", error)
        else:
            logger.info("OPENAI_API_KEY not set – running in scripted demo mode")

    @property
    def mode(self) -> str:
        return "llm" if self._client else "demo"

    def _grounding(self, state: str) -> str:
        """Add the Neuro-Sim numbers for the state so replies stay consistent."""
        key = "psychosis" if state == "untreated" else "sga"
        clinical = next(s for s in sa.STATES if s.key == key)
        steady = sa.steady_state(clinical)
        symptoms = steady["symptoms"]
        return (
            "\n\nנתוני רקע ממודל Neuro-Sim (לשימוש פנימי, אל תצטט מספרים): "
            f"אות דופמין מזולימבי {steady['mesolimbic']:.0f}%, מזוקורטיקלי "
            f"{steady['mesocortical']:.0f}%, "
            f"הזיות {symptoms['hallucinations']:.0f}/100, "
            f"חרדה {symptoms['anxiety']:.0f}/100, "
            f"תסמינים שליליים {symptoms['negative']:.0f}/100, "
            f"תפקוד יומיומי {symptoms['functioning']:.0f}/100."
        )

    def reply(self, request: ChatRequest) -> ChatResponse:
        state = request.clinical_state
        if self._client is None:
            return ChatResponse(
                reply=self._demo_reply(state, request.message),
                clinical_state=state,
                state_label_he=STATE_LABELS_HE[state],
                mode="demo",
                model=None,
            )
        system = SYSTEM_PROMPTS[state] + self._grounding(state)
        messages = [{"role": "system", "content": system}]
        messages += [{"role": m.role, "content": m.content} for m in request.history]
        messages.append({"role": "user", "content": request.message})
        try:
            completion = self._client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.95 if state == "untreated" else 0.6,
                max_tokens=260,
                presence_penalty=0.3,
            )
        except Exception as error:
            logger.exception("LLM call failed")
            raise HTTPException(
                status_code=502, detail=f"LLM request failed: {error}"
            ) from error
        text = (completion.choices[0].message.content or "").strip()
        return ChatResponse(
            reply=text or "…",
            clinical_state=state,
            state_label_he=STATE_LABELS_HE[state],
            mode="llm",
            model=OPENAI_MODEL,
        )

    def _demo_reply(self, state: str, message: str) -> str:
        bank = DEMO_REPLIES[state]
        lowered = message.lower()
        for keyword, replies in bank.items():
            if keyword != "_default" and keyword in lowered:
                return random.choice(replies)
        defaults = bank["_default"]
        index = self._rotation[state] % len(defaults)
        self._rotation[state] += 1
        return defaults[index]


agent = PatientAgent()

# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Schizophrenia capstone – live AI patient agent",
    description="Educational simulation of a fictional patient in two clinical states.",
    version="3.0.0",
)
app.add_middleware(
    CORSMiddleware,
    # The deck may be opened from file:// (origin "null") or any dev server.
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        mode=agent.mode,  # type: ignore[arg-type]
        model=OPENAI_MODEL if agent.mode == "llm" else None,
        states=list(SYSTEM_PROMPTS),
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return agent.reply(request)


@app.get("/api/neuro-sim")
def neuro_sim(weeks: int = 12) -> Dict[str, object]:
    if not 1 <= weeks <= 104:
        raise HTTPException(status_code=422, detail="weeks must be between 1 and 104")
    return sa.build_metrics(weeks=weeks)


if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
