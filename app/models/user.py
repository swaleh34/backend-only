from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, 
    Boolean, DateTime, Float, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, BaseModel
import uuid

class User(BaseModel, Base):
    __tablename__ = "users"
    
    user_uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(200), nullable=False)
    avatar_url = Column(String(500))
    bio = Column(Text)
    country = Column(String(100))
    language_preference = Column(String(10), default="en")
    madhab_preference = Column(String(50))
    is_verified = Column(Boolean, default=False)
    is_scholar = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    account_status = Column(String(20), default="active")
    last_login = Column(DateTime)
    joined_at = Column(DateTime, default=func.now())
    
    queries = relationship("UserQuery", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("UserNote", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserQuery(BaseModel, Base):
    __tablename__ = "user_queries"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query_text = Column(Text, nullable=False)
    query_language = Column(String(10), default="en")
    query_type = Column(String(50))
    response_text = Column(Text)
    response_language = Column(String(10))
    ai_model_used = Column(String(100))
    response_time = Column(Float)
    sources_used = Column(JSON)
    is_satisfied = Column(Boolean)
    user_feedback = Column(Text)
    rating = Column(Integer)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    user = relationship("User", back_populates="queries")

class UserFavorite(BaseModel, Base):
    __tablename__ = "user_favorites"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50))
    content_id = Column(Integer)
    content_reference = Column(String(200))
    notes = Column(Text)
    tags = Column(JSON)
    
    user = relationship("User", back_populates="favorites")

class UserNote(BaseModel, Base):
    __tablename__ = "user_notes"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50))
    content_id = Column(Integer)
    note_title = Column(String(200))
    note_text = Column(Text)
    is_private = Column(Boolean, default=True)
    tags = Column(JSON)
    
    user = relationship("User", back_populates="notes")

class UserSettings(BaseModel, Base):
    __tablename__ = "user_settings"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    theme = Column(String(20), default="light")
    font_size = Column(String(10), default="medium")
    arabic_font_size = Column(String(10), default="large")
    default_language = Column(String(10), default="en")
    default_madhab = Column(String(50), default="General")
    preferred_translators = Column(JSON)
    preferred_reciters = Column(JSON)
    email_notifications = Column(Boolean, default=True)
    daily_verse = Column(Boolean, default=True)
    prayer_times = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="settings")
