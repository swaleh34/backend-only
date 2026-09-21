"""
Quick seed script for Swaleh AI
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import db_manager, get_db
from app.models.quran import QuranMetadata, QuranVerse, QuranTranslation
from app.models.hadith import HadithCollection, Hadith
from app.models.fiqh import Madhab, FiqhCategory

def seed_all():
    db = next(get_db())
    
    try:
        print("🌱 Seeding Islamic knowledge base...\n")
        
        # Seed Quran Surahs
        surahs = [
            (1, "الفاتحة", "Al-Fatiha", "The Opening", "Meccan", 7),
            (2, "البقرة", "Al-Baqarah", "The Cow", "Medinan", 286),
            (3, "آل عمران", "Aal-E-Imran", "Family of Imran", "Medinan", 200),
            (36, "يس", "Ya-Sin", "Ya-Sin", "Meccan", 83),
            (67, "الملك", "Al-Mulk", "The Dominion", "Meccan", 30),
            (112, "الإخلاص", "Al-Ikhlas", "The Sincerity", "Meccan", 4),
            (113, "الفلق", "Al-Falaq", "The Dawn", "Meccan", 5),
            (114, "الناس", "An-Nas", "The Mankind", "Meccan", 6),
        ]
        
        for s in surahs:
            existing = db.query(QuranMetadata).filter(QuranMetadata.surah_id == s[0]).first()
            if not existing:
                surah = QuranMetadata(
                    surah_id=s[0],
                    surah_name_arabic=s[1],
                    surah_name_english=s[2],
                    surah_name_transliteration=s[2],
                    meaning_english=s[3],
                    revelation_type=s[4],
                    total_verses=s[5]
                )
                db.add(surah)
                print(f"  ✅ Added Surah {s[0]}: {s[2]}")
        
        # Seed Hadith Collections
        collections = [
            ("Sahih Bukhari", "Imam Bukhari", "846 CE", 7563, "Sahih", "The most authentic book after the Quran"),
            ("Sahih Muslim", "Imam Muslim", "875 CE", 4000, "Sahih", "Second most authentic collection"),
            ("Sunan Abu Dawud", "Imam Abu Dawud", "889 CE", 4800, "Hasan", "Focuses on legal hadith"),
        ]
        
        for c in collections:
            existing = db.query(HadithCollection).filter(HadithCollection.collection_name == c[0]).first()
            if not existing:
                col = HadithCollection(
                    collection_name=c[0],
                    compiler_name=c[1],
                    compilation_date=c[2],
                    total_hadith=c[3],
                    authenticity_grade=c[4],
                    description=c[5]
                )
                db.add(col)
                print(f"  ✅ Added {c[0]}")
        
        # Seed Madhabs
        madhabs = [
            ("Hanafi", "حنفي", "Imam Abu Hanifa", "8th Century"),
            ("Maliki", "مالكي", "Imam Malik", "8th Century"),
            ("Shafi'i", "شافعي", "Imam Al-Shafi'i", "9th Century"),
            ("Hanbali", "حنبلي", "Imam Ahmad ibn Hanbal", "9th Century"),
        ]
        
        for m in madhabs:
            existing = db.query(Madhab).filter(Madhab.madhab_name == m[0]).first()
            if not existing:
                madhab = Madhab(
                    madhab_name=m[0],
                    madhab_name_arabic=m[1],
                    founder_name=m[2],
                    founded_year=m[3]
                )
                db.add(madhab)
                print(f"  ✅ Added {m[0]} Madhab")
        
        db.commit()
        print("\n✅ Database seeded successfully!")
        print("🤲 Now try asking questions in the chat again!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()