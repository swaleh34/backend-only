from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, 
    Boolean, DateTime, Index
)
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModel

class HadithCollection(BaseModel, Base):
    __tablename__ = "hadith_collections"
    
    collection_name = Column(String(200), unique=True, nullable=False)
    compiler_name = Column(String(200))
    compiler_full_name = Column(String(300))
    compiler_bio = Column(Text)
    birth_year = Column(String(10))
    death_year = Column(String(10))
    compilation_date = Column(String(50))
    total_hadith = Column(Integer)
    authenticity_grade = Column(String(50))
    description = Column(Text)
    methodology = Column(Text)
    
    hadiths = relationship("Hadith", back_populates="collection", cascade="all, delete-orphan")
    chapters = relationship("HadithChapter", back_populates="collection", cascade="all, delete-orphan")

class HadithChapter(BaseModel, Base):
    __tablename__ = "hadith_chapters"
    
    collection_id = Column(Integer, ForeignKey("hadith_collections.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    chapter_name_arabic = Column(String(300))
    chapter_name_english = Column(String(300))
    book_number = Column(Integer)
    book_name_arabic = Column(String(300))
    book_name_english = Column(String(300))
    
    collection = relationship("HadithCollection", back_populates="chapters")
    hadiths = relationship("Hadith", back_populates="chapter")

class Hadith(BaseModel, Base):
    __tablename__ = "hadith"
    
    collection_id = Column(Integer, ForeignKey("hadith_collections.id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("hadith_chapters.id"))
    hadith_number = Column(String(50), nullable=False)
    international_number = Column(Integer)
    book_number = Column(Integer)
    chapter_number = Column(Integer)
    isnad_arabic = Column(Text)
    isnad_english = Column(Text)
    narrator_chain = Column(Text)
    matn_arabic = Column(Text, nullable=False)
    matn_english = Column(Text, nullable=False)
    matn_urdu = Column(Text)
    grade = Column(String(50))
    graded_by = Column(String(200))
    grading_reason = Column(Text)
    keywords = Column(Text)
    topics = Column(Text)
    rulings = Column(Text)
    benefits = Column(Text)
    is_authentic_hadith = Column(Boolean, default=True)
    verified_by = Column(String(200))
    verification_date = Column(DateTime)
    similar_hadith = Column(Text)
    quran_reference = Column(Text)
    
    collection = relationship("HadithCollection", back_populates="hadiths")
    chapter = relationship("HadithChapter", back_populates="hadiths")
    narrators = relationship("HadithNarrator", back_populates="hadith", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_hadith_collection_number', 'collection_id', 'hadith_number'),
        Index('ix_hadith_grade', 'grade'),
    )

class HadithNarrator(BaseModel, Base):
    __tablename__ = "hadith_narrators"
    
    hadith_id = Column(Integer, ForeignKey("hadith.id"), nullable=False)
    narrator_name = Column(String(200), nullable=False)
    narrator_full_name = Column(String(300))
    order_in_chain = Column(Integer)
    reliability = Column(String(50))
    biography = Column(Text)
    birth_year = Column(String(10))
    death_year = Column(String(10))
    
    hadith = relationship("Hadith", back_populates="narrators")

class HadithGrade(BaseModel, Base):
    __tablename__ = "hadith_grades"
    
    grade_name = Column(String(50), unique=True, nullable=False)
    grade_name_arabic = Column(String(50))
    description = Column(Text)
    criteria = Column(Text)
    authenticity_level = Column(Integer)
