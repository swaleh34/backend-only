from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from app.services.fiqh_service import FiqhService
from app.services.verification_service import VerificationService
from app.services.cache_service import cache_service
from app.api.dependencies import (
    get_fiqh_service,
    get_verification_service,
    common_pagination,
    language_parameter
)
import time

router = APIRouter()

@router.get("/madhabs", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="fiqh_madhabs", ttl=86400)
async def get_madhabs(
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Get all recognized Islamic schools of thought (Madhabs).
    """
    start_time = time.time()
    
    madhabs = fiqh_service.get_madhabs()
    
    return {
        "status": "success",
        "total": len(madhabs),
        "madhabs": madhabs,
        "note": "All four major Sunni madhabs are recognized",
        "response_time": round(time.time() - start_time, 3)
    }

@router.get("/categories", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="fiqh_categories", ttl=86400)
async def get_categories(
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Get Fiqh categories and subcategories.
    """
    categories = fiqh_service.get_categories()
    
    return {
        "status": "success",
        "total": len(categories),
        "categories": categories
    }

@router.get("/rulings/search", response_model=Dict[str, Any])
async def search_rulings(
    query: str = Query(..., min_length=3, description="Search query"),
    madhab: Optional[str] = Query(None, description="Filter by madhab"),
    category: Optional[str] = Query(None, description="Filter by category"),
    ruling_type: Optional[str] = Query(
        None, 
        pattern="^(Fard|Wajib|Sunnah|Mustahab|Mubah|Makruh|Haram)$",
        description="Filter by ruling type"
    ),
    page_params: dict = Depends(common_pagination),
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Search Fiqh rulings with advanced filters.
    
    - **query**: Search term
    - **madhab**: Filter by school of thought
    - **category**: Filter by fiqh category
    - **ruling_type**: Filter by ruling type (Fard, Wajib, etc.)
    """
    start_time = time.time()
    
    results = fiqh_service.search_rulings(
        query=query,
        madhab=madhab,
        category=category,
        ruling_type=ruling_type,
        limit=page_params["limit"]
    )
    
    return {
        "status": "success",
        "query": query,
        "filters": {
            "madhab": madhab,
            "category": category,
            "ruling_type": ruling_type
        },
        "total_results": len(results),
        "results": results,
        "response_time": round(time.time() - start_time, 3)
    }

@router.get("/rulings/compare/{topic}", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="fiqh_compare", ttl=3600)
async def compare_rulings(
    topic: str = Path(..., min_length=2, description="Topic to compare"),
    include_evidence: bool = Query(True, description="Include evidence"),
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Compare Fiqh rulings across different Madhabs for a topic.
    
    - **topic**: Fiqh topic to compare
    - **include_evidence**: Include Quran and Hadith evidence
    """
    comparison = fiqh_service.get_comparative_ruling(topic, include_evidence)
    
    if "error" in comparison:
        raise HTTPException(status_code=404, detail=comparison["error"])
    
    return {
        "status": "success",
        "comparison": comparison,
        "note": "Differences of opinion among recognized madhabs are respected in Islam"
    }

@router.get("/rulings/types", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="fiqh_types", ttl=86400)
async def get_ruling_types(
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Get all Islamic ruling types with explanations.
    """
    ruling_types = fiqh_service.get_ruling_types()
    
    return {
        "status": "success",
        "total": len(ruling_types),
        "ruling_types": ruling_types
    }

@router.get("/scholars", response_model=Dict[str, Any])
@cache_service.cache_decorator(prefix="fiqh_scholars", ttl=86400)
async def get_scholars(
    madhab: Optional[str] = Query(None, description="Filter by madhab"),
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Get list of recognized Islamic scholars.
    """
    # This would query the database
    scholars = []  # Placeholder
    
    return {
        "status": "success",
        "total": len(scholars),
        "scholars": scholars,
        "message": "Endpoint to be fully implemented with database"
    }

@router.get("/fatwa/ask", response_model=Dict[str, Any])
async def ask_fatwa(
    question: str = Query(..., min_length=10, description="Your question"),
    madhab_preference: Optional[str] = Query(None, description="Preferred madhab"),
    fiqh_service: FiqhService = Depends(get_fiqh_service)
):
    """
    Get Islamic ruling on a specific question.
    
    - **question**: Your detailed question
    - **madhab_preference**: Preferred school of thought
    """
    # Search for similar rulings
    results = fiqh_service.search_rulings(
        query=question,
        madhab=madhab_preference,
        limit=5
    )
    
    if not results:
        return {
            "status": "warning",
            "message": "No specific ruling found. Please consult a qualified scholar.",
            "recommendation": "Visit your local mosque or Islamic center for guidance",
            "disclaimer": "Online fatwa should be verified with local scholars"
        }
    
    return {
        "status": "success",
        "question": question,
        "related_rulings": results,
        "disclaimer": "This is an automated response. For important matters, consult a qualified scholar.",
        "reminder": "Differences of opinion among recognized madhabs are valid and respected"
    }
