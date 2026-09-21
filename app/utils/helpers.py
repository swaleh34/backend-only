from typing import Any, Dict, List, Optional
import json
import re
from datetime import datetime, timedelta
import arabic_reshaper
from bidi.algorithm import get_display
from app.core.config import settings

class IslamicHelpers:
    """Islamic helper functions"""
    
    @staticmethod
    def format_arabic_text(text: str, reshape: bool = True) -> str:
        """Format Arabic text for proper display"""
        if reshape:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        return text
    
    @staticmethod
    def get_bismillah() -> str:
        """Get Bismillah in Arabic"""
        return "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    
    @staticmethod
    def get_salawat() -> str:
        """Get Salawat on Prophet"""
        return "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ"
    
    @staticmethod
    def get_common_duas() -> Dict[str, Dict[str, str]]:
        """Get common duas"""
        return {
            "before_eating": {
                "arabic": "بِسْمِ اللَّهِ",
                "transliteration": "Bismillah",
                "translation": "In the name of Allah"
            },
            "after_eating": {
                "arabic": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مُسْلِمِينَ",
                "transliteration": "Alhamdulillahil-ladhi at'amana wa saqana wa ja'alana muslimeen",
                "translation": "Praise be to Allah who fed us and gave us drink and made us Muslims"
            },
            "before_sleep": {
                "arabic": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
                "transliteration": "Bismika Allahumma amutu wa ahya",
                "translation": "In Your name O Allah, I die and I live"
            },
            "morning_dhikr": {
                "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ",
                "transliteration": "Asbahna wa asbahal mulku lillah",
                "translation": "We have entered the morning and the dominion belongs to Allah"
            }
        }
    
    @staticmethod
    def get_prayer_times_info() -> Dict[str, Dict]:
        """Get information about prayer times"""
        return {
            "fajr": {
                "name": "Fajr",
                "arabic": "الفجر",
                "rakats_sunnah": 2,
                "rakats_fard": 2,
                "time": "Dawn to sunrise",
                "importance": "high"
            },
            "dhuhr": {
                "name": "Dhuhr",
                "arabic": "الظهر",
                "rakats_sunnah": 4,
                "rakats_fard": 4,
                "time": "After zenith to mid-afternoon",
                "importance": "high"
            },
            "asr": {
                "name": "Asr",
                "arabic": "العصر",
                "rakats_sunnah": 0,
                "rakats_fard": 4,
                "time": "Mid-afternoon to sunset",
                "importance": "high"
            },
            "maghrib": {
                "name": "Maghrib",
                "arabic": "المغرب",
                "rakats_sunnah": 2,
                "rakats_fard": 3,
                "time": "Sunset to dusk",
                "importance": "high"
            },
            "isha": {
                "name": "Isha",
                "arabic": "العشاء",
                "rakats_sunnah": 2,
                "rakats_fard": 4,
                "time": "Dusk to midnight",
                "importance": "high"
            }
        }
    
    @staticmethod
    def extract_quran_references(text: str) -> List[Dict[str, int]]:
        """Extract Quran references from text"""
        patterns = [
            r'Quran\s+(\d+):(\d+)',
            r'Surah\s+(\d+),\s*verse\s+(\d+)',
            r'(\d+):(\d+)'
        ]
        
        references = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for surah, verse in matches:
                surah_num = int(surah)
                verse_num = int(verse)
                if 1 <= surah_num <= 114:
                    references.append({
                        "surah": surah_num,
                        "verse": verse_num
                    })
        
        return references
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s\-\.\,\!\?\:\;\(\)\[\]\{\}\@\#\$\%\^\&\*\+\=\/\|\\\'\"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def generate_response_id() -> str:
        """Generate unique response ID"""
        import uuid
        import time
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"swlh-{timestamp}-{unique_id}"

class DateHelpers:
    """Date and time helper functions"""
    
    @staticmethod
    def get_hijri_date() -> Dict[str, Any]:
        """Get current Hijri date (approximate)"""
        # This is a simplified conversion
        # In production, use a proper Hijri calendar library
        gregorian_date = datetime.now()
        
        # Approximate Hijri year calculation
        hijri_year = int((gregorian_date.year - 622) * 1.0307)
        
        hijri_months = [
            "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
            "Jumada al-Ula", "Jumada al-Thani", "Rajab", "Sha'ban",
            "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
        ]
        
        # This is highly simplified - use proper library for accuracy
        month_index = (gregorian_date.month - 1) % 12
        
        return {
            "hijri_year": hijri_year,
            "hijri_month": hijri_months[month_index],
            "hijri_month_arabic": hijri_months[month_index],  # Would be Arabic in production
            "gregorian_date": gregorian_date.strftime("%Y-%m-%d"),
            "is_approximate": True
        }
    
    @staticmethod
    def get_islamic_events() -> List[Dict[str, str]]:
        """Get important Islamic dates"""
        return [
            {
                "event": "Ramadan",
                "description": "Month of fasting",
                "importance": "major",
                "duration": "29-30 days"
            },
            {
                "event": "Eid al-Fitr",
                "description": "Festival of breaking the fast",
                "importance": "major",
                "duration": "1 day"
            },
            {
                "event": "Eid al-Adha",
                "description": "Festival of sacrifice",
                "importance": "major",
                "duration": "3 days"
            },
            {
                "event": "Hajj",
                "description": "Annual pilgrimage to Makkah",
                "importance": "major",
                "duration": "5-6 days"
            },
            {
                "event": "Laylat al-Qadr",
                "description": "Night of Power",
                "importance": "major",
                "duration": "1 night"
            },
            {
                "event": "Ashura",
                "description": "10th of Muharram",
                "importance": "significant",
                "duration": "1 day"
            }
        ]

class TextHelpers:
    """Text processing helpers"""
    
    @staticmethod
    def highlight_arabic(text: str) -> str:
        """Wrap Arabic text in spans for styling"""
        arabic_pattern = re.compile(r'([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')
        return arabic_pattern.sub(r'<span class="arabic-text">\1</span>', text)
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(' ', 1)[0] + suffix
    
    @staticmethod
    def get_keywords(text: str) -> List[str]:
        """Extract keywords from text"""
        # Remove common words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return list(set(keywords))[:10]

# Create instances
islamic_helpers = IslamicHelpers()
date_helpers = DateHelpers()
text_helpers = TextHelpers()
