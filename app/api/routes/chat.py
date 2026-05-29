from fastapi import APIRouter

from pydantic import BaseModel

from app.services.rag_service import (
    RAGService,
)


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(
    request: ChatRequest
):

    rag_service = RAGService()

    response = rag_service.ask(
        request.question
    )

    return response