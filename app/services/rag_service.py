"""
Advanced RAG (Retrieval-Augmented Generation) Service
Combines vector search with Islamic knowledge for accurate answers
"""
from typing import Dict, Any, List, Optional
from app.services.vector_store import vector_store
from app.services.text_ingester import text_ingester
from app.services.islamic_corpus import search_qa, search_quran_verses, search_hadith
from app.services.islamic_knowledge_base import search_knowledge_base

class RAGService:
    """Advanced RAG service for Islamic Q&A"""
    
    def __init__(self):
        self.initialized = False
    
    def initialize(self):
        """Load all texts into vector store"""
        if not self.initialized:
            text_ingester.load_all_texts()
            self.initialized = True
    
    def answer_question(self, query: str, language: str = "en") -> Dict[str, Any]:
        """Answer an Islamic question using RAG"""
        self.initialize()
        
        # Step 1: Try Q&A database first (fastest, most accurate)
        qa_answer = search_qa(query)
        if qa_answer:
            return {
                'answer': qa_answer,
                'source': 'Q&A Database',
                'confidence': 0.9,
                'method': 'direct_match'
            }
        
        # Step 2: Vector search for relevant context
        vector_results = vector_store.search(query, top_k=5)
        
        # Step 3: Also search Quran and Hadith
        quran_results = search_quran_verses(query)
        hadith_results = search_hadith(query)
        
        # Step 4: Build comprehensive answer
        answer = self._build_answer(query, vector_results, quran_results, hadith_results)
        
        return answer
    
    def _build_answer(
        self, 
        query: str,
        vector_results: List[Dict],
        quran_results: List[Dict],
        hadith_results: List[Dict]
    ) -> Dict[str, Any]:
        """Build a comprehensive answer from multiple sources"""
        
        parts = []
        confidence = 0.0
        sources = []
        
        # Add Bismillah
        parts.append("بسم الله الرحمن الرحيم\n")
        
        # Add vector search results (general knowledge)
        if vector_results:
            best = vector_results[0]
            if best['relevance'] > 0.3:
                parts.append(best['content'])
                sources.append(best.get('source', 'Islamic Knowledge Base'))
                confidence = max(confidence, best['relevance'])
        
        # Add Quran verses if relevant
        if quran_results and confidence < 0.8:
            parts.append("\n📖 **From the Quran:**")
            for verse in quran_results[:2]:
                parts.append(f"• {verse['reference']}: {verse['text'][:200]}...")
                sources.append(verse['reference'])
        
        # Add Hadith if relevant
        if hadith_results and confidence < 0.7:
            parts.append("\n📜 **From Hadith:**")
            for hadith in hadith_results[:2]:
                parts.append(f"• {hadith.get('collection', 'Hadith')}: {hadith.get('text', '')[:200]}...")
                sources.append(hadith.get('collection', 'Hadith'))
        
        # Fallback response
        if not parts or confidence < 0.2:
            return {
                'answer': self._get_fallback(query),
                'source': 'General Knowledge',
                'confidence': 0.1,
                'method': 'fallback'
            }
        
        return {
            'answer': '\n\n'.join(parts),
            'source': ', '.join(sources[:3]) if sources else 'Multiple Sources',
            'confidence': min(confidence, 0.95),
            'method': 'rag'
        }
    
    def _get_fallback(self, query: str) -> str:
        """Get fallback response"""
        query_lower = query.lower()
        
        common_answers = {
            "pillar": "The Five Pillars of Islam are: Shahada, Salah, Zakat, Sawm, and Hajj.",
            "allah": "Allah is the One and Only God, Creator of everything. He has 99 beautiful names including Ar-Rahman (Most Gracious) and Ar-Raheem (Most Merciful).",
            "quran": "The Quran is the holy book of Islam, revealed to Prophet Muhammad ﷺ over 23 years. It has 114 surahs.",
            "muhammad": "Prophet Muhammad ﷺ is the final messenger of Allah, born in Makkah in 570 CE.",
            "pray": "Muslims pray 5 times daily: Fajr, Dhuhr, Asr, Maghrib, and Isha.",
            "ramadan": "Ramadan is the 9th month of the Islamic calendar. Muslims fast from dawn to sunset.",
            "hajj": "Hajj is the pilgrimage to Makkah, performed once in a lifetime if able.",
            "zakat": "Zakat is obligatory charity of 2.5% on savings above the Nisab threshold.",
        }
        
        for key, answer in common_answers.items():
            if key in query_lower:
                return answer + "\n\n📚 Please ask for more details if needed."
        
        return "I don't have enough information to answer this question accurately. Please try asking about: Five Pillars of Islam, Who is Allah, What is the Quran, or other Islamic topics."

# Global instance
rag_service = RAGService()
