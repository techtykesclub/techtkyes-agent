# FastAPI on Vercel (Python serverless function at /api/answer)
from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional, List
import os, re

API_KEY = os.environ.get("AGENT_API_KEY", "CHANGE_ME")

class Site(BaseModel):
    policies: str = "#"
    schedule: str = "#"
    faq: str = "#"

class Req(BaseModel):
    subject: Optional[str] = ""
    from_: Optional[str] = None
    body: str
    site: Optional[Site] = None

class Citation(BaseModel):
    title: str
    url: str

class Resp(BaseModel):
    reply: str
    confidence: float
    citations: List[Citation] = []
    needs_human: bool = False

app = FastAPI()

def intent(t: str):
    t = t.lower()
    if re.search(r"\b(refund|cancel|cancellation)\b", t): return "refund"
    if re.search(r"\b(when|date|schedule|spring break|president|thanksgiving|camp)\b", t): return "schedule"
    if re.search(r"\b(laptop|chromebook|device)\b", t): return "laptop"
    return "unknown"

@app.post("/api/answer", response_model=Resp)
def answer(req: Req, authorization: Optional[str] = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        return Resp(reply="", confidence=0.0, citations=[], needs_human=True)

    text = f"{req.subject}\n\n{req.body}".strip()
    i = intent(text)
    s = req.site or Site()

    if i == "refund":
        return Resp(
            reply=("Here's our current refund policy:\n"
                   "- Up to two weeks before class: 6% fee\n"
                   "- Up to one week before class: 20% fee\n"
                   "- After classes begin: no refunds\n\n"
                   "Reply with student name + order ID to proceed."),
            confidence=0.92,
            citations=[Citation(title="Policies - Refunds & Cancellations", url=s.policies)]
        )
    if i == "schedule":
        return Resp(
            reply=("We align camps with district breaks. Tell me the district and week "
                   '(e.g., "Los Altos - Spring Break 2026") and I\'ll confirm exact dates + links.'),
            confidence=0.78,
            citations=[Citation(title="Schedules & Dates", url=s.schedule)]
        )
    if i == "laptop":
        return Resp(
            reply=("A charged laptop (Windows/Mac/Chromebook) with a modern browser works. "
                   "Student should know their login. If you need a loaner, reply and we'll try to arrange."),
            confidence=0.86,
            citations=[Citation(title="FAQ - Devices & Setup", url=s.faq)]
        )
    return Resp(
        reply=("I can get you the exact answer-please share the student's grade, school/district, "
               "and topic (dates, refunds, skill level). I'll route to our coordinator if needed."),
        confidence=0.55,
        citations=[],
        needs_human=True
    )