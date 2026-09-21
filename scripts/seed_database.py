"""
Database seeding script with authentic Islamic content
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import db_manager, get_db
from app.models.quran import QuranMetadata, QuranVerse, QuranTranslation, QuranTafsir
from app.models.hadith import HadithCollection, Hadith, HadithChapter, HadithNarrator
from app.models.fiqh import Madhab, FiqhCategory, FiqhTopic, FiqhRuling, FiqhScholar
from datetime import datetime
import json

def seed_quran_metadata(db: Session):
    """Seed Quran surah metadata"""
    print("📚 Seeding Quran metadata...")
    
    surahs_data = [
        {
            "surah_id": 1, "surah_name_arabic": "الفاتحة",
            "surah_name_english": "Al-Fatiha",
            "surah_name_transliteration": "Al-Fatihah",
            "revelation_type": "Meccan",
            "total_verses": 7,
            "juz": 1,
            "meaning_english": "The Opening",
            "theme": "Praise, worship, and supplication to Allah"
        },
        {
            "surah_id": 2, "surah_name_arabic": "البقرة",
            "surah_name_english": "Al-Baqarah",
            "surah_name_transliteration": "Al-Baqarah",
            "revelation_type": "Medinan",
            "total_verses": 286,
            "juz": 1,
            "meaning_english": "The Cow",
            "theme": "Guidance for righteous, stories of creation, law"
        },
        {
            "surah_id": 112, "surah_name_arabic": "الإخلاص",
            "surah_name_english": "Al-Ikhlas",
            "surah_name_transliteration": "Al-Ikhlas",
            "revelation_type": "Meccan",
            "total_verses": 4,
            "juz": 30,
            "meaning_english": "The Sincerity",
            "theme": "Pure monotheism, oneness of Allah"
        },
        {
            "surah_id": 113, "surah_name_arabic": "الفلق",
            "surah_name_english": "Al-Falaq",
            "surah_name_transliteration": "Al-Falaq",
            "revelation_type": "Meccan",
            "total_verses": 5,
            "juz": 30,
            "meaning_english": "The Dawn",
            "theme": "Seeking protection from evil"
        },
        {
            "surah_id": 114, "surah_name_arabic": "الناس",
            "surah_name_english": "An-Nas",
            "surah_name_transliteration": "An-Nas",
            "revelation_type": "Meccan",
            "total_verses": 6,
            "juz": 30,
            "meaning_english": "The Mankind",
            "theme": "Seeking refuge in Allah from evil whispers"
        }
    ]
    
    for surah_data in surahs_data:
        existing = db.query(QuranMetadata).filter(
            QuranMetadata.surah_id == surah_data["surah_id"]
        ).first()
        
        if not existing:
            surah = QuranMetadata(**surah_data)
            db.add(surah)
            print(f"  ✅ Added Surah {surah_data['surah_id']}: {surah_data['surah_name_english']}")
    
    db.commit()
    print("✅ Quran metadata seeded successfully\n")

def seed_quran_verses(db: Session):
    """Seed some Quran verses"""
    print("📖 Seeding Quran verses...")
    
    verses_data = [
        {
            "surah_id": 1, "verse_number": 1,
            "arabic_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            "arabic_text_uthmani": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
            "verse_key": "1:1"
        },
        {
            "surah_id": 112, "verse_number": 1,
            "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
            "arabic_text_uthmani": "قُلْ هُوَ ٱللَّهُ أَحَدٌ",
            "verse_key": "112:1"
        },
        {
            "surah_id": 112, "verse_number": 2,
            "arabic_text": "اللَّهُ الصَّمَدُ",
            "arabic_text_uthmani": "ٱللَّهُ ٱلصَّمَدُ",
            "verse_key": "112:2"
        },
        {
            "surah_id": 112, "verse_number": 3,
            "arabic_text": "لَمْ يَلِدْ وَلَمْ يُولَدْ",
            "arabic_text_uthmani": "لَمْ يَلِدْ وَلَمْ يُولَدْ",
            "verse_key": "112:3"
        },
        {
            "surah_id": 112, "verse_number": 4,
            "arabic_text": "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
            "arabic_text_uthmani": "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌ",
            "verse_key": "112:4"
        }
    ]
    
    for verse_data in verses_data:
        existing = db.query(QuranVerse).filter(
            QuranVerse.verse_key == verse_data["verse_key"]
        ).first()
        
        if not existing:
            verse = QuranVerse(**verse_data)
            db.add(verse)
            print(f"  ✅ Added verse {verse_data['verse_key']}")
    
    db.commit()
    print("✅ Quran verses seeded successfully\n")

def seed_hadith_collections(db: Session):
    """Seed Hadith collections"""
    print("📜 Seeding Hadith collections...")
    
    collections_data = [
        {
            "collection_name": "Sahih Bukhari",
            "compiler_name": "Imam Bukhari",
            "compiler_full_name": "Abu Abdullah Muhammad ibn Ismail al-Bukhari",
            "birth_year": "194 AH",
            "death_year": "256 AH",
            "compilation_date": "846 CE",
            "total_hadith": 7563,
            "authenticity_grade": "Sahih",
            "description": "The most authentic book after the Quran",
            "methodology": "Strict authentication criteria for hadith acceptance"
        },
        {
            "collection_name": "Sahih Muslim",
            "compiler_name": "Imam Muslim",
            "compiler_full_name": "Abul Husayn Muslim ibn al-Hajjaj al-Naysaburi",
            "birth_year": "204 AH",
            "death_year": "261 AH",
            "compilation_date": "875 CE",
            "total_hadith": 4000,
            "authenticity_grade": "Sahih",
            "description": "Second most authentic hadith collection",
            "methodology": "Rigorous authentication methodology"
        },
        {
            "collection_name": "Sunan Abu Dawud",
            "compiler_name": "Imam Abu Dawud",
            "compiler_full_name": "Abu Dawud Sulayman ibn al-Ash'ath al-Sijistani",
            "birth_year": "202 AH",
            "death_year": "275 AH",
            "compilation_date": "889 CE",
            "total_hadith": 4800,
            "authenticity_grade": "Hasan",
            "description": "Focuses on legal hadith",
            "methodology": "Includes hadith related to legal rulings"
        },
        {
            "collection_name": "Jami at-Tirmidhi",
            "compiler_name": "Imam Tirmidhi",
            "compiler_full_name": "Abu Isa Muhammad ibn Isa at-Tirmidhi",
            "birth_year": "209 AH",
            "death_year": "279 AH",
            "compilation_date": "892 CE",
            "total_hadith": 3956,
            "authenticity_grade": "Hasan",
            "description": "Includes opinions of different madhabs",
            "methodology": "Comparative fiqh analysis"
        },
        {
            "collection_name": "Sunan an-Nasa'i",
            "compiler_name": "Imam Nasa'i",
            "compiler_full_name": "Abu Abdur Rahman Ahmad ibn Shu'ayb an-Nasa'i",
            "birth_year": "215 AH",
            "death_year": "303 AH",
            "compilation_date": "915 CE",
            "total_hadith": 5761,
            "authenticity_grade": "Sahih",
            "description": "Known for strict authentication",
            "methodology": "Very strict criteria for hadith acceptance"
        },
        {
            "collection_name": "Sunan Ibn Majah",
            "compiler_name": "Imam Ibn Majah",
            "compiler_full_name": "Abu Abdullah Muhammad ibn Yazid Ibn Majah",
            "birth_year": "209 AH",
            "death_year": "273 AH",
            "compilation_date": "887 CE",
            "total_hadith": 4341,
            "authenticity_grade": "Hasan",
            "description": "Sixth of the six authentic collections",
            "methodology": "Comprehensive collection of hadith"
        }
    ]
    
    for col_data in collections_data:
        existing = db.query(HadithCollection).filter(
            HadithCollection.collection_name == col_data["collection_name"]
        ).first()
        
        if not existing:
            collection = HadithCollection(**col_data)
            db.add(collection)
            print(f"  ✅ Added {col_data['collection_name']} by {col_data['compiler_name']}")
    
    db.commit()
    print("✅ Hadith collections seeded successfully\n")

def seed_madhabs(db: Session):
    """Seed Madhab information"""
    print("⚖️ Seeding Madhabs...")
    
    madhabs_data = [
        {
            "madhab_name": "Hanafi",
            "madhab_name_arabic": "حنفي",
            "founder_name": "Imam Abu Hanifa",
            "founder_bio": "Nu'man ibn Thabit (80-150 AH). Born in Kufa, Iraq. Known for extensive use of qiyas and istihsan.",
            "founded_year": "8th Century CE",
            "description": "The oldest and most widely followed madhab. Known for its systematic methodology.",
            "methodology": "Quran, Sunnah, Ijma, Qiyas, Istihsan, Urf",
            "major_books": '["Al-Hidayah", "Radd al-Muhtar", "Al-Mabsut"]',
            "regions": '["Turkey", "Central Asia", "Indian Subcontinent", "Balkans"]'
        },
        {
            "madhab_name": "Maliki",
            "madhab_name_arabic": "مالكي",
            "founder_name": "Imam Malik ibn Anas",
            "founder_bio": "Malik ibn Anas (93-179 AH). Born in Medina. Author of Al-Muwatta.",
            "founded_year": "8th Century CE",
            "description": "Based on the practice of the people of Medina.",
            "methodology": "Quran, Sunnah, Amal Ahl al-Madinah, Ijma, Qiyas, Masalih Mursalah",
            "major_books": '["Al-Muwatta", "Al-Mudawwanah", "Al-Risalah"]',
            "regions": '["North Africa", "West Africa", "Sudan", "Upper Egypt"]'
        },
        {
            "madhab_name": "Shafi'i",
            "madhab_name_arabic": "شافعي",
            "founder_name": "Imam Al-Shafi'i",
            "founder_bio": "Muhammad ibn Idris al-Shafi'i (150-204 AH). Born in Gaza. Founded Usul al-Fiqh.",
            "founded_year": "9th Century CE",
            "description": "Known for systematic legal theory (Usul al-Fiqh).",
            "methodology": "Quran, Sunnah, Ijma, Qiyas",
            "major_books": '["Al-Risalah", "Al-Umm", "Minhaj al-Talibin"]',
            "regions": '["Egypt", "East Africa", "Southeast Asia", "Yemen"]'
        },
        {
            "madhab_name": "Hanbali",
            "madhab_name_arabic": "حنبلي",
            "founder_name": "Imam Ahmad ibn Hanbal",
            "founder_bio": "Ahmad ibn Hanbal (164-241 AH). Born in Baghdad. Known for hadith scholarship.",
            "founded_year": "9th Century CE",
            "description": "Most conservative madhab, relies heavily on hadith.",
            "methodology": "Quran, Sunnah, Fatwa of Sahabah, Weak Hadith over Qiyas",
            "major_books": '["Al-Musnad", "Al-Mughni", "Al-Insaf"]',
            "regions": '["Saudi Arabia", "Qatar", "UAE", "Parts of Syria"]'
        }
    ]
    
    for madhab_data in madhabs_data:
        existing = db.query(Madhab).filter(
            Madhab.madhab_name == madhab_data["madhab_name"]
        ).first()
        
        if not existing:
            madhab = Madhab(**madhab_data)
            db.add(madhab)
            print(f"  ✅ Added {madhab_data['madhab_name']} Madhab - Founded by {madhab_data['founder_name']}")
    
    db.commit()
    print("✅ Madhabs seeded successfully\n")

def seed_fiqh_categories(db: Session):
    """Seed Fiqh categories"""
    print("📋 Seeding Fiqh categories...")
    
    categories_data = [
        {
            "category_name": "Ibadah",
            "category_name_arabic": "عبادات",
            "description": "Acts of worship and devotion to Allah",
            "order_number": 1
        },
        {
            "category_name": "Mu'amalat",
            "category_name_arabic": "معاملات",
            "description": "Social and economic transactions",
            "order_number": 2
        },
        {
            "category_name": "Munakahat",
            "category_name_arabic": "مناكحات",
            "description": "Marriage and family law",
            "order_number": 3
        },
        {
            "category_name": "Jinayat",
            "category_name_arabic": "جنايات",
            "description": "Criminal law and punishments",
            "order_number": 4
        },
        {
            "category_name": "Akhlaq",
            "category_name_arabic": "أخلاق",
            "description": "Ethics, manners, and character",
            "order_number": 5
        }
    ]
    
    for cat_data in categories_data:
        existing = db.query(FiqhCategory).filter(
            FiqhCategory.category_name == cat_data["category_name"]
        ).first()
        
        if not existing:
            category = FiqhCategory(**cat_data)
            db.add(category)
            print(f"  ✅ Added category: {cat_data['category_name']} ({cat_data['category_name_arabic']})")
    
    db.commit()
    print("✅ Fiqh categories seeded successfully\n")

def main():
    """Main seeding function"""
    print("\n" + "=" * 60)
    print("🌱 SWALEH AI - DATABASE SEEDING")
    print("=" * 60)
    print("Seeding authentic Islamic content...\n")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Seed data in order
        seed_quran_metadata(db)
        seed_quran_verses(db)
        seed_hadith_collections(db)
        seed_madhabs(db)
        seed_fiqh_categories(db)
        
        print("=" * 60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("📚 The database now contains:")
        print("   - Quran Surahs and Verses")
        print("   - Authentic Hadith Collections")
        print("   - Four Madhabs Information")
        print("   - Fiqh Categories")
        print("\n🤲 May Allah accept this effort. Ameen.")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
