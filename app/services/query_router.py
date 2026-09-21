"""
Intelligent Query Router
Routes questions to the most appropriate API/source
"""
from typing import Dict, Any, List, Optional, Tuple
import re

class QueryRouter:
    """Routes queries to the best data source"""
    
    def __init__(self):
        self.routes = {
            "quran_verse": self._is_quran_verse_query,
            "hadith_specific": self._is_specific_hadith_query,
            "fiqh_ruling": self._is_fiqh_query,
            "prayer_times": self._is_prayer_query,
            "tafsir": self._is_tafsir_query,
            "general_islamic": self._is_general_islamic_query,
        }
    
    def classify_query(self, query: str) -> Dict[str, Any]:
        """Classify query and determine best data sources"""
        query_lower = query.lower()
        
        result = {
            "type": "general",
            "sources": ["local_knowledge", "vector_store"],
            "priority": "local",
            "needs_api": False,
            "api_calls": []
        }
        
        # Check for Quran verse reference
        verse_match = re.search(r'(?:surah|chapter)?\s*(\d+)[:\s]+(\d+)', query_lower)
        if verse_match:
            result["type"] = "quran_verse"
            result["sources"] = ["quran_api", "tafsir_api"]
            result["priority"] = "api_first"
            result["needs_api"] = True
            result["api_calls"] = [{
                "api": "quran_cloud",
                "method": "get_quran_verse",
                "params": {"surah": int(verse_match.group(1)), "ayah": int(verse_match.group(2))}
            }]
            result["params"] = {
                "surah": int(verse_match.group(1)),
                "ayah": int(verse_match.group(2))
            }
            return result
        
        # Check for specific hadith request
        hadith_match = re.search(r'(?:hadith|hadeeth)\s*(?:number|#)?\s*(\d+)', query_lower)
        if hadith_match or any(w in query_lower for w in ["bukhari", "muslim", "tirmidhi", "narrated by"]):
            result["type"] = "hadith_specific"
            result["sources"] = ["hadith_api", "local_hadith"]
            result["priority"] = "api_first"
            result["needs_api"] = True
            result["api_calls"] = [{
                "api": "hadith_api",
                "method": "search_hadith_multi",
                "params": {"query": query}
            }]
            return result
        
        # Check for prayer times
        if any(w in query_lower for w in ["prayer time", "azan", "fajr time", "maghrib time"]):
            result["type"] = "prayer_times"
            result["sources"] = ["aladhan_api"]
            result["priority"] = "api_first"
            result["needs_api"] = True
            city = self._extract_city(query)
            result["api_calls"] = [{
                "api": "aladhan",
                "method": "get_prayer_times",
                "params": {"city": city}
            }]
            return result
        
        # Check for tafsir request
        if any(w in query_lower for w in ["tafsir", "explanation of verse", "interpretation"]):
            result["type"] = "tafsir"
            result["sources"] = ["tafsir_api"]
            result["priority"] = "api_first"
            result["needs_api"] = True
            return result
        
        # General Islamic question
        if any(w in query_lower for w in ["halal", "haram", "ruling", "fatwa", "permissible"]):
            result["type"] = "fiqh_ruling"
            result["sources"] = ["islamhouse", "local_fiqh"]
            result["priority"] = "hybrid"
            result["needs_api"] = True
            result["api_calls"] = [{
                "api": "islamhouse",
                "method": "search_islamhouse",
                "params": {"query": query}
            }]
        
        return result
    
    def _is_quran_verse_query(self, query: str) -> bool:
        return bool(re.search(r'(?:surah|chapter)?\s*(\d+)[:\s]+(\d+)', query.lower()))
    
    def _is_specific_hadith_query(self, query: str) -> bool:
        return bool(re.search(r'hadith\s*(?:number|#)?\s*\d+', query.lower()))
    
    def _is_fiqh_query(self, query: str) -> bool:
        fiqh_words = ["halal", "haram", "ruling", "fatwa", "permissible", "allowed", "forbidden"]
        return any(w in query.lower() for w in fiqh_words)
    
    def _is_prayer_query(self, query: str) -> bool:
        prayer_words = ["prayer time", "azan", "fajr", "maghrib", "isha"]
        return any(w in query.lower() for w in prayer_words)
    
    def _is_tafsir_query(self, query: str) -> bool:
        return any(w in query.lower() for w in ["tafsir", "explanation", "interpretation"])
    
    def _is_general_islamic_query(self, query: str) -> bool:
        islamic_words = ["islam", "muslim", "allah", "quran", "prophet", "prayer", "faith"]
        return any(w in query.lower() for w in islamic_words)
    
    def _extract_city(self, query: str) -> str:
        """Extract city name from query"""
        cities = ["makkah", "madina", "riyadh", "dubai", "london", "new york", "cairo", "istanbul"]
        for city in cities:
            if city in query.lower():
                return city.title()
        return "Makkah"

# Global instance
query_router = QueryRouter()