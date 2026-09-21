"""
Comprehensive Islamic Knowledge Base for Swaleh AI
"""
from typing import List, Dict, Any, Optional

ISLAMIC_KNOWLEDGE = {
    "basics": {
        "five_pillars": {
            "title": "The Five Pillars of Islam",
            "content": """
The Five Pillars of Islam (Arkan al-Islam):

1. **SHAHADA (Faith)** - "There is no god but Allah, and Muhammad is His Messenger"
2. **SALAH (Prayer)** - Five daily prayers: Fajr, Dhuhr, Asr, Maghrib, Isha
3. **ZAKAT (Charity)** - 2.5% of savings given to the poor annually
4. **SAWM (Fasting)** - Fasting during Ramadan from dawn to sunset
5. **HAJJ (Pilgrimage)** - Pilgrimage to Makkah once in a lifetime if able

📚 Source: Sahih al-Bukhari 8, Sahih Muslim 16
"""
        },
        "six_articles": {
            "title": "Six Articles of Faith",
            "content": """
The Six Articles of Faith (Arkan al-Iman):

1. Belief in Allah (Tawheed)
2. Belief in His Angels
3. Belief in His Books (Quran, Torah, Gospel, Psalms, Scrolls)
4. Belief in His Messengers (from Adam to Muhammad ﷺ)
5. Belief in the Day of Judgment
6. Belief in Divine Decree (Qadr)

📚 Source: Hadith of Jibreel, Sahih Muslim 8
"""
        }
    }
}

def search_knowledge_base(query: str) -> Optional[str]:
    """Search the knowledge base for relevant information"""
    query_lower = query.lower()
    
    for category, topics in ISLAMIC_KNOWLEDGE.items():
        for key, data in topics.items():
            if any(word in query_lower for word in data.get("title", "").lower().split()):
                return data["content"]
    
    return None