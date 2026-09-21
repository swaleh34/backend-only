from app.services.islamic_corpus import search_qa, search_quran_verses, search_hadith, ISLAMIC_QA
from app.services.advanced_search import advanced_search
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import json
import re
from datetime import datetime
from app.services.quran_service import QuranService
from app.services.hadith_service import HadithService
from app.services.fiqh_service import FiqhService
from app.core.config import settings

class IslamicAIService:
    """Advanced Islamic AI with RAG (Retrieval-Augmented Generation)"""
    
    def __init__(self, db: Session):
        self.db = db
        self.quran_service = QuranService(db)
        self.hadith_service = HadithService(db)
        self.fiqh_service = FiqhService(db)
        self.authentic_sources = {
            "tafsir": settings.AUTHENTIC_TAFSIR,
            "hadith": settings.AUTHENTIC_HADITH_COLLECTIONS,
            "madhabs": settings.AUTHENTIC_MADHABS
        }
    
    def process_query(self, query, language="en", user_id=None, include_sources=True, authenticate_only=True):
        from app.services.free_llm import free_llm
        
        # Try free LLM first
        result = free_llm.ask(query)
        
        if result:
            return {
                "query": query,
                "answer": result["answer"],
                "confidence": result.get("confidence", 0.9),
                "sources": [result.get("source", "AI")] if include_sources else [],
                "disclaimer": "📚 Verify with qualified scholars. والله أعلم",
                "suggestions": self._get_suggestions(query, "general"),
                "timestamp": datetime.now().isoformat()
            }
        
        # Fallback to local knowledge
        from app.services.answer_engine import answer_engine
        result = answer_engine.answer(query)
        return {
            "query": query,
            "answer": result.get("answer", "No answer."),
            "confidence": result.get("confidence", 0.5),
            "sources": [result.get("source", "Local")] if include_sources else [],
            "disclaimer": "📚 Verify with qualified scholars. والله أعلم",
            "suggestions": self._get_suggestions(query, "general"),
            "timestamp": datetime.now().isoformat()
        }
    def _classify_query(self, query: str) -> str:
        """Classify the type of Islamic query"""
        query_lower = query.lower()
        
        # Quran-related
        quran_keywords = [
            "quran", "surah", "verse", "ayat", "chapter",
            "revelation", "juz", "hifz", "tajweed", "recitation",
            "tafsir", "meaning of surah", "explain verse"
        ]
        if any(keyword in query_lower for keyword in quran_keywords):
            return "quran"
        
        # Hadith-related
        hadith_keywords = [
            "hadith", "prophet said", "prophet muhammad said",
            "narration", "narrated", "sahih", "bukhari", "muslim",
            "sunan", "sunnah", "prophet's saying"
        ]
        if any(keyword in query_lower for keyword in hadith_keywords):
            return "hadith"
        
        # Fiqh-related
        fiqh_keywords = [
            "ruling", "halal", "haram", "fard", "wajib",
            "sunnah", "makruh", "allowed", "permissible",
            "forbidden", "obligatory", "prayer", "fasting",
            "zakat", "hajj", "wudu", "nikah", "talaq"
        ]
        if any(keyword in query_lower for keyword in fiqh_keywords):
            return "fiqh"
        
        # Aqeedah-related
        aqeedah_keywords = [
            "believe", "faith", "iman", "tawheed", "shirk",
            "paradise", "hell", "judgment day", "angels",
            "prophets", "books of allah", "qadr"
        ]
        if any(keyword in query_lower for keyword in aqeedah_keywords):
            return "aqeedah"
        
        # Seerah-related
        seerah_keywords = [
            "prophet life", "seerah", "companion", "sahabah",
            "battle", "migration", "hijrah", "prophet's family"
        ]
        if any(keyword in query_lower for keyword in seerah_keywords):
            return "seerah"
        
        return "general"
    
    
    def _retrieve_context(
        self, 
        query: str, 
        query_type: str, 
        language: str
    ) -> List[Dict]:
        """Retrieve relevant Islamic context based on query type"""
        context = []
        
        if query_type == "quran":
            # Search Quran
            quran_results = self.quran_service.search_quran(
                query, language, limit=5
            )
            context.extend([
                {
                    "type": "quran",
                    "surah_id": r.get("surah_id"),
                    "verse_number": r.get("verse_number"),
                    "text": r.get("arabic_text") if language == "ar" else r.get("translation"),
                    "reference": f"Quran {r.get('surah_id')}:{r.get('verse_number')}"
                }
                for r in quran_results
            ])
        
        elif query_type == "hadith":
            # Search Hadith
            hadith_results = self.hadith_service.search_hadith(
                query, language=language, limit=5
            )
            context.extend([
                {
                    "type": "hadith",
                    "collection": r.get("collection"),
                    "text": r.get("text_english") if language == "en" else r.get("text_arabic"),
                    "grade": r.get("grade"),
                    "reference": f"{r.get('collection')} #{r.get('hadith_number')}"
                }
                for r in hadith_results
            ])
        
        elif query_type == "fiqh":
            # Search Fiqh
            fiqh_results = self.fiqh_service.search_rulings(
                query, limit=5
            )
            context.extend([
                {
                    "type": "fiqh",
                    "madhab": r.get("madhab"),
                    "ruling": r.get("ruling_type"),
                    "text": r.get("ruling_text"),
                    "reference": r.get("reference", {}).get("book")
                }
                for r in fiqh_results
            ])
        
        else:
            # General search across all sources
            quran_results = self.quran_service.search_quran(query, language, limit=3)
            hadith_results = self.hadith_service.search_hadith(query, language=language, limit=3)
            
            context.extend([
                {
                    "type": "quran",
                    "text": r.get("translation"),
                    "reference": f"Quran {r.get('surah_id')}:{r.get('verse_number')}"
                }
                for r in quran_results
            ])
            
            context.extend([
                {
                    "type": "hadith",
                    "text": r.get("text_english"),
                    "grade": r.get("grade"),
                    "reference": f"{r.get('collection')} #{r.get('hadith_number')}"
                }
                for r in hadith_results
            ])
        
        return context
    
    def _verify_authenticity(self, context: List[Dict]) -> List[Dict]:
        """Verify the authenticity of retrieved sources"""
        verified_context = []
        
        for item in context:
            if item["type"] == "quran":
                # All Quran is authentic
                item["authenticity"] = "authentic"
                item["verified"] = True
                verified_context.append(item)
            
            elif item["type"] == "hadith":
                # Check if from authentic collection
                if item.get("collection") in self.authentic_sources["hadith"]:
                    if item.get("grade") in ["Sahih", "Hasan"]:
                        item["authenticity"] = "authentic"
                        item["verified"] = True
                        verified_context.append(item)
                    else:
                        item["authenticity"] = "weak"
                        item["verified"] = False
                else:
                    item["authenticity"] = "unverified"
                    item["verified"] = False
            
            elif item["type"] == "fiqh":
                # Check if from recognized madhab
                if item.get("madhab") in self.authentic_sources["madhabs"]:
                    item["authenticity"] = "authentic"
                    item["verified"] = True
                    verified_context.append(item)
                else:
                    item["authenticity"] = "general"
                    item["verified"] = True
                    verified_context.append(item)
        
        return verified_context
    
    def _generate_islamic_response(
        self,
        query: str,
        context: List[Dict],
        query_type: str,
        language: str
    ) -> Dict[str, Any]:
        """Generate Islamic response with proper citations"""
        
        if not context:
            return {
                "answer": self._get_no_context_response(query, language),
                "confidence": 0.1
            }
        
        # Build response from context
        response_parts = []
        confidence = 0.0
        
        if language == "en":
            response_parts.append("In the name of Allah, the Most Gracious, the Most Merciful.\n")
        else:
            response_parts.append("بسم الله الرحمن الرحيم\n")
        
        # Add contextual information
        for item in context:
            if item["type"] == "quran":
                response_parts.append(f"From the Quran ({item.get('reference', '')}):")
                response_parts.append(f"\"{item['text']}\"")
                confidence += 0.3
            elif item["type"] == "hadith":
                if item.get("verified"):
                    response_parts.append(f"The Prophet Muhammad ﷺ said:")
                    response_parts.append(f"\"{item['text']}\"")
                    response_parts.append(f"[{item.get('reference', '')} - {item.get('grade', '')}]")
                    confidence += 0.25
            elif item["type"] == "fiqh":
                response_parts.append(f"According to {item.get('madhab', 'scholars')}:")
                response_parts.append(item['text'])
                confidence += 0.2
        
        # Normalize confidence
        confidence = min(confidence, 0.95)
        
        return {
            "answer": "\n\n".join(response_parts),
            "confidence": confidence
        }
    
    def _get_no_context_response(self, query: str, language: str) -> str:
        """Advanced multi-source search for best answer"""
        
        # Step 1: Search Q&A database first
        qa_result = search_qa(query)
        if qa_result:
            return qa_result + "\n\n---\n*Source: Swaleh AI Islamic Q&A Database*"
        
        # Step 2: Search Quran verses
        quran_results = search_quran_verses(query)
        if quran_results:
            response = "📖 **From the Holy Quran:**\n\n"
            for verse in quran_results:
                response += f"**{verse['reference']}** - {verse['surah']}\n"
                response += f"_{verse['text']}_\n\n"
            return response + "---\n*Always refer to the Quran as the primary source*"
        
        # Step 3: Search Hadith
        hadith_results = search_hadith(query)
        if hadith_results:
            response = "📜 **From Authentic Hadith:**\n\n"
            for hadith in hadith_results[:3]:
                response += f"**{hadith['collection']}** - {hadith['topic']}\n"
                response += f"Narrated by {hadith['narrator']}:\n"
                response += f"_{hadith['text']}_\n"
                response += f"Grade: **{hadith['grade']}**\n\n"
            return response + "---\n*Authentic hadith from recognized collections*"
        
        # Step 4: Search Knowledge Base
        from app.services.islamic_knowledge_base import search_knowledge_base
        kb_result = search_knowledge_base(query)
        if kb_result:
            return kb_result + "\n\n---\n*Source: Swaleh AI Islamic Knowledge Base*"
        
        # Step 5: Comprehensive search
        search_results = advanced_search.comprehensive_search(query)
        if search_results["best_answer"]:
            return search_results["best_answer"] + f"\n\n---\n*Source: {search_results['source_type']}*"
        
        # Final fallback
        return (
            "I searched through the Quran, Hadith collections, and Islamic knowledge base "
            "but couldn't find a specific answer to your question.\n\n"
            "📚 **Try asking about:**\n"
            "• Five Pillars of Islam\n"
            "• Prayer (Salah) guidance\n"
            "• Fasting (Sawm) rules\n"
            "• Charity (Zakat) calculation\n"
            "• Hajj rituals\n"
            "• Quranic verses and their meanings\n"
            "• Hadith on various topics\n"
            "• Islamic beliefs (Aqeedah)\n\n"
            "والله أعلم (And Allah knows best)\n\n"
            "*For detailed matters, please consult a qualified Islamic scholar.*"
        )
    
    def _get_disclaimer(self, query_type: str, confidence: float) -> str:
        """Get appropriate disclaimer based on query type and confidence"""
        if confidence < 0.5:
            return (
                "⚠️ This response has low confidence. "
                "Please verify with a qualified Islamic scholar. "
                "Allah knows best (والله أعلم)."
            )
        elif query_type in ["fiqh", "aqeedah"]:
            return (
                "📚 This is based on authentic Islamic sources. "
                "For personal matters, please consult a qualified scholar. "
                "Differences of opinion among recognized madhabs are respected."
            )
        else:
            return (
                "✅ Based on authentic Islamic sources. "
                "Always refer to the Quran and Sunnah as primary sources."
            )
    
    def _get_suggestions(self, query: str, query_type: str) -> List[str]:
        """Get follow-up question suggestions"""
        suggestions = {
            "quran": [
                "Can you explain the tafsir of this verse?",
                "What is the context of revelation for this surah?",
                "Are there similar verses in other surahs?"
            ],
            "hadith": [
                "What is the authenticity grade of this hadith?",
                "Are there similar hadith in other collections?",
                "What do scholars say about this hadith?"
            ],
            "fiqh": [
                "What is the ruling according to other madhabs?",
                "What is the evidence for this ruling?",
                "Are there any exceptions to this ruling?"
            ],
            "aqeedah": [
                "What does the Quran say about this?",
                "What is the consensus of Ahl us-Sunnah?",
                "Are there any misconceptions about this?"
            ],
            "general": [
                "Can you provide more details?",
                "What are the authentic sources for this?",
                "Is there scholarly consensus on this?"
            ]
        }
        
        return suggestions.get(query_type, suggestions["general"])
