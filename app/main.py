import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from app.state import create_session, get_session
from app.agent import start_interview, continue_interview

load_dotenv()

app = FastAPI(title="AI Technical Interview Agent")


class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[dict] = None
    message: Optional[str] = None

@app.get("/")
def root():
    return {"status": "running", "service": "AI Technical Interview Agent"}

@app.post("/api/interview")
def interview(request: InterviewRequest):
    session = get_session(request.sessionId)

    if session is None:
        if request.candidate is None:
            return {"reply": "Candidate information is required to start.", "done": True}
        session = create_session(request.sessionId, request.candidate)
        return {"reply": start_interview(session), "done": False}

    if session["done"]:
        return {"reply": "This interview has already been completed.", "done": True}

    if not request.message:
        return {"reply": "Please provide your interview answer.", "done": False}

    return continue_interview(session, request.message)
