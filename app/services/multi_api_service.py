"""
Multi-API Integration Service for Swaleh AI
Orchestrates multiple Islamic APIs for comprehensive answers
"""
import httpx
import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from functools import lru_cache

class MultiAPIService:
    """Orchestrates multiple Islamic APIs"""
    
    def __init__(self):
        self.client = httpx.Client(timeout=20.0)
        self.async_client = httpx.AsyncClient(timeout=20.0)
        
        # API Endpoints
        self.apis = {
            "quran_cloud": "https://api.alquran.cloud/v1",
            "quran_com": "https://api.quran.com/api/v4",
            "hadith_api": "https://api.sunnah.com/v1",
            "aladhan": "http://api.aladhan.com/v1",
            "islamhouse": "https://api.islamhouse.com/v1",
        }
        
        # API availability tracking
        self.api_status = {}
        self._check_api_health()
    
    def _check_api_health(self):
        """Check which APIs are available"""
        print("🔍 Checking API availability...")
        
        apis_to_check = {
            "quran_cloud": f"{self.apis['quran_cloud']}/surah",
            "aladhan": f"{self.apis['aladhan']}/timings/1-1-2024",
        }
        
        for name, url in apis_to_check.items():
            try:
                response = self.client.get(url, timeout=5.0)
                self.api_status[name] = response.status_code == 200
                status = "✅" if self.api_status[name] else "❌"
                print(f"  {status} {name}")
            except:
                self.api_status[name] = False
                print(f"  ❌ {name} - unavailable")
    
    # ==================== QURAN APIS ====================
    
    def get_quran_verse(self, surah: int, ayah: int, edition: str = "en.sahih") -> Dict:
        """Get specific Quran verse from Quran Cloud API"""
        try:
            response = self.client.get(
                f"{self.apis['quran_cloud']}/ayah/{surah}:{ayah}/{edition}"
            )
            data = response.json()
            if data.get("code") == 200:
                return {
                    "arabic": data["data"]["text"],
                    "translation": data["data"]["text"],
                    "surah": data["data"]["surah"]["englishName"],
                    "ayah": data["data"]["numberInSurah"],
                    "source": "Quran Cloud API"
                }
        except:
            pass
        return self._fallback_quran_verse(surah, ayah)
    
    def get_surah_with_translation(self, surah: int, edition: str = "en.sahih") -> Dict:
        """Get complete surah with translation"""
        try:
            response = self.client.get(
                f"{self.apis['quran_cloud']}/surah/{surah}/{edition}"
            )
            data = response.json()
            if data.get("code") == 200:
                verses = []
                for ayah in data["data"]["ayahs"]:
                    verses.append({
                        "number": ayah["numberInSurah"],
                        "text": ayah["text"]
                    })
                return {
                    "name": data["data"]["englishName"],
                    "arabic_name": data["data"]["name"],
                    "verses": verses,
                    "source": "Quran Cloud API"
                }
        except:
            pass
        return {"error": "Could not fetch surah"}
    
    def search_quran_multi(self, query: str, language: str = "en") -> List[Dict]:
        """Search Quran across multiple APIs"""
        results = []
        
        # Try Quran.com API
        try:
            response = self.client.get(
                f"{self.apis['quran_com']}/search",
                params={"q": query, "language": language, "size": 5}
            )
            data = response.json()
            for result in data.get("search", {}).get("results", []):
                results.append({
                    "text": result.get("text", ""),
                    "surah": result.get("surah_name", ""),
                    "ayah": result.get("ayah", ""),
                    "source": "Quran.com API"
                })
        except:
            pass
        
        # Fallback to Quran Cloud
        if not results:
            try:
                response = self.client.get(
                    f"{self.apis['quran_cloud']}/search/{query}/all/en"
                )
                data = response.json()
                for match in data.get("data", {}).get("matches", [])[:5]:
                    results.append({
                        "text": match.get("text", ""),
                        "surah": match.get("surah", {}).get("englishName", ""),
                        "ayah": match.get("numberInSurah", ""),
                        "source": "Quran Cloud API"
                    })
            except:
                pass
        
        return results[:5]
    
    def get_tafsir(self, surah: int, ayah: int, tafsir: str = "en-tafsir-ibn-kathir") -> str:
        """Get tafsir for a verse"""
        try:
            response = self.client.get(
                f"{self.apis['quran_cloud']}/ayah/{surah}:{ayah}/{tafsir}"
            )
            data = response.json()
            if data.get("code") == 200:
                return data["data"]["text"]
        except:
            pass
        
        # Try Quran.com tafsir
        try:
            response = self.client.get(
                f"{self.apis['quran_com']}/tafsirs/{tafsir}/by_ayah/{surah}:{ayah}"
            )
            data = response.json()
            return data.get("tafsir", {}).get("text", "")
        except:
            pass
        
        return "Tafsir not available for this verse."
    
    # ==================== HADITH APIS ====================
    
    def get_hadith_from_api(self, collection: str, number: int) -> Dict:
        """Get specific hadith from Hadith API"""
        try:
            response = self.client.get(
                f"{self.apis['hadith_api']}/collections/{collection}/hadiths/{number}",
                headers={"X-API-Key": "demo"}
            )
            data = response.json()
            if data.get("status") == "success":
                hadith = data["data"]
                return {
                    "text": hadith.get("hadithText", ""),
                    "narrator": hadith.get("narrator", ""),
                    "grade": hadith.get("grade", ""),
                    "collection": collection,
                    "number": number,
                    "source": "Hadith API"
                }
        except:
            pass
        return {}
    
    def search_hadith_multi(self, query: str, collection: str = "bukhari") -> List[Dict]:
        """Search hadith across APIs"""
        results = []
        
        # Try Hadith API
        try:
            response = self.client.get(
                f"{self.apis['hadith_api']}/hadiths/search",
                params={"q": query, "collection": collection, "limit": 5},
                headers={"X-API-Key": "demo"}
            )
            data = response.json()
            for hadith in data.get("data", []):
                results.append({
                    "text": hadith.get("hadithText", ""),
                    "collection": collection,
                    "grade": hadith.get("grade", ""),
                    "source": "Hadith API"
                })
        except:
            pass
        
        return results[:5]
    
    def get_hadith_collections(self) -> List[Dict]:
        """Get available hadith collections"""
        return [
            {"name": "Sahih al-Bukhari", "id": "bukhari", "hadiths": 7563},
            {"name": "Sahih Muslim", "id": "muslim", "hadiths": 4000},
            {"name": "Sunan Abu Dawud", "id": "abudawud", "hadiths": 4800},
            {"name": "Jami al-Tirmidhi", "id": "tirmidhi", "hadiths": 3956},
            {"name": "Sunan al-Nasa'i", "id": "nasai", "hadiths": 5761},
            {"name": "Sunan Ibn Majah", "id": "ibnmajah", "hadiths": 4341},
            {"name": "Muwatta Malik", "id": "malik", "hadiths": 1720},
            {"name": "Musnad Ahmad", "id": "ahmad", "hadiths": 27647},
            {"name": "Riyad as-Salihin", "id": "riyad", "hadiths": 1896},
            {"name": "40 Hadith Nawawi", "id": "nawawi", "hadiths": 42},
        ]
    
    # ==================== PRAYER TIMES ====================
    
    def get_prayer_times(self, city: str = "Makkah", country: str = "SA", method: int = 4) -> Dict:
        """Get prayer times from Aladhan API"""
        try:
            today = datetime.now()
            response = self.client.get(
                f"{self.apis['aladhan']}/timingsByCity",
                params={
                    "city": city,
                    "country": country,
                    "method": method,
                    "month": today.month,
                    "year": today.year
                }
            )
            data = response.json()
            if data.get("code") == 200:
                return {
                    "city": city,
                    "country": country,
                    "date": data["data"]["date"]["readable"],
                    "hijri": data["data"]["date"]["hijri"],
                    "timings": data["data"]["timings"],
                    "source": "Aladhan API"
                }
        except:
            pass
        return {"error": "Could not fetch prayer times"}
    
    def get_qibla_direction(self, lat: float = 21.4225, lng: float = 39.8262) -> Dict:
        """Get Qibla direction"""
        try:
            response = self.client.get(
                f"{self.apis['aladhan']}/qibla/{lat}/{lng}"
            )
            data = response.json()
            if data.get("code") == 200:
                return {
                    "direction": data["data"]["direction"],
                    "latitude": lat,
                    "longitude": lng,
                    "source": "Aladhan API"
                }
        except:
            pass
        return {"direction": "Makkah, Saudi Arabia"}
    
    # ==================== ISLAMHOUSE API ====================
    
    def search_islamhouse(self, query: str, language: str = "en") -> List[Dict]:
        """Search IslamHouse for books, fatwas, articles"""
        results = []
        
        # Try IslamHouse API
        try:
            response = self.client.get(
                f"{self.apis['islamhouse']}/search",
                params={"q": query, "language": language, "limit": 5}
            )
            data = response.json()
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "type": item.get("type", ""),
                    "description": item.get("description", "")[:300],
                    "url": item.get("url", ""),
                    "source": "IslamHouse"
                })
        except:
            pass
        
        return results[:5]
    
    # ==================== FALLBACK METHODS ====================
    
    def _fallback_quran_verse(self, surah: int, ayah: int) -> Dict:
        """Fallback Quran verse data"""
        from app.services.islamic_corpus import QURAN_FULL_TEXT
        
        surah_data = QURAN_FULL_TEXT.get(str(surah), {})
        verse_text = surah_data.get("verses", {}).get(str(ayah), "Verse not found")
        
        return {
            "arabic": "",
            "translation": verse_text,
            "surah": surah_data.get("name", f"Surah {surah}"),
            "ayah": ayah,
            "source": "Local Database"
        }
    
    def get_api_status(self) -> Dict:
        """Get status of all APIs"""
        return self.api_status

# Global instance
multi_api = MultiAPIService()