from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class ChatQuestion(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    language: str = Field("en")

@router.post("/ask")
async def ask_question(question: ChatQuestion):
    try:
        from app.services.free_llm import free_llm
        result = free_llm.ask(question.query)
        if result and result.get("answer"):
            return {
                "query": question.query,
                "answer": result["answer"],
                "confidence": result.get("confidence", 0.9),
                "sources": [],
                "disclaimer": "Verify with scholars. Wallahu A'lam",
            }
        return {"query": question.query, "answer": "Please try again.", "confidence": 0}
    except Exception:
        return {"query": question.query, "answer": "An error occurred.", "confidence": 0}

@router.get("/health")
async def chat_health():
    return {"status": "chat_ready"}
