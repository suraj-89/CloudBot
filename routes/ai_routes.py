from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from ai_service import ask_ai
from token_verify import verify_token
from database import SessionLocal
from models import User, Lead

router = APIRouter()

security = HTTPBearer()


class Question(BaseModel):
    question: str


@router.post("/ask-ai")
def ask_bot(
    data: Question,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    if user.role == "admin":

        leads = db.query(Lead).all()

    else:

        leads = db.query(Lead).filter(
            Lead.user_id == user.id
        ).all()

    lead_text = ""

    for lead in leads:

        lead_text += f"""
        Name: {lead.name}
        Company: {lead.company}
        Email: {lead.email}
        """

    prompt = f"""
    User question:
    {data.question}

    User leads:
    {lead_text}

    Give a short summary in 3-5 lines.
    """

    response = ask_ai(prompt)

    return {
        "answer": response
    }

@router.get("/generate-email/{lead_id}")
def generate_email(
    lead_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    lead = db.query(Lead).filter(
        Lead.id == lead_id
    ).first()

    if not lead:
        return {
            "message":"Lead not found"
        }

    if user.role != "admin" and lead.user_id != user.id:

        return {
            "message":"Access denied"
        }

    prompt = f"""
    Write a short professional follow-up email.

    Lead name: {lead.name}
    Company: {lead.company}

    Keep it friendly and under 100 words.
    """

    response = ask_ai(prompt)

    return {
        "email": response
    }