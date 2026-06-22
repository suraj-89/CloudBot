from fastapi import APIRouter
from pydantic import BaseModel
from ai_service import ask_ai

router = APIRouter()


class Question(BaseModel):
    question: str


@router.post("/ask-ai")
def ask_bot(data: Question):

    response = ask_ai(
        data.question
    )

    return {
        "answer": response
    }