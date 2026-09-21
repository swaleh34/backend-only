"""
REAL ISLAMIC API INTEGRATION
Connects to authentic Islamic APIs for live data
"""
import httpx
from typing import Dict, Any, List, Optional

class RealIslamicAPI:
    """Direct integration with authentic Islamic APIs"""
    
    def __init__(self):
        self.client = httpx.Client(timeout=15.0)
        self.base_urls = {
            "quran": "https://api.alquran.cloud/v1",
            "quran_com": "https://api.quran.com/api/v4",
            "hadith": "https://api.sunnah.com/v1",
            "aladhan": "http://api.aladhan.com/v1",
        }
    
    # ========== QURAN APIS ==========
    
    def get_verse(self, surah: int, ayah: int, translation: str = "en.sahih") -> Dict:
        """Get specific Quran verse with translation"""
        try:
            resp = self.client.get(f"{self.base_urls['quran']}/ayah/{surah}:{ayah}/{translation}")
            data = resp.json()
            if data.get("code") == 200:
                d = data["data"]
                return {
                    "arabic": d.get("text", ""),
                    "translation": d.get("text", ""),
                    "surah_name": d.get("surah", {}).get("englishName", ""),
                    "surah_number": surah,
                    "ayah_number": ayah,
                    "source": "Quran Cloud API"
                }
        except Exception as e:
            print(f"API Error: {e}")
        return {}
    
    def search_quran(self, query: str, language: str = "en") -> List[Dict]:
        """Search the Quran for keywords"""
        results = []
        
        # Try Quran.com API
        try:
            resp = self.client.get(
                f"{self.base_urls['quran_com']}/search",
                params={"q": query, "language": language, "size": 5}
            )
            data = resp.json()
            for r in data.get("search", {}).get("results", []):
                results.append({
                    "text": r.get("text", ""),
                    "translation": r.get("translations", [{}])[0].get("text", "") if r.get("translations") else "",
                    "surah": r.get("verse", {}).get("chapter_id", ""),
                    "ayah": r.get("verse", {}).get("verse_number", ""),
                    "source": "Quran.com API"
                })
        except:
            pass
        
        # Fallback to Quran Cloud
        if not results:
            try:
                resp = self.client.get(f"{self.base_urls['quran']}/search/{query}/all/en")
                data = resp.json()
                for m in data.get("data", {}).get("matches", [])[:5]:
                    results.append({
                        "text": m.get("text", ""),
                        "surah": m.get("surah", {}).get("englishName", ""),
                        "ayah": m.get("numberInSurah", ""),
                        "source": "Quran Cloud API"
                    })
            except:
                pass
        
        return results
    
    def get_surah_list(self) -> List[Dict]:
        """Get list of all 114 surahs"""
        try:
            resp = self.client.get(f"{self.base_urls['quran']}/surah")
            data = resp.json()
            return data.get("data", [])
        except:
            return []
    
    def get_tafsir(self, surah: int, ayah: int) -> str:
        """Get tafsir for a verse"""
        try:
            resp = self.client.get(f"{self.base_urls['quran']}/ayah/{surah}:{ayah}/en.tafseer")
            data = resp.json()
            return data.get("data", {}).get("text", "")
        except:
            return ""
    
    # ========== HADITH API ==========
    
    def get_hadith(self, collection: str, number: int) -> Dict:
        """Get specific hadith"""
        try:
            resp = self.client.get(
                f"{self.base_urls['hadith']}/collections/{collection}/hadiths/{number}",
                headers={"X-API-Key": "demo"}
            )
            return resp.json().get("data", {})
        except:
            return {}
    
    def search_hadith_api(self, query: str) -> List[Dict]:
        """Search hadith"""
        try:
            resp = self.client.get(
                f"{self.base_urls['hadith']}/hadiths/search",
                params={"q": query, "limit": 5},
                headers={"X-API-Key": "demo"}
            )
            return resp.json().get("data", [])
        except:
            return []
    
    # ========== PRAYER TIMES ==========
    
    def get_prayer_times(self, city: str = "Makkah", country: str = "SA") -> Dict:
        """Get prayer times"""
        try:
            resp = self.client.get(
                f"{self.base_urls['aladhan']}/timingsByCity",
                params={"city": city, "country": country, "method": 4}
            )
            data = resp.json()
            return data.get("data", {})
        except:
            return {}

# Global instance
real_api = RealIslamicAPI()