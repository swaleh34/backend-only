from typing import Optional, List
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.quran_service import QuranService
from app.services.hadith_service import HadithService
from app.services.fiqh_service import FiqhService
from app.services.islamic_ai_service import IslamicAIService
from app.services.verification_service import VerificationService
from app.services.cache_service import cache_service
from app.services.auth_service import auth_service
from app.models.user import User

def get_quran_service(db: Session = Depends(get_db)) -> QuranService:
    return QuranService(db)

def get_hadith_service(db: Session = Depends(get_db)) -> HadithService:
    return HadithService(db)

def get_fiqh_service(db: Session = Depends(get_db)) -> FiqhService:
    return FiqhService(db)

def get_islamic_ai_service(db: Session = Depends(get_db)) -> IslamicAIService:
    return IslamicAIService(db)

def get_verification_service() -> VerificationService:
    return VerificationService()

async def common_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    return {
        "skip": (page - 1) * limit,
        "limit": limit,
        "page": page
    }

async def language_parameter(
    language: str = Query("en", description="Language code")
):
    return language

async def optional_authentication(
    current_user: Optional[User] = Depends(auth_service.get_current_user)
):
    return current_user