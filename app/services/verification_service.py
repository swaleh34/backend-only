from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import re
from datetime import datetime
from app.core.config import settings

class VerificationService:
    """Service for verifying Islamic content authenticity"""
    
    def __init__(self):
        self.authentic_collections = settings.AUTHENTIC_HADITH_COLLECTIONS
        self.authentic_tafsir = settings.AUTHENTIC_TAFSIR
        self.authentic_madhabs = settings.AUTHENTIC_MADHABS
        
        # Define acceptable grades
        self.acceptable_grades = ["Sahih", "Hasan", "Sahih li ghairihi", "Hasan li ghairihi"]
        self.weak_grades = ["Da'if", "Da'if jiddan", "Mawdu", "Munkar"]
    
    def verify_quran_reference(self, surah_number: int, verse_number: int) -> bool:
        """Verify if Quran reference is valid"""
        # Quran has 114 surahs
        if surah_number < 1 or surah_number > 114:
            return False
        
        # Each surah has specific number of verses
        surah_verses = {
            1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206,
            8: 75, 9: 129, 10: 109, 11: 123, 12: 111, 13: 43, 14: 52,
            15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135, 21: 112,
            22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88,
            29: 69, 30: 60, 31: 34, 32: 30, 33: 73, 34: 54, 35: 45,
            36: 83, 37: 182, 38: 88, 39: 75, 40: 85, 41: 54, 42: 53,
            43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18,
            50: 45, 51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96,
            57: 29, 58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11,
            64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44,
            71: 28, 72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50,
            78: 40, 79: 46, 80: 42, 81: 29, 82: 19, 83: 36, 84: 25,
            85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20, 91: 15,
            92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8,
            99: 8, 100: 11, 101: 11, 102: 8, 103: 3, 104: 9, 105: 5,
            106: 4, 107: 7, 108: 3, 109: 6, 110: 3, 111: 5, 112: 4,
            113: 5, 114: 6
        }
        
        if surah_number in surah_verses:
            return 1 <= verse_number <= surah_verses[surah_number]
        
        return False
    
    def verify_hadith_authenticity(
        self, 
        collection_name: str, 
        grade: str
    ) -> Dict[str, Any]:
        """Verify hadith authenticity based on collection and grade"""
        
        is_authentic_collection = collection_name in self.authentic_collections
        is_authentic_grade = grade in self.acceptable_grades
        is_weak_grade = grade in self.weak_grades
        
        if is_authentic_collection and is_authentic_grade:
            status = "authentic"
            confidence = 0.9
            explanation = f"From authentic collection ({collection_name}) with authentic grade ({grade})"
        elif is_authentic_collection and is_weak_grade:
            status = "weak"
            confidence = 0.3
            explanation = f"From authentic collection but with weak grade ({grade})"
        elif not is_authentic_collection and is_authentic_grade:
            status = "acceptable"
            confidence = 0.6
            explanation = "Authentic grade but from less-known collection"
        else:
            status = "unverified"
            confidence = 0.1
            explanation = "Unable to verify authenticity"
        
        return {
            "status": status,
            "confidence": confidence,
            "explanation": explanation,
            "collection_authentic": is_authentic_collection,
            "grade_authentic": is_authentic_grade,
            "recommendation": self._get_recommendation(status)
        }
    
    def verify_fiqh_ruling(
        self,
        madhab: str,
        scholar: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify fiqh ruling authenticity"""
        
        is_recognized_madhab = madhab in self.authentic_madhabs
        
        if is_recognized_madhab:
            status = "authentic"
            confidence = 0.85
            explanation = f"From recognized madhab: {madhab}"
        elif madhab == "General":
            status = "general"
            confidence = 0.7
            explanation = "General ruling without specific madhab attribution"
        else:
            status = "unverified"
            confidence = 0.3
            explanation = "From unrecognized or minority opinion"
        
        return {
            "status": status,
            "confidence": confidence,
            "explanation": explanation,
            "madhab_recognized": is_recognized_madhab,
            "recommendation": self._get_recommendation(status)
        }
    
    def verify_tafsir_source(self, tafsir_name: str) -> Dict[str, Any]:
        """Verify tafsir source authenticity"""
        
        is_authentic = tafsir_name in self.authentic_tafsir
        
        if is_authentic:
            status = "authentic"
            confidence = 0.9
            explanation = f"{tafsir_name} is a recognized authentic tafsir"
        else:
            status = "unverified"
            confidence = 0.4
            explanation = "Tafsir source not in authenticated list"
        
        return {
            "status": status,
            "confidence": confidence,
            "explanation": explanation,
            "is_authentic": is_authentic,
            "recommendation": self._get_recommendation(status)
        }
    
    def verify_islamic_claim(self, claim: str, source: str) -> Dict[str, Any]:
        """General Islamic claim verification"""
        
        # Check for common red flags
        red_flags = [
            "scientific miracle",
            "numerical miracle",
            "prediction",
            "only true",
            "all others wrong"
        ]
        
        has_red_flags = any(flag in claim.lower() for flag in red_flags)
        
        # Check source reliability
        reliable_sources = ["quran", "hadith", "scholarly consensus", "ijma"]
        has_reliable_source = any(rs in source.lower() for rs in reliable_sources)
        
        if has_red_flags and not has_reliable_source:
            return {
                "status": "suspicious",
                "confidence": 0.1,
                "warning": "This claim contains patterns common in unreliable Islamic information",
                "recommendation": "Verify with authentic sources and qualified scholars"
            }
        elif has_reliable_source:
            return {
                "status": "likely_authentic",
                "confidence": 0.7,
                "recommendation": "Verify specific details with original sources"
            }
        else:
            return {
                "status": "unverified",
                "confidence": 0.3,
                "recommendation": "Requires further verification from authentic sources"
            }
    
    def _get_recommendation(self, status: str) -> str:
        """Get recommendation based on verification status"""
        recommendations = {
            "authentic": "Can be used as evidence in Islamic rulings",
            "acceptable": "Can be used with caution, verify from other sources",
            "general": "General guidance, not for specific rulings",
            "weak": "Cannot be used as primary evidence",
            "unverified": "Requires verification from qualified scholars",
            "suspicious": "Avoid using this source"
        }
        return recommendations.get(status, "Verify with qualified scholars")
    
    def validate_arabic_text(self, text: str) -> Dict[str, Any]:
        """Validate Arabic text for common issues"""
        issues = []
        
        # Check for Quranic text markers
        if text.startswith('﷽') or '﷽' in text:
            issues.append("Contains Bismillah marker")
        
        # Check for proper Arabic characters
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        if not arabic_pattern.search(text):
            issues.append("No Arabic characters found")
        
        # Check for common typos
        common_typos = {
            'الرحمن': 'الرحمان',
            'الصلوة': 'الصلاة',
            'الزكوة': 'الزكاة'
        }
        
        for correct, wrong in common_typos.items():
            if wrong in text:
                issues.append(f"Possible typo: {wrong} should be {correct}")
        
        return {
            "has_arabic": bool(arabic_pattern.search(text)),
            "has_issues": len(issues) > 0,
            "issues": issues,
            "is_valid": len(issues) == 0 or all("Possible typo" in i for i in issues)
        }
