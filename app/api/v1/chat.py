from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.services.free_llm import free_llm
from app.services.islamic_ai_service import IslamicAIService
from app.services.cache_service import cache_service
from app.api.dependencies import get_islamic_ai_service, optional_authentication
from app.models.user import User
from app.utils.helpers import islamic_helpers
import time

router = APIRouter()

class ChatQuestion(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000, description="Your question")
    language: str = Field("en", description="Response language: en, ar, ur, fr, es")
    include_sources: bool = Field(True, description="Include source references")
    authenticate_only: bool = Field(True, description="Use only authenticated sources")
class ChatResponse(BaseModel):
    question: str
    answer: str
    query_type: str
    confidence: float
    sources: list = []
    disclaimer: str
    suggestions: list = []
    timestamp: str

@router.post("/ask")
async def ask_question(question: ChatQuestion):
    """
    Ask an Islamic question and get AI-powered response.
    Never returns errors to the user - always has a graceful response.
    """
    start_time = time.time()
    
    try:
        # Try free LLM (Puter first, then Groq keys)
        result = free_llm.ask(question.query)
        
        if result and result.get("answer"):
            return {
                "query": question.query,
                "answer": result["answer"],
                "confidence": result.get("confidence", 0.9),
                "sources": [],
                "disclaimer": "Verify with qualified scholars. Wallahu A'lam",
                "suggestions": [],
                "response_id": f"swlh-{int(time.time())}",
                "response_time": round(time.time() - start_time, 3),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        
        # No answer - graceful fallback
        return {
            "query": question.query,
            "answer": "I apologize, but I am currently experiencing high demand. Please try again in a moment. JazakAllahu Khairan.",
            "confidence": 0,
            "sources": [],
            "disclaimer": "Wallahu A'lam",
            "suggestions": [],
            "response_id": f"swlh-{int(time.time())}",
            "response_time": round(time.time() - start_time, 3),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {
            "query": question.query,
            "answer": "An unexpected error occurred. Please try again. JazakAllahu Khairan for your patience.",
            "confidence": 0,
            "sources": [],
            "disclaimer": "Wallahu A'lam",
            "suggestions": [],
            "response_id": f"swlh-{int(time.time())}",
            "response_time": round(time.time() - start_time, 3),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

@router.get("/suggestions", response_model=Dict[str, Any])
async def get_suggestions():
    """
    Get suggested questions for common Islamic topics.
    """
    suggestions = {
        "quran": [
            "What is the meaning of Surah Al-Fatiha?",
            "How many surahs are in the Quran?",
            "What are the Makki and Madani surahs?",
            "Explain Surah Al-Ikhlas"
        ],
        "hadith": [
            "What are the most authentic hadith collections?",
            "What did the Prophet say about honesty?",
            "Explain the hadith about intentions",
            "What are the 40 Hadith of Nawawi?"
        ],
        "fiqh": [
            "How to perform wudu?",
            "What breaks the fast in Ramadan?",
            "How to calculate zakat?",
            "What are the conditions for valid prayer?"
        ],
        "aqeedah": [
            "What are the six pillars of faith?",
            "Explain Tawheed",
            "Who are the prophets in Islam?",
            "What is the Day of Judgment?"
        ],
        "general": [
            "What is Islam?",
            "Who is Prophet Muhammad?",
            "What are the five pillars of Islam?",
            "How to become a Muslim?"
        ]
    }
    
    return {
        "status": "success",
        "suggestions": suggestions,
        "message": "Click any question to get an answer"
    }

@router.get("/history", response_model=Dict[str, Any])
async def get_chat_history(
    current_user: User = Depends(optional_authentication),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get chat history for authenticated users.
    """
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required to view history"
        )
    
    # Would fetch from database
    return {
        "status": "success",
        "user": current_user.username,
        "history": [],
        "message": "History feature coming soon"
    }

@router.post("/feedback", response_model=Dict[str, Any])
async def submit_feedback(
    response_id: str = Query(..., description="Response ID"),
    rating: int = Query(..., ge=1, le=5, description="Rating (1-5)"),
    feedback: Optional[str] = Query(None, description="Additional feedback"),
    current_user: Optional[User] = Depends(optional_authentication)
):
    """
    Submit feedback on AI responses to improve the system.
    """
    # Would save to database
    return {
        "status": "success",
        "message": "JazakAllah khair for your feedback!",
        "response_id": response_id,
        "rating": rating
    }
    
@router.get("/health")
async def chat_health():
    """Health check."""
    return {"status": "chat_ready"}

@router.get("/disclaimer", response_model=Dict[str, str])
async def get_disclaimer():
    """
    Get important disclaimers about using the AI system.
    """
    return {
        "general": "This AI system provides Islamic information based on Quran and authentic Hadith. However, it is not a substitute for qualified scholarly advice.",
        "fiqh": "For fiqh (jurisprudence) matters, rulings may vary among recognized madhabs. Consult local scholars for personal matters.",
        "accuracy": "While we strive for accuracy, always verify information with authentic sources and qualified scholars.",
        "responsibility": "Users are responsible for verifying any information before acting upon it.",
        "reminder": "Allah knows best (والله أعلم)"
    }