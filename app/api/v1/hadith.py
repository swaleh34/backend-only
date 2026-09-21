from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from app.services.hadith_service import HadithService
from app.services.verification_service import VerificationService
from app.services.cache_service import cache_service
from app.api.dependencies import (
    get_hadith_service,
    get_verification_service,
    common_pagination,
    language_parameter
)
import time

router = APIRouter()

@router.get("/collections", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="hadith_collections", ttl=86400)
async def get_collections(
    hadith_service: HadithService = Depends(get_hadith_service)
):
    """
    Get all authentic Hadith collections with metadata.
    """
    start_time = time.time()
    
    collections = hadith_service.get_collections()
    
    return {
        "status": "success",
        "total": len(collections),
        "collections": collections,
        "note": "All collections are from authentic Sunni sources",
        "response_time": round(time.time() - start_time, 3)
    }

@router.get("/search", response_model=Dict[str, Any])
async def search_hadith(
    query: str = Query(..., min_length=3, description="Search query"),
    collection: Optional[str] = Query(None, description="Filter by collection name"),
    grade: Optional[str] = Query(None, pattern="^(Sahih|Hasan|Da'if|Mawud)$"),
    language: str = Depends(language_parameter),
    authenticate_only: bool = Query(True, description="Show only authentic hadith"),
    page_params: dict = Depends(common_pagination),
    hadith_service: HadithService = Depends(get_hadith_service)
):
    """
    Search Hadith with advanced filters.
    
    - **query**: Search term in hadith text
    - **collection**: Filter by specific collection (e.g., Sahih Bukhari)
    - **grade**: Filter by authenticity grade
    - **authenticate_only**: Show only Sahih and Hasan hadith
    """
    start_time = time.time()
    
    results = hadith_service.search_hadith(
        query=query,
        collection_name=collection,
        grade=grade,
        language=language,
        limit=page_params["limit"],
        authenticate_only=authenticate_only
    )
    
    return {
        "status": "success",
        "query": query,
        "filters": {
            "collection": collection,
            "grade": grade,
            "authenticate_only": authenticate_only
        },
        "total_results": len(results),
        "results": results,
        "response_time": round(time.time() - start_time, 3)
    }

@router.get("/hadith/{hadith_id}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="hadith_detail", ttl=86400)
async def get_hadith_detail(
    hadith_id: int = Path(..., description="Hadith ID"),
    include_chain: bool = Query(True, description="Include chain of narration"),
    hadith_service: HadithService = Depends(get_hadith_service),
    verification_service: VerificationService = Depends(get_verification_service)
):
    """
    Get complete Hadith with chain of narration and verification.
    
    - **hadith_id**: Unique hadith identifier
    - **include_chain**: Include detailed chain of narration
    """
    hadith = hadith_service.get_hadith_by_id(hadith_id)
    
    if not hadith:
        raise HTTPException(
            status_code=404,
            detail=f"Hadith with ID {hadith_id} not found"
        )
    
    # Verify hadith authenticity
    if hadith.get("collection") and hadith.get("grading", {}).get("grade"):
        verification = verification_service.verify_hadith_authenticity(
            hadith["collection"]["name"],
            hadith["grading"]["grade"]
        )
    else:
        verification = {"status": "unverified"}
    
    # Verify chain if requested
    chain_verification = None
    if include_chain and hadith.get("isnad"):
        chain_verification = hadith_service.verify_hadith_chain(hadith_id)
    
    return {
        "status": "success",
        "hadith": hadith,
        "verification": verification,
        "chain_analysis": chain_verification,
        "disclaimer": "Verify with qualified scholars for important matters"
    }

@router.get("/topics/{topic}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="hadith_topic", ttl=3600)
async def get_hadith_by_topic(
    topic: str = Path(..., min_length=2, description="Topic keyword"),
    hadith_service: HadithService = Depends(get_hadith_service)
):
    """
    Get authentic Hadith related to a specific topic.
    
    - **topic**: Topic keyword (e.g., prayer, charity, honesty)
    """
    hadiths = hadith_service.get_hadiths_by_topic(topic)
    
    return {
        "status": "success",
        "topic": topic,
        "total": len(hadiths),
        "hadiths": hadiths,
        "note": "Showing authentic hadith only"
    }

@router.get("/daily", response_model=Dict[str, Any])
async def get_daily_hadith(
    hadith_service: HadithService = Depends(get_hadith_service)
):
    """
    Get a daily Hadith for reflection.
    """
    import random
    
    # Get a random authentic hadith
    daily_hadith = {
        "status": "success",
        "message": "Daily Hadith for reflection",
        "hadith": None  # Would fetch from database
    }
    
    return daily_hadith

@router.get("/verify/{hadith_id}", response_model=Dict[str, Any])
async def verify_hadith(
    hadith_id: int = Path(..., description="Hadith ID to verify"),
    hadith_service: HadithService = Depends(get_hadith_service),
    verification_service: VerificationService = Depends(get_verification_service)
):
    """
    Verify the authenticity of a specific Hadith.
    
    - **hadith_id**: Hadith ID to verify
    """
    hadith = hadith_service.get_hadith_by_id(hadith_id)
    
    if not hadith:
        raise HTTPException(status_code=404, detail="Hadith not found")
    
    # Verify collection and grade
    verification = verification_service.verify_hadith_authenticity(
        hadith.get("collection", {}).get("name", ""),
        hadith.get("grading", {}).get("grade", "")
    )
    
    # Verify chain
    chain_analysis = hadith_service.verify_hadith_chain(hadith_id)
    
    return {
        "status": "success",
        "hadith_reference": f"{hadith.get('collection', {}).get('name', 'Unknown')} #{hadith.get('hadith_number')}",
        "verification": verification,
        "chain_analysis": chain_analysis,
        "recommendation": verification.get("recommendation")
    }

@router.get("/stats", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="hadith_stats", ttl=86400)
async def get_hadith_stats(
    hadith_service: HadithService = Depends(get_hadith_service)
):
    """
    Get statistics about Hadith collections.
    """
    stats = hadith_service.get_authentic_collections_stats()
    
    return {
        "status": "success",
        "statistics": stats,
        "note": "Statistics for authentic collections only"
    }
