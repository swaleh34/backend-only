from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.models.quran import (
    QuranMetadata, QuranVerse, QuranTranslation, 
    QuranTafsir, QuranWord
)
import json

class QuranService:
    """Advanced Quran Service with search and retrieval capabilities"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_surah_list(self, language: str = "en") -> List[Dict]:
        """Get list of all Surahs with metadata"""
        surahs = self.db.query(QuranMetadata).order_by(
            QuranMetadata.surah_id
        ).all()
        
        return [
            {
                "id": s.surah_id,
                "name_arabic": s.surah_name_arabic,
                "name_english": s.surah_name_english,
                "transliteration": s.surah_name_transliteration,
                "revelation_type": s.revelation_type,
                "total_verses": s.total_verses,
                "juz": s.juz,
                "meaning": s.meaning_english if language == "en" else s.meaning_urdu
            }
            for s in surahs
        ]
    
    def get_verse(
        self, 
        surah_id: int, 
        verse_number: int,
        include_translation: bool = True,
        include_tafsir: bool = False,
        translator: str = "Saheeh International"
    ) -> Optional[Dict]:
        """Get specific verse with optional translation and tafsir"""
        query = self.db.query(QuranVerse).filter(
            and_(
                QuranVerse.surah_id == surah_id,
                QuranVerse.verse_number == verse_number
            )
        )
        
        verse = query.first()
        if not verse:
            return None
        
        result = {
            "surah_id": verse.surah_id,
            "verse_number": verse.verse_number,
            "arabic_text": verse.arabic_text_uthmani,
            "verse_key": f"{surah_id}:{verse_number}",
            "juz": verse.juz_number,
            "page": verse.page_number,
            "audio_url": verse.audio_url
        }
        
        if include_translation:
            translation = self.db.query(QuranTranslation).filter(
                and_(
                    QuranTranslation.verse_id == verse.id,
                    QuranTranslation.translator_name == translator,
                    QuranTranslation.is_authentic_translation == True
                )
            ).first()
            
            if translation:
                result["translation"] = {
                    "text": translation.translation_text,
                    "translator": translation.translator_name
                }
        
        if include_tafsir:
            tafsirs = self.db.query(QuranTafsir).filter(
                QuranTafsir.verse_id == verse.id
            ).all()
            
            result["tafsir"] = [
                {
                    "name": t.tafsir_name,
                    "scholar": t.scholar_name,
                    "text": t.tafsir_text_english or t.tafsir_text
                }
                for t in tafsirs if t.is_authentic_tafsir
            ]
        
        return result
    
    def search_quran(
        self,
        query: str,
        language: str = "en",
        search_type: str = "translation",
        limit: int = 10
    ) -> List[Dict]:
        """Advanced Quran search"""
        results = []
        
        if search_type == "translation":
            translations = self.db.query(QuranTranslation).filter(
                and_(
                    QuranTranslation.translation_text.contains(query),
                    QuranTranslation.language == language,
                    QuranTranslation.is_authentic_translation == True
                )
            ).limit(limit).all()
            
            for trans in translations:
                verse = trans.verse
                results.append({
                    "surah_id": verse.surah_id,
                    "verse_number": verse.verse_number,
                    "arabic_text": verse.arabic_text_uthmani,
                    "translation": trans.translation_text,
                    "translator": trans.translator_name,
                    "relevance": "translation_match"
                })
        
        elif search_type == "arabic":
            verses = self.db.query(QuranVerse).filter(
                or_(
                    QuranVerse.arabic_text.contains(query),
                    QuranVerse.arabic_text_uthmani.contains(query)
                )
            ).limit(limit).all()
            
            for verse in verses:
                results.append({
                    "surah_id": verse.surah_id,
                    "verse_number": verse.verse_number,
                    "arabic_text": verse.arabic_text_uthmani,
                    "relevance": "arabic_match"
                })
        
        return results
    
    def get_verses_by_topic(self, topic: str) -> List[Dict]:
        """Get verses related to a specific topic using keywords"""
        translations = self.db.query(QuranTranslation).filter(
            and_(
                QuranTranslation.translation_text.contains(topic),
                QuranTranslation.language == "en",
                QuranTranslation.is_authentic_translation == True
            )
        ).limit(20).all()
        
        results = []
        for trans in translations:
            verse = trans.verse
            surah = verse.surah
            results.append({
                "surah_name": surah.surah_name_english,
                "surah_id": verse.surah_id,
                "verse_number": verse.verse_number,
                "arabic_text": verse.arabic_text_uthmani,
                "translation": trans.translation_text,
                "translator": trans.translator_name
            })
        
        return results