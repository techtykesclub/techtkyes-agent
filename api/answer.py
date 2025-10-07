# FastAPI on Vercel (Python serverless function at /api/answer)# FastAPI on Vercel (Python serverless function at /api/answer)

from fastapi import FastAPI, Headerfrom f    return Resp(

from pydantic import BaseModel        reply=("I can get you the exact answer—please share the student's grade, school/district, "

from typing import Optional, List               "and topic (dates, refunds, skill level). I'll route to our coordinator if needed."),

import os, re        confidence=0.55,

        citations=[],

API_KEY = os.environ.get("AGENT_API_KEY", "CHANGE_ME")        needs_human=True

    )

class Site(BaseModel):

    policies: str = "#"# Export handler for Vercel

    schedule: str = "#"handler = appimport FastAPI, Header

    faq: str = "#"from pydantic import BaseModel

from typing import Optional, List

class Req(BaseModel):import os, re

    subject: Optional[str] = ""

    from_: Optional[str] = NoneAPI_KEY = os.environ.get("AGENT_API_KEY", "CHANGE_ME")

    body: str

    site: Optional[Site] = Noneclass Site(BaseModel):

    policies: str = "#"

class Citation(BaseModel):    schedule: str = "#"

    title: str    faq: str = "#"

    url: str

class Req(BaseModel):

class Resp(BaseModel):    subject: Optional[str] = ""

    reply: str    from_: Optional[str] = None

    confidence: float    body: str

    citations: List[Citation] = []    site: Optional[Site] = None

    needs_human: bool = False

class Citation(BaseModel):

app = FastAPI()    title: str

    url: str

def intent(t: str):

    t = t.lower()class Resp(BaseModel):

    if re.search(r"\b(refund|cancel|cancellation)\b", t): return "refund"    reply: str

    if re.search(r"\b(when|date|schedule|spring break|president|thanksgiving|camp)\b", t): return "schedule"    confidence: float

    if re.search(r"\b(laptop|chromebook|device)\b", t): return "laptop"    citations: List[Citation] = []

    return "unknown"    needs_human: bool = False



@app.post("/", response_model=Resp)app = FastAPI()

def answer(req: Req, authorization: Optional[str] = Header(None)):

    if authorization != f"Bearer {API_KEY}":def intent(t: str):

        return Resp(reply="", confidence=0.0, citations=[], needs_human=True)    t = t.lower()

    if re.search(r"\b(refund|cancel|cancellation)\b", t): return "refund"

    text = f"{req.subject}\n\n{req.body}".strip()    if re.search(r"\b(when|date|schedule|spring break|president|thanksgiving|camp)\b", t): return "schedule"

    i = intent(text)    if re.search(r"\b(laptop|chromebook|device)\b", t): return "laptop"

    s = req.site or Site()    return "unknown"



    if i == "refund":@app.post("/", response_model=Resp)

        return Resp(def answer(req: Req, authorization: Optional[str] = Header(None)):

            reply=("Here's our current refund policy:\n"    if authorization != f"Bearer {API_KEY}":

                   "• Up to two weeks before class: 6% fee\n"        return Resp(reply="", confidence=0.0, citations=[], needs_human=True)

                   "• Up to one week before class: 20% fee\n"

                   "• After classes begin: no refunds\n\n"    text = f"{req.subject}\n\n{req.body}".strip()

                   "Reply with student name + order ID to proceed."),    i = intent(text)

            confidence=0.92,    s = req.site or Site()

            citations=[Citation(title="Policies — Refunds & Cancellations", url=s.policies)]

        )    if i == "refund":

    if i == "schedule":        return Resp(

        return Resp(            reply=("Here’s our current refund policy:\n"

            reply=("We align camps with district breaks. Tell me the district and week "                   "• Up to two weeks before class: 6% fee\n"

                   "(e.g., "Los Altos — Spring Break 2026") and I'll confirm exact dates + links."),                   "• Up to one week before class: 20% fee\n"

            confidence=0.78,                   "• After classes begin: no refunds\n\n"

            citations=[Citation(title="Schedules & Dates", url=s.schedule)]                   "Reply with student name + order ID to proceed."),

        )            confidence=0.92,

    if i == "laptop":            citations=[Citation(title="Policies — Refunds & Cancellations", url=s.policies)]

        return Resp(        )

            reply=("A charged laptop (Windows/Mac/Chromebook) with a modern browser works. "    if i == "schedule":

                   "Student should know their login. If you need a loaner, reply and we'll try to arrange."),        return Resp(

            confidence=0.86,            reply=("We align camps with district breaks. Tell me the district and week "

            citations=[Citation(title="FAQ — Devices & Setup", url=s.faq)]                   "(e.g., “Los Altos — Spring Break 2026”) and I’ll confirm exact dates + links."),

        )            confidence=0.78,

    return Resp(            citations=[Citation(title="Schedules & Dates", url=s.schedule)]

        reply=("I can get you the exact answer—please share the student's grade, school/district, "        )

               "and topic (dates, refunds, skill level). I'll route to our coordinator if needed."),    if i == "laptop":

        confidence=0.55,        return Resp(

        citations=[],            reply=("A charged laptop (Windows/Mac/Chromebook) with a modern browser works. "

        needs_human=True                   "Student should know their login. If you need a loaner, reply and we’ll try to arrange."),

    )            confidence=0.86,

            citations=[Citation(title="FAQ — Devices & Setup", url=s.faq)]

# Export handler for Vercel        )

handler = app    return Resp(
        reply=("I can get you the exact answer—please share the student’s grade, school/district, "
               "and topic (dates, refunds, skill level). I’ll route to our coordinator if needed."),
        confidence=0.55,
        citations=[],
        needs_human=True
    )