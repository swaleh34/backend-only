from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.quran_service import QuranService
from app.services.cache_service import cache_service
from app.api.dependencies import (
    get_quran_service, 
    common_pagination, 
    language_parameter,
    optional_authentication
)
from app.core.config import settings
import time

router = APIRouter()

@router.get("/surahs", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="quran_surahs", ttl=86400)  # Cache for 24 hours
async def get_all_surahs(
    language: str = Depends(language_parameter),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get list of all 114 Surahs with metadata.
    
    - **language**: Language for surah names (en, ar, ur, fr, es)
    """
    start_time = time.time()
    
    surahs = quran_service.get_surah_list(language)
    
    return {
        "status": "success",
        "total": len(surahs),
        "language": language,
        "surahs": surahs,
        "response_time": round(time.time() - start_time, 3),
        "source": "authentic"
    }

@router.get("/surah/{surah_id}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="quran_surah", ttl=86400)
async def get_surah_details(
    surah_id: int = Path(..., ge=1, le=114, description="Surah number (1-114)"),
    language: str = Depends(language_parameter),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get detailed information about a specific Surah.
    
    - **surah_id**: Surah number from 1 to 114
    - **language**: Language for names and translations
    """
    surahs = quran_service.get_surah_list(language)
    
    surah = next((s for s in surahs if s["id"] == surah_id), None)
    
    if not surah:
        raise HTTPException(
            status_code=404,
            detail=f"Surah {surah_id} not found"
        )
    
    return {
        "status": "success",
        "surah": surah,
        "language": language
    }

@router.get("/verse/{surah_id}/{verse_number}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="quran_verse", ttl=86400)
async def get_verse(
    surah_id: int = Path(..., ge=1, le=114, description="Surah number"),
    verse_number: int = Path(..., ge=1, description="Verse number"),
    include_translation: bool = Query(True, description="Include translation"),
    include_tafsir: bool = Query(False, description="Include tafsir"),
    translator: str = Query("Saheeh International", description="Translator name"),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get a specific Quranic verse with optional translation and tafsir.
    
    - **surah_id**: Surah number (1-114)
    - **verse_number**: Verse number within the surah
    - **include_translation**: Include English translation
    - **include_tafsir**: Include authentic tafsir
    - **translator**: Choose translator (default: Saheeh International)
    """
    verse = quran_service.get_verse(
        surah_id=surah_id,
        verse_number=verse_number,
        include_translation=include_translation,
        include_tafsir=include_tafsir,
        translator=translator
    )
    
    if not verse:
        raise HTTPException(
            status_code=404,
            detail=f"Verse {surah_id}:{verse_number} not found"
        )
    
    return {
        "status": "success",
        "verse": verse,
        "metadata": {
            "translator": translator if include_translation else None,
            "includes_tafsir": include_tafsir
        }
    }

@router.get("/search", response_model=Dict[str, Any])
async def search_quran(
    query: str = Query(..., min_length=2, description="Search query"),
    language: str = Depends(language_parameter),
    search_type: str = Query("translation", pattern="^(translation|arabic|tafsir)$"),
    page_params: dict = Depends(common_pagination),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Search the Quran by text, translation, or tafsir.
    
    - **query**: Search term (minimum 2 characters)
    - **language**: Language to search in
    - **search_type**: Type of search (translation, arabic, tafsir)
    """
    start_time = time.time()
    
    results = quran_service.search_quran(
        query=query,
        language=language,
        search_type=search_type,
        limit=page_params["limit"]
    )
    
    return {
        "status": "success",
        "query": query,
        "total_results": len(results),
        "results": results,
        "search_type": search_type,
        "language": language,
        "response_time": round(time.time() - start_time, 3)
    }

@router.get("/juz/{juz_number}", response_model=Dict[str, Any])
async def get_juz(
    juz_number: int = Path(..., ge=1, le=30, description="Juz number (1-30)"),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get information about a specific Juz (part) of the Quran.
    
    - **juz_number**: Juz number from 1 to 30
    """
    # This would query the database for juz information
    return {
        "status": "success",
        "juz": juz_number,
        "message": "Juz information endpoint - to be fully implemented"
    }

@router.get("/topics/{topic}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="quran_topic", ttl=3600)
async def get_verses_by_topic(
    topic: str = Path(..., min_length=2, description="Topic to search for"),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get Quranic verses related to a specific topic.
    
    - **topic**: Topic keyword (e.g., patience, prayer, charity)
    """
    verses = quran_service.get_verses_by_topic(topic)
    
    return {
        "status": "success",
        "topic": topic,
        "total_verses": len(verses),
        "verses": verses
    }

@router.get("/random", response_model=Dict[str, Any])
async def get_random_verse(
    language: str = Depends(language_parameter),
    quran_service: QuranService = Depends(get_quran_service)
):
    """
    Get a random verse from the Quran for reflection.
    """
    import random
    
    surah_id = random.randint(1, 114)
    # Get random verse number based on surah
    surah_verses = {
        1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206,
        8: 75, 9: 129, 10: 109, 11: 123, 12: 111, 13: 43, 14: 52,
        15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135
        # Add all surahs...
    }
    
    max_verse = surah_verses.get(surah_id, 100)
    verse_number = random.randint(1, max_verse)
    
    verse = quran_service.get_verse(
        surah_id=surah_id,
        verse_number=verse_number,
        include_translation=True
    )
    
    return {
        "status": "success",
        "verse": verse,
        "message": "Ayah for reflection"
    }
