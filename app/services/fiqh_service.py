from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.fiqh import (
    Madhab, FiqhCategory, FiqhTopic, 
    FiqhRuling, FiqhScholar, FiqhEvidence
)
from app.core.config import settings
import json

class FiqhService:
    """Advanced Fiqh Service with comparative madhab analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.madhabs = settings.AUTHENTIC_MADHABS
    
    def get_madhabs(self) -> List[Dict]:
        """Get all madhabs with details"""
        madhabs = self.db.query(Madhab).filter(
            Madhab.is_active == True
        ).all()
        
        return [
            {
                "id": m.id,
                "name": m.madhab_name,
                "name_arabic": m.madhab_name_arabic,
                "founder": m.founder_name,
                "founded_year": m.founded_year,
                "description": m.description,
                "methodology": m.methodology,
                "major_books": json.loads(m.major_books) if m.major_books else [],
                "regions": json.loads(m.regions) if m.regions else []
            }
            for m in madhabs
        ]
    
    def get_categories(self) -> List[Dict]:
        """Get Fiqh categories (Ibadah, Mu'amalat, etc.)"""
        categories = self.db.query(FiqhCategory).filter(
            FiqhCategory.parent_category_id == None
        ).all()
        
        result = []
        for cat in categories:
            subcategories = self.db.query(FiqhCategory).filter(
                FiqhCategory.parent_category_id == cat.id
            ).all()
            
            result.append({
                "id": cat.id,
                "name": cat.category_name,
                "name_arabic": cat.category_name_arabic,
                "description": cat.description,
                "subcategories": [
                    {
                        "id": sub.id,
                        "name": sub.category_name,
                        "name_arabic": sub.category_name_arabic,
                        "description": sub.description
                    }
                    for sub in subcategories
                ]
            })
        
        return result
    
    def search_rulings(
        self,
        query: str,
        madhab: Optional[str] = None,
        category: Optional[str] = None,
        ruling_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Advanced Fiqh ruling search"""
        
        filters = [FiqhRuling.is_active == True]
        
        # Text search in ruling text
        filters.append(
            or_(
                FiqhRuling.ruling_text.contains(query),
                FiqhRuling.topic_name_arabic.contains(query) if hasattr(FiqhRuling, 'topic_name_arabic') else FiqhRuling.ruling_text.contains(query),
                FiqhRuling.ruling_summary.contains(query)
            )
        )
        
        # Madhab filter
        if madhab:
            madhab_obj = self.db.query(Madhab).filter(
                Madhab.madhab_name == madhab
            ).first()
            if madhab_obj:
                filters.append(FiqhRuling.madhab_id == madhab_obj.id)
        
        # Category filter
        if category:
            cat_obj = self.db.query(FiqhCategory).filter(
                FiqhCategory.category_name == category
            ).first()
            if cat_obj:
                topic_ids = self.db.query(FiqhTopic.id).filter(
                    FiqhTopic.category_id == cat_obj.id
                ).all()
                filters.append(FiqhRuling.topic_id.in_([t[0] for t in topic_ids]))
        
        # Ruling type filter
        if ruling_type:
            filters.append(FiqhRuling.ruling_type == ruling_type)
        
        rulings = self.db.query(FiqhRuling).filter(
            and_(*filters)
        ).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "topic": r.topic.topic_name if r.topic else None,
                "topic_arabic": r.topic.topic_name_arabic if r.topic else None,
                "madhab": r.madhab.madhab_name if r.madhab else "General",
                "ruling_type": r.ruling_type,
                "ruling_arabic": r.ruling_arabic,
                "ruling_text": r.ruling_text,
                "ruling_summary": r.ruling_summary,
                "evidence": {
                    "quran": json.loads(r.quran_evidence) if r.quran_evidence else [],
                    "hadith": json.loads(r.hadith_evidence) if r.hadith_evidence else [],
                    "ijma": r.ijma_evidence,
                    "qiyas": r.qiyas_evidence
                },
                "scholar": r.scholar_name,
                "reference": {
                    "book": r.reference_book,
                    "page": r.reference_page
                },
                "complexity": r.complexity_level,
                "is_authentic": r.is_authentic,
                "conditions": json.loads(r.conditions) if r.conditions else [],
                "exceptions": json.loads(r.exceptions) if r.exceptions else []
            }
            for r in rulings
        ]
    
    def get_comparative_ruling(
        self,
        topic: str,
        include_evidence: bool = True
    ) -> Dict:
        """Get comparative rulings across all madhabs for a topic"""
        
        # Find topic
        topic_obj = self.db.query(FiqhTopic).filter(
            or_(
                FiqhTopic.topic_name.contains(topic),
                FiqhTopic.topic_name_arabic.contains(topic)
            )
        ).first()
        
        if not topic_obj:
            return {"error": "Topic not found"}
        
        # Get rulings for all madhabs
        rulings = self.db.query(FiqhRuling).filter(
            and_(
                FiqhRuling.topic_id == topic_obj.id,
                FiqhRuling.is_authentic == True
            )
        ).all()
        
        comparative_analysis = {
            "topic": topic_obj.topic_name,
            "topic_arabic": topic_obj.topic_name_arabic,
            "description": topic_obj.description,
            "rulings_by_madhab": {},
            "consensus": None,
            "differences": []
        }
        
        for ruling in rulings:
            madhab_name = ruling.madhab.madhab_name if ruling.madhab else "General"
            ruling_data = {
                "ruling_type": ruling.ruling_type,
                "ruling_text": ruling.ruling_text,
                "scholar": ruling.scholar_name,
                "reference": ruling.reference_book
            }
            
            if include_evidence:
                ruling_data["evidence"] = {
                    "quran": json.loads(ruling.quran_evidence) if ruling.quran_evidence else [],
                    "hadith": json.loads(ruling.hadith_evidence) if ruling.hadith_evidence else []
                }
            
            comparative_analysis["rulings_by_madhab"][madhab_name] = ruling_data
        
        # Analyze consensus and differences
        ruling_types = set(
            r.ruling_type for r in rulings
        )
        
        if len(ruling_types) == 1:
            comparative_analysis["consensus"] = f"All madhabs agree on: {list(ruling_types)[0]}"
        else:
            comparative_analysis["differences"] = [
                {
                    "madhab": r.madhab.madhab_name if r.madhab else "General",
                    "ruling": r.ruling_type,
                    "summary": r.ruling_summary
                }
                for r in rulings
            ]
        
        return comparative_analysis
    
    def get_ruling_types(self) -> List[Dict]:
        """Get all ruling types with explanations"""
        return [
            {
                "type": "Fard",
                "arabic": "فرض",
                "meaning": "Obligatory - must be performed",
                "example": "Five daily prayers",
                "sin_if_omitted": True
            },
            {
                "type": "Wajib",
                "arabic": "واجب",
                "meaning": "Necessary - highly emphasized",
                "example": "Witr prayer (according to Hanafi)",
                "sin_if_omitted": True
            },
            {
                "type": "Sunnah Mu'akkadah",
                "arabic": "سنة مؤكدة",
                "meaning": "Emphasized Sunnah - Prophet regularly performed",
                "example": "Taraweeh prayer",
                "sin_if_omitted": False
            },
            {
                "type": "Sunnah Ghair Mu'akkadah",
                "arabic": "سنة غير مؤكدة",
                "meaning": "Non-emphasized Sunnah - Prophet sometimes performed",
                "example": "4 rakahs before Isha",
                "sin_if_omitted": False
            },
            {
                "type": "Mustahab",
                "arabic": "مستحب",
                "meaning": "Recommended - reward for doing, no sin for leaving",
                "example": "Giving charity beyond zakat",
                "sin_if_omitted": False
            },
            {
                "type": "Mubah",
                "arabic": "مباح",
                "meaning": "Permissible - neither reward nor sin",
                "example": "Eating permissible food",
                "sin_if_omitted": False
            },
            {
                "type": "Makruh Tanzihi",
                "arabic": "مكروه تنزيهي",
                "meaning": "Slightly disliked - better to avoid",
                "example": "Eating garlic before mosque",
                "sin_if_omitted": False
            },
            {
                "type": "Makruh Tahrimi",
                "arabic": "مكروه تحريمي",
                "meaning": "Prohibitively disliked - close to haram",
                "example": "Wasting water in wudu",
                "sin_if_omitted": True
            },
            {
                "type": "Haram",
                "arabic": "حرام",
                "meaning": "Forbidden - must be avoided",
                "example": "Drinking alcohol",
                "sin_if_omitted": True
            }
        ]
