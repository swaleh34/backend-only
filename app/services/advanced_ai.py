"""
ADVANCED ISLAMIC AI ENGINE
- Analyzes question intent
- Searches Quran, Hadith, Tafsir simultaneously
- Synthesizes comprehensive answers with citations
"""
import re
import httpx
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class SearchResult:
    """Structured search result"""
    type: str  # quran, hadith, tafsir, knowledge
    content: str
    reference: str
    relevance: float
    source: str

class AdvancedIslamicAI:
    """Multi-source Islamic AI with deep analysis"""
    
    def __init__(self):
        self.client = httpx.Client(timeout=15.0)
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # API endpoints
        self.quran_api = "https://api.alquran.cloud/v1"
        self.quran_com = "https://api.quran.com/api/v4"
        
        # Question analysis patterns
        self.patterns = {
            "verse_lookup": r'(?:quran|surah|chapter|verse|ayah)?\s*(\d+)[:\s]+(\d+)',
            "hadith_lookup": r'(?:hadith|hadeeth)\s*(?:number|#)?\s*(\d+)',
            "comparison": r'(?:difference|compare|similarities|vs|versus|between)',
            "how_to": r'(?:how\s+(?:to|do|can|should|does)|steps|method|procedure|way\s+to)',
            "definition": r'(?:what\s+(?:is|are)|define|meaning\s+of|definition\s+of|explain)',
            "ruling": r'(?:is\s+it|ruling|halal|haram|permissible|allowed|forbidden|makruh|wajib|fard)',
            "who": r'(?:who\s+(?:is|are|was|were))',
            "when": r'(?:when\s+(?:is|was|did|will|should))',
            "where": r'(?:where\s+(?:is|are|was|were|can|should))',
            "why": r'(?:why\s+(?:do|does|is|are|should|must))',
        }
    
    def analyze_question(self, query: str) -> Dict[str, Any]:
        """Deep analysis of the question"""
        query_lower = query.lower()
        
        analysis = {
            "original_query": query,
            "query_lower": query_lower,
            "intent": self._detect_intent(query_lower),
            "topics": self._extract_topics(query_lower),
            "keywords": self._extract_keywords(query_lower),
            "verse_reference": None,
            "is_explanatory": False,
            "needs_evidence": False,
            "search_queries": []
        }
        
        # Check for verse reference
        verse_match = re.search(self.patterns["verse_lookup"], query_lower)
        if verse_match:
            analysis["verse_reference"] = {
                "surah": int(verse_match.group(1)),
                "ayah": int(verse_match.group(2))
            }
        
        # Determine if explanatory
        explanatory_patterns = [
            "what is", "what are", "who is", "explain", "describe",
            "how to", "how does", "why do", "meaning of", "concept of",
            "categories of", "types of", "characteristics", "made from",
            "role of", "purpose of", "best times", "best way",
            "similarities", "difference between", "conditions for",
            "major signs", "minor signs", "pillars of"
        ]
        analysis["is_explanatory"] = any(p in query_lower for p in explanatory_patterns)
        analysis["needs_evidence"] = any(w in query_lower for w in [
            "evidence", "proof", "verse", "hadith", "quran", "sunnah", "source", "citation"
        ])
        
        # Generate search queries
        analysis["search_queries"] = self._generate_search_queries(query_lower, analysis)
        
        return analysis
    
    def _detect_intent(self, query: str) -> str:
        """Detect the intent of the question"""
        if re.search(self.patterns["verse_lookup"], query):
            return "verse_lookup"
        if re.search(self.patterns["hadith_lookup"], query):
            return "hadith_lookup"
        if re.search(self.patterns["comparison"], query):
            return "comparison"
        if re.search(self.patterns["how_to"], query):
            return "how_to"
        if re.search(self.patterns["ruling"], query):
            return "fiqh_ruling"
        if re.search(self.patterns["definition"], query):
            return "definition"
        if re.search(self.patterns["who"], query):
            return "person_lookup"
        return "general_knowledge"
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract Islamic topics from query"""
        topics_db = [
            "allah", "tawheed", "shirk", "iman", "faith",
            "prophet", "muhammad", "rasul", "nabi", "messenger",
            "quran", "surah", "ayah", "verse", "revelation",
            "hadith", "sunnah", "bukhari", "muslim", "narrated",
            "salah", "prayer", "salat", "namaz", "wudu", "ablution",
            "zakat", "charity", "sadaqah", "zakah",
            "sawm", "fasting", "ramadan", "siyam",
            "hajj", "pilgrimage", "umrah", "kaaba", "makkah",
            "jannah", "paradise", "heaven", "akhirah", "hereafter",
            "jahannam", "hell", "fire", "punishment",
            "angel", "malaika", "jibreel", "gabriel", "mikail",
            "jinn", "shaytan", "satan", "iblis", "devil",
            "prophet", "isa", "jesus", "musa", "moses", "ibrahim", "abraham",
            "marriage", "nikah", "divorce", "talaq", "family",
            "halal", "haram", "permissible", "forbidden",
            "death", "grave", "barzakh", "resurrection", "judgment",
            "dua", "supplication", "dhikr", "remembrance",
            "hijab", "modesty", "women", "rights",
            "jihad", "struggle", "peace",
            "sharia", "fiqh", "law", "ruling", "fatwa",
            "sahabah", "companions", "caliph", "abu bakr", "umar", "uthman", "ali",
            "seerah", "history", "battle", "badr", "uhud",
            "qadr", "decree", "destiny", "free will", "predestination",
            "tawbah", "repentance", "forgiveness", "sin",
            "sabr", "patience", "shukr", "gratitude",
        ]
        
        found_topics = []
        for topic in topics_db:
            if topic in query:
                found_topics.append(topic)
        
        return found_topics[:5]
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract meaningful keywords"""
        # Remove common words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                      "have", "has", "had", "do", "does", "did", "will", "would",
                      "can", "could", "should", "may", "might", "shall", "must",
                      "i", "me", "my", "we", "our", "you", "your", "he", "she",
                      "it", "they", "them", "this", "that", "these", "those",
                      "what", "which", "who", "whom", "when", "where", "why", "how",
                      "in", "on", "at", "to", "for", "of", "from", "with", "by",
                      "about", "into", "through", "during", "before", "after",
                      "and", "but", "or", "nor", "not", "so", "yet", "both",
                      "either", "neither", "each", "every", "all", "any", "few",
                      "more", "most", "other", "some", "such", "only", "own",
                      "same", "than", "too", "very", "just"}
        
        words = re.findall(r'\b[a-z]+\b', query)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return list(set(keywords))[:10]
    
    def _generate_search_queries(self, query: str, analysis: Dict) -> List[str]:
        """Generate optimized search queries"""
        queries = [query]
        
        # Add topic-based queries
        for topic in analysis.get("topics", []):
            queries.append(topic)
        
        # Add keyword combinations
        keywords = analysis.get("keywords", [])
        if len(keywords) >= 2:
            queries.append(" ".join(keywords[:3]))
        
        return queries[:3]
    
    def comprehensive_search(self, query: str) -> Dict[str, Any]:
        """Perform comprehensive multi-source search"""
        
        # Step 1: Analyze the question
        analysis = self.analyze_question(query)
        
        # Step 2: Search ALL sources in parallel
        results = self._parallel_search(analysis)
        
        # Step 3: Synthesize answer
        answer = self._synthesize_answer(query, analysis, results)
        
        return answer
    
    def _parallel_search(self, analysis: Dict) -> Dict[str, List[SearchResult]]:
        """Search all sources simultaneously"""
        results = {
            "quran_verses": [],
            "hadith": [],
            "tafsir": [],
            "knowledge": []
        }
        
        queries = analysis.get("search_queries", [analysis["original_query"]])
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            
            # Submit Quran search
            for q in queries[:2]:
                futures[executor.submit(self._search_quran, q)] = "quran"
            
            # Submit Hadith search
            for q in queries[:2]:
                futures[executor.submit(self._search_hadith, q)] = "hadith"
            
            # Submit Knowledge base search
            futures[executor.submit(self._search_knowledge, queries[0])] = "knowledge"
            
            # Process results as they complete
            for future in as_completed(futures):
                source_type = futures[future]
                try:
                    result = future.result()
                    if result:
                        if source_type == "quran":
                            results["quran_verses"].extend(result)
                        elif source_type == "hadith":
                            results["hadith"].extend(result)
                        elif source_type == "knowledge":
                            results["knowledge"].extend(result)
                except Exception as e:
                    print(f"Search error for {source_type}: {e}")
        
        # Sort by relevance
        for key in results:
            results[key].sort(key=lambda x: x.relevance, reverse=True)
        
        return results
    
    def _search_quran(self, query: str) -> List[SearchResult]:
        """Search Quran - use API for verse lookups, local for keyword search"""
        results = []
        
        # Check if this is a specific verse reference (e.g., "2:255", "Quran 1:1")
        import re
        verse_match = re.search(r'(\d+)[:\s]+(\d+)', query)
        
        if verse_match:
            # Direct verse lookup via API (WORKS RELIABLY)
            surah = int(verse_match.group(1))
            ayah = int(verse_match.group(2))
            
            try:
                resp = self.client.get(f"{self.quran_api}/ayah/{surah}:{ayah}/en.sahih")
                data = resp.json()
                if data.get("code") == 200:
                    d = data["data"]
                    results.append(SearchResult(
                        type="quran",
                        content=d.get("text", ""),
                        reference=f"Quran {surah}:{ayah} - {d.get('surah', {}).get('englishName', '')}",
                        relevance=1.0,
                        source="Quran Cloud API"
                    ))
                    return results
            except Exception as e:
                print(f"Verse lookup error: {e}")
        
        # For keyword searches, use local Quran data
        try:
            from app.services.islamic_corpus import QURAN_FULL_TEXT
            
            query_words = [w.lower() for w in query.split() if len(w) > 3]
            
            for surah_id, surah_data in QURAN_FULL_TEXT.items():
                for verse_num, verse_text in surah_data.get("verses", {}).items():
                    verse_lower = verse_text.lower()
                    matches = sum(1 for w in query_words if w in verse_lower)
                    if matches >= 2:
                        results.append(SearchResult(
                            type="quran",
                            content=verse_text[:400],
                            reference=f"Quran {surah_id}:{verse_num} - {surah_data.get('name', '')}",
                            relevance=min(0.9, matches * 0.2),
                            source="Quran (Local Database)"
                        ))
        except Exception as e:
            print(f"Local Quran search error: {e}")
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance, reverse=True)
        return results[:5]
    
    def _search_hadith(self, query: str) -> List[SearchResult]:
        """Search Hadith - only return truly relevant ones"""
        results = []
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        
        if not query_words:
            return []
        
        try:
            from app.services.islamic_corpus import AUTHENTIC_HADITH
            
            for collection, hadiths in AUTHENTIC_HADITH.items():
                for hadith in hadiths:
                    text = hadith.get("text", "").lower()
                    topic = hadith.get("topic", "").lower()
                    
                    # Count matching words
                    text_matches = sum(1 for w in query_words if w in text)
                    topic_matches = sum(1 for w in query_words if w in topic)
                    
                    # Only include if at least 2 keyword matches OR topic matches
                    if text_matches >= 2 or topic_matches >= 2:
                        results.append(SearchResult(
                            type="hadith",
                            content=hadith.get("text", "")[:400],
                            reference=f"{hadith.get('collection', collection)} - {hadith.get('topic', '')}",
                            relevance=min(0.9, (text_matches + topic_matches) * 0.15),
                            source=hadith.get('collection', collection)
                        ))
        except Exception as e:
            print(f"Hadith search error: {e}")
        
        # Sort by relevance and return top 3
        results.sort(key=lambda x: x.relevance, reverse=True)
        return results[:3]
    
    def _search_knowledge(self, query: str) -> List[SearchResult]:
        """Search Islamic knowledge base - try specific knowledge first"""
        results = []
        
        try:
            from app.services.answer_engine import answer_engine
            answer_engine.initialize()
            
            # FIRST: Try specific knowledge base (most accurate)
            specific = answer_engine._try_specific_knowledge(query.lower())
            if specific:
                results.append(SearchResult(
                    type="knowledge",
                    content=specific['answer'][:800],
                    reference=specific.get('source', 'Islamic Knowledge Base'),
                    relevance=specific.get('confidence', 0.9),
                    source="Islamic Knowledge Base"
                ))
            
            # SECOND: Try vector search for additional context
            from app.services.vector_store import vector_store
            vector_results = vector_store.search(query, top_k=2)
            
            for vr in vector_results:
                if vr.get('relevance', 0) > 0.25:
                    # Don't duplicate if similar to specific knowledge
                    results.append(SearchResult(
                        type="knowledge",
                        content=vr.get('content', '')[:500],
                        reference=vr.get('source', 'Islamic Knowledge'),
                        relevance=vr.get('relevance', 0.5) * 0.7,  # Lower priority
                        source=vr.get('source', 'Knowledge Base')
                    ))
                    
        except Exception as e:
            print(f"Knowledge search error: {e}")
        
        # Remove duplicates
        seen_content = set()
        unique_results = []
        for r in results:
            key = r.content[:100]
            if key not in seen_content:
                seen_content.add(key)
                unique_results.append(r)
        
        return unique_results[:3]
    
    def _synthesize_answer(
        self, 
        query: str, 
        analysis: Dict, 
        results: Dict[str, List[SearchResult]]
    ) -> Dict[str, Any]:
        """Synthesize a comprehensive answer from all sources"""
        
        answer_parts = []
        sources = []
        
        # HEADER
        answer_parts.append(f"## {query}\n")
        
        # PRIMARY EXPLANATION (Knowledge base first for explanatory questions)
        if results["knowledge"]:
            best = results["knowledge"][0]
            if best.relevance > 0.5:
                answer_parts.append("### 📚 Answer\n")
                answer_parts.append(best.content)
                answer_parts.append("")
                sources.append(best.reference)
        
        # QURAN EVIDENCE
        if results["quran_verses"]:
            answer_parts.append("### 📖 Quranic Evidence\n")
            shown = 0
            for verse in results["quran_verses"]:
                if shown >= 3:
                    break
                # Skip if verse content is already in the knowledge answer
                if results["knowledge"] and verse.content[:50] in results["knowledge"][0].content:
                    continue
                answer_parts.append(f"**{verse.reference}**")
                answer_parts.append(f"> {verse.content[:350]}\n")
                sources.append(verse.reference)
                shown += 1
        
        # HADITH EVIDENCE  
        if results["hadith"]:
            answer_parts.append("### 📜 Hadith Evidence\n")
            shown = 0
            for hadith in results["hadith"]:
                if shown >= 2:
                    break
                answer_parts.append(f"**{hadith.reference}**")
                answer_parts.append(f"> {hadith.content[:350]}\n")
                sources.append(hadith.reference)
                shown += 1
        
        # NO RESULTS FALLBACK
        if not answer_parts or len(answer_parts) <= 2:
            answer_parts.append(
                "I could not find specific information on this topic in my knowledge base. "
                "Please try rephrasing your question, or consult a qualified Islamic scholar.\n\n"
                "**Suggested resources:**\n"
                "- Quran: quran.com\n"
                "- Hadith: sunnah.com\n"
                "- Ask a local imam or scholar\n\n"
                "والله أعلم (And Allah knows best)"
            )
        
        # FOOTER
        unique_sources = list(dict.fromkeys(sources))[:5]  # Remove duplicates, keep order
        answer_parts.append("\n---")
        if unique_sources:
            answer_parts.append(f"📚 **Sources:** {', '.join(unique_sources)}")
        answer_parts.append("⚠️ *Verify with qualified scholars for important matters. والله أعلم*")
        
        return {
            "answer": "\n\n".join(answer_parts),
            "sources": unique_sources,
            "analysis": {
                "intent": analysis.get("intent", "general"),
                "topics": analysis.get("topics", []),
                "quran_count": len(results["quran_verses"]),
                "hadith_count": len(results["hadith"]),
                "knowledge_count": len(results["knowledge"])
            },
            "confidence": 0.85 if (results["knowledge"] or results["quran_verses"]) else 0.4
        }

# Global instance
advanced_ai = AdvancedIslamicAI()