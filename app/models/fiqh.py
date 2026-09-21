from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, 
    Boolean, DateTime, Index
)
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModel

class Madhab(BaseModel, Base):
    __tablename__ = "madhabs"
    
    madhab_name = Column(String(100), unique=True, nullable=False)
    madhab_name_arabic = Column(String(100))
    founder_name = Column(String(200))
    founder_bio = Column(Text)
    founded_year = Column(String(10))
    description = Column(Text)
    methodology = Column(Text)
    major_books = Column(Text)
    regions = Column(Text)
    
    rulings = relationship("FiqhRuling", back_populates="madhab")
    scholars = relationship("FiqhScholar", back_populates="madhab")

class FiqhCategory(BaseModel, Base):
    __tablename__ = "fiqh_categories"
    
    category_name = Column(String(100), unique=True, nullable=False)
    category_name_arabic = Column(String(100))
    description = Column(Text)
    parent_category_id = Column(Integer, ForeignKey("fiqh_categories.id"))
    order_number = Column(Integer)
    
    topics = relationship("FiqhTopic", back_populates="category")

class FiqhTopic(BaseModel, Base):
    __tablename__ = "fiqh_topics"
    
    topic_name = Column(String(200), nullable=False)
    topic_name_arabic = Column(String(200))
    category_id = Column(Integer, ForeignKey("fiqh_categories.id"))
    description = Column(Text)
    keywords = Column(Text)
    
    category = relationship("FiqhCategory", back_populates="topics")
    rulings = relationship("FiqhRuling", back_populates="topic")

class FiqhRuling(BaseModel, Base):
    __tablename__ = "fiqh_rulings"
    
    topic_id = Column(Integer, ForeignKey("fiqh_topics.id"))
    madhab_id = Column(Integer, ForeignKey("madhabs.id"))
    ruling_type = Column(String(50))
    ruling_arabic = Column(String(100))
    ruling_text = Column(Text, nullable=False)
    ruling_summary = Column(Text)
    conditions = Column(Text)
    exceptions = Column(Text)
    differences_of_opinion = Column(Text)
    quran_evidence = Column(Text)
    hadith_evidence = Column(Text)
    ijma_evidence = Column(Text)
    qiyas_evidence = Column(Text)
    scholar_name = Column(String(200))
    scholar_opinion_date = Column(String(50))
    reference_book = Column(String(300))
    reference_page = Column(String(50))
    is_authentic_ruling = Column(Boolean, default=True)
    verified_by = Column(String(200))
    review_date = Column(DateTime)
    complexity_level = Column(String(20))
    applicable_today = Column(Boolean, default=True)
    
    topic = relationship("FiqhTopic", back_populates="rulings")
    madhab = relationship("Madhab", back_populates="rulings")

class FiqhScholar(BaseModel, Base):
    __tablename__ = "fiqh_scholars"
    
    scholar_name = Column(String(200), nullable=False)
    scholar_full_name = Column(String(300))
    scholar_name_arabic = Column(String(300))
    madhab_id = Column(Integer, ForeignKey("madhabs.id"))
    birth_year = Column(String(10))
    death_year = Column(String(10))
    biography = Column(Text)
    major_works = Column(Text)
    students = Column(Text)
    teachers = Column(Text)
    era = Column(String(100))
    
    madhab = relationship("Madhab", back_populates="scholars")

class FiqhEvidence(BaseModel, Base):
    __tablename__ = "fiqh_evidence"
    
    evidence_type = Column(String(50))
    evidence_text = Column(Text, nullable=False)
    evidence_arabic = Column(Text)
    source_reference = Column(String(300))
    strength = Column(String(50))
    explanation = Column(Text)
