from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, 
    Float, Boolean, DateTime, Enum, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, BaseModel
import enum

class RevelationType(str, enum.Enum):
    MECCAN = "Meccan"
    MEDINAN = "Medinan"

class QuranMetadata(BaseModel, Base):
    __tablename__ = "quran_metadata"
    
    surah_id = Column(Integer, unique=True, nullable=False, index=True)
    surah_name_arabic = Column(String(200), nullable=False)
    surah_name_english = Column(String(200), nullable=False)
    surah_name_transliteration = Column(String(200))
    revelation_type = Column(String(20), nullable=False)
    total_verses = Column(Integer, nullable=False)
    juz = Column(Integer)
    hizb = Column(Integer)
    page_number = Column(Integer)
    sajdah_type = Column(String(50))
    meaning_english = Column(Text)
    meaning_urdu = Column(Text)
    theme = Column(Text)
    period = Column(String(100))
    
    verses = relationship("QuranVerse", back_populates="surah", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Surah {self.surah_id}: {self.surah_name_english}>"

class QuranVerse(BaseModel, Base):
    __tablename__ = "quran_verses"
    
    surah_id = Column(Integer, ForeignKey("quran_metadata.surah_id"), nullable=False)
    verse_number = Column(Integer, nullable=False)
    arabic_text = Column(Text, nullable=False)
    arabic_text_uthmani = Column(Text, nullable=False)
    arabic_text_simple = Column(Text)
    page_number = Column(Integer)
    juz_number = Column(Integer)
    hizb_number = Column(Integer)
    rub_number = Column(Integer)
    sajdah = Column(Boolean, default=False)
    verse_key = Column(String(20), unique=True)
    audio_url = Column(String(500))
    audio_duration = Column(Float)
    
    surah = relationship("QuranMetadata", back_populates="verses")
    translations = relationship("QuranTranslation", back_populates="verse", cascade="all, delete-orphan")
    tafsirs = relationship("QuranTafsir", back_populates="verse", cascade="all, delete-orphan")
    words = relationship("QuranWord", back_populates="verse", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_verse_location', 'surah_id', 'verse_number', unique=True),
    )

class QuranTranslation(BaseModel, Base):
    __tablename__ = "quran_translations"
    
    verse_id = Column(Integer, ForeignKey("quran_verses.id"), nullable=False)
    translator_name = Column(String(200), nullable=False)
    translator_description = Column(Text)
    language = Column(String(10), nullable=False)
    translation_text = Column(Text, nullable=False)
    is_authentic_translation = Column(Boolean, default=True)
    approved_by = Column(String(200))
    footnotes = Column(Text)
    
    verse = relationship("QuranVerse", back_populates="translations")
    
    __table_args__ = (
        Index('ix_translation', 'verse_id', 'language', 'translator_name'),
    )

class QuranTafsir(BaseModel, Base):
    __tablename__ = "quran_tafsir"
    
    verse_id = Column(Integer, ForeignKey("quran_verses.id"), nullable=False)
    tafsir_name = Column(String(200), nullable=False)
    scholar_name = Column(String(200))
    scholar_bio = Column(Text)
    language = Column(String(10), default="ar")
    tafsir_text = Column(Text, nullable=False)
    tafsir_text_english = Column(Text)
    methodology = Column(String(100))
    is_authentic_tafsir = Column(Boolean, default=True)
    grade = Column(String(50))
    
    verse = relationship("QuranVerse", back_populates="tafsirs")
    
    __table_args__ = (
        Index('ix_tafsir', 'verse_id', 'tafsir_name'),
    )

class QuranWord(BaseModel, Base):
    __tablename__ = "quran_words"
    
    verse_id = Column(Integer, ForeignKey("quran_verses.id"), nullable=False)
    word_number = Column(Integer, nullable=False)
    arabic_word = Column(String(200), nullable=False)
    transliteration = Column(String(200))
    english_translation = Column(String(200))
    root_word = Column(String(100))
    grammar_type = Column(String(50))
    morphology = Column(Text)
    
    verse = relationship("QuranVerse", back_populates="words")

class QuranRoot(BaseModel, Base):
    __tablename__ = "quran_roots"
    
    root_word = Column(String(100), unique=True, nullable=False)
    arabic_root = Column(String(100))
    meaning = Column(Text)
    occurrences = Column(Integer, default=0)
    related_words = Column(Text)
