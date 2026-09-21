"""
Advanced Islamic Search Engine
Combines keyword search, semantic search, and vector similarity
"""
from typing import List, Dict, Any, Optional
from app.services.islamic_corpus import (
    search_qa, search_quran_verses, search_hadith, 
    ISLAMIC_QA, QURAN_FULL_TEXT, AUTHENTIC_HADITH
)
from app.services.islamic_knowledge_base import search_knowledge_base

class AdvancedIslamicSearch:
    """Multi-strategy search for Islamic content"""
    
    def __init__(self):
        self.search_strategies = [
            self._search_qa_database,
            self._search_knowledge_base,
            self._search_quran,
            self._search_hadith,
            self._keyword_search
        ]
    
    def comprehensive_search(self, query: str) -> Dict[str, Any]:
        """Perform comprehensive search across all sources"""
        results = {
            "qa_matches": [],
            "quran_verses": [],
            "hadith": [],
            "knowledge_base": None,
            "best_answer": None,
            "source_type": None
        }
        
        # Search Q&A database
        qa_result = search_qa(query)
        if qa_result:
            results["qa_matches"].append(qa_result)
            results["best_answer"] = qa_result
            results["source_type"] = "Islamic Q&A Database"
        
        # Search Quran
        quran_results = search_quran_verses(query)
        if quran_results:
            results["quran_verses"] = quran_results
        
        # Search Hadith
        hadith_results = search_hadith(query)
        if hadith_results:
            results["hadith"] = hadith_results
        
        # Search Knowledge Base
        kb_result = search_knowledge_base(query)
        if kb_result:
            results["knowledge_base"] = kb_result
            if not results["best_answer"]:
                results["best_answer"] = kb_result
                results["source_type"] = "Islamic Knowledge Base"
        
        return results
    
    def _search_qa_database(self, query: str) -> Optional[str]:
        return search_qa(query)
    
    def _search_knowledge_base(self, query: str) -> Optional[str]:
        return search_knowledge_base(query)
    
    def _search_quran(self, query: str) -> List[Dict]:
        return search_quran_verses(query)
    
    def _search_hadith(self, query: str) -> List[Dict]:
        return search_hadith(query)
    
    def _keyword_search(self, query: str) -> Optional[str]:
        """Fallback keyword-based search"""
        query_lower = query.lower()
        
        # Expanded keyword matching
        keyword_map = {
            "tawheed": "Tawheed is the belief in the Oneness of Allah...",
            "shirk": "Shirk is associating partners with Allah, the greatest sin...",
            "jannah": "Jannah (Paradise) is the eternal reward for the righteous...",
            "jahannam": "Jahannam (Hell) is the punishment for disbelievers and sinners...",
            "sahabah": "The Sahabah were the companions of Prophet Muhammad (ﷺ)...",
            "sunnah": "Sunnah refers to the teachings and practices of Prophet Muhammad (ﷺ)...",
            "sharia": "Sharia is Islamic law derived from Quran and Sunnah...",
            "fatwa": "A fatwa is a legal opinion issued by a qualified Islamic scholar...",
            "imam": "An imam leads prayer and provides religious guidance...",
            "masjid": "A masjid (mosque) is the place of worship for Muslims...",
            "kaaba": "The Kaaba is the sacred house of Allah in Makkah, the Qibla for Muslims...",
            "adhan": "The Adhan is the call to prayer, announced 5 times daily...",
            "iqama": "The Iqama is the second call to prayer, said just before the prayer begins...",
        }
        
        for key, answer in keyword_map.items():
            if key in query_lower:
                return answer
        
        return None

# Global instance
advanced_search = AdvancedIslamicSearch()