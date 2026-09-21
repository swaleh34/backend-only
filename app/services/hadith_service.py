from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from app.models.hadith import (
    HadithCollection, Hadith, HadithChapter, 
    HadithNarrator, HadithGrade
)
from app.core.config import settings
import json
import re
from datetime import datetime

class HadithService:
    """Advanced Hadith Service with authentication verification"""
    
    def __init__(self, db: Session):
        self.db = db
        self.authentic_collections = settings.AUTHENTIC_HADITH_COLLECTIONS
    
    def get_collections(self) -> List[Dict]:
        """Get all hadith collections with metadata"""
        collections = self.db.query(HadithCollection).filter(
            HadithCollection.is_active == True
        ).all()
        
        return [
            {
                "id": c.id,
                "name": c.collection_name,
                "compiler": c.compiler_name,
                "compiler_full_name": c.compiler_full_name,
                "total_hadith": c.total_hadith,
                "authenticity": c.authenticity_grade,
                "description": c.description,
                "methodology": c.methodology,
                "birth_year": c.birth_year,
                "death_year": c.death_year,
                "compilation_date": c.compilation_date,
                "is_authentic_source": c.collection_name in self.authentic_collections
            }
            for c in collections
        ]
    
    def search_hadith(
        self,
        query: str,
        collection_name: Optional[str] = None,
        grade: Optional[str] = None,
        topic: Optional[str] = None,
        language: str = "en",
        limit: int = 10,
        authenticate_only: bool = True
    ) -> List[Dict]:
        """Advanced hadith search with multiple filters"""
        
        filters = []
        
        # Text search
        if language == "en":
            text_filter = Hadith.matn_english.contains(query)
        elif language == "ar":
            text_filter = Hadith.matn_arabic.contains(query)
        else:
            text_filter = or_(
                Hadith.matn_english.contains(query),
                Hadith.matn_arabic.contains(query)
            )
        filters.append(text_filter)
        
        # Collection filter
        if collection_name:
            collection = self.db.query(HadithCollection).filter(
                HadithCollection.collection_name == collection_name
            ).first()
            if collection:
                filters.append(Hadith.collection_id == collection.id)
        
        # Grade filter
        if grade:
            filters.append(Hadith.grade == grade)
        
        # Topic filter
        if topic:
            filters.append(Hadith.topics.contains(topic))
        
        # Authenticity filter
        if authenticate_only:
            filters.append(Hadith.is_authentic_hadith == True)
            filters.append(Hadith.grade.in_(['Sahih', 'Hasan']))
        
        # Execute query
        hadiths = self.db.query(Hadith).filter(
            and_(*filters)
        ).order_by(
            desc(Hadith.grade == 'Sahih'),
            Hadith.collection_id
        ).limit(limit).all()
        
        return [
            {
                "id": h.id,
                "collection": h.collection.collection_name if h.collection else None,
                "hadith_number": h.hadith_number,
                "book_number": h.book_number,
                "chapter_number": h.chapter_number,
                "narrator_chain_english": h.isnad_english,
                "text_arabic": h.matn_arabic,
                "text_english": h.matn_english,
                "grade": h.grade,
                "graded_by": h.graded_by,
                "topics": json.loads(h.topics) if h.topics else [],
                "benefits": h.benefits,
                "is_authentic": h.is_authentic_hadith,
                "references": {
                    "quran": json.loads(h.quran_reference) if h.quran_reference else [],
                    "similar_hadith": json.loads(h.similar_hadith) if h.similar_hadith else []
                }
            }
            for h in hadiths
        ]
    
    def get_hadith_by_id(self, hadith_id: int) -> Optional[Dict]:
        """Get complete hadith with all details"""
        hadith = self.db.query(Hadith).filter(Hadith.id == hadith_id).first()
        
        if not hadith:
            return None
        
        narrators = [
            {
                "name": n.narrator_name,
                "full_name": n.narrator_full_name,
                "order": n.order_in_chain,
                "reliability": n.reliability,
                "biography": n.biography
            }
            for n in hadith.narrators
        ]
        
        collection = hadith.collection
        chapter = hadith.chapter
        
        return {
            "id": hadith.id,
            "collection": {
                "name": collection.collection_name if collection else None,
                "compiler": collection.compiler_name if collection else None,
                "authenticity": collection.authenticity_grade if collection else None
            },
            "chapter": {
                "name_arabic": chapter.chapter_name_arabic if chapter else None,
                "name_english": chapter.chapter_name_english if chapter else None,
                "book_name": chapter.book_name_english if chapter else None
            },
            "hadith_number": hadith.hadith_number,
            "international_number": hadith.international_number,
            "isnad": {
                "arabic": hadith.isnad_arabic,
                "english": hadith.isnad_english
            },
            "narrator_chain": json.loads(hadith.narrator_chain) if hadith.narrator_chain else [],
            "narrators": narrators,
            "matn": {
                "arabic": hadith.matn_arabic,
                "english": hadith.matn_english,
                "urdu": hadith.matn_urdu
            },
            "grading": {
                "grade": hadith.grade,
                "graded_by": hadith.graded_by,
                "reason": hadith.grading_reason
            },
            "topics": json.loads(hadith.topics) if hadith.topics else [],
            "keywords": json.loads(hadith.keywords) if hadith.keywords else [],
            "rulings": hadith.rulings,
            "benefits": hadith.benefits,
            "is_authentic": hadith.is_authentic_hadith,
            "verified_by": hadith.verified_by,
            "references": {
                "quran": json.loads(hadith.quran_reference) if hadith.quran_reference else [],
                "similar_hadith": json.loads(hadith.similar_hadith) if hadith.similar_hadith else []
            }
        }
    
    def get_hadiths_by_topic(self, topic: str, limit: int = 20) -> List[Dict]:
        """Get hadiths related to a specific topic"""
        return self.search_hadith(
            query=topic,
            topic=topic,
            limit=limit,
            authenticate_only=True
        )
    
    def verify_hadith_chain(self, hadith_id: int) -> Dict:
        """Verify the chain of narration (Isnad)"""
        hadith = self.db.query(Hadith).filter(Hadith.id == hadith_id).first()
        
        if not hadith:
            return {"error": "Hadith not found"}
        
        narrators = hadith.narrators
        chain_analysis = {
            "total_narrators": len(narrators),
            "chain_connected": True,
            "narrator_reliability": [],
            "chain_strength": "Unknown"
        }
        
        for i, narrator in enumerate(narrators):
            reliability = narrator.reliability or "Unknown"
            chain_analysis["narrator_reliability"].append({
                "name": narrator.narrator_name,
                "order": narrator.order_in_chain,
                "reliability": reliability,
                "era": f"{narrator.birth_year}-{narrator.death_year}" if narrator.birth_year else "Unknown"
            })
            
            if i > 0 and not self._check_chain_connection(narrators[i-1], narrator):
                chain_analysis["chain_connected"] = False
        
        reliable_count = sum(
            1 for n in chain_analysis["narrator_reliability"]
            if n["reliability"] in ["Thiqah", "Saduq", "Trustworthy"]
        )
        
        if chain_analysis["chain_connected"] and reliable_count == len(narrators):
            chain_analysis["chain_strength"] = "Strong (Sahih)"
        elif chain_analysis["chain_connected"] and reliable_count >= len(narrators) * 0.7:
            chain_analysis["chain_strength"] = "Good (Hasan)"
        else:
            chain_analysis["chain_strength"] = "Weak (Da'if)"
        
        return chain_analysis
    
    def _check_chain_connection(self, narrator1: HadithNarrator, narrator2: HadithNarrator) -> bool:
        """Check if two narrators could have met based on their eras"""
        try:
            death1 = int(narrator1.death_year) if narrator1.death_year else 0
            birth2 = int(narrator2.birth_year) if narrator2.birth_year else 9999
            return death1 >= birth2
        except:
            return True
    
    def get_authentic_collections_stats(self) -> Dict:
        """Get statistics about authentic collections"""
        stats = {}
        
        for collection_name in self.authentic_collections:
            collection = self.db.query(HadithCollection).filter(
                HadithCollection.collection_name == collection_name
            ).first()
            
            if collection:
                total = self.db.query(func.count(Hadith.id)).filter(
                    Hadith.collection_id == collection.id
                ).scalar()
                
                sahih = self.db.query(func.count(Hadith.id)).filter(
                    and_(
                        Hadith.collection_id == collection.id,
                        Hadith.grade == 'Sahih'
                    )
                ).scalar()
                
                stats[collection_name] = {
                    "total_hadith": total,
                    "sahih": sahih,
                    "percentage_sahih": round((sahih / total * 100) if total > 0 else 0, 2)
                }
        
        return stats