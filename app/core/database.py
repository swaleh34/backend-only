from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool
from typing import Generator, Optional
from pathlib import Path
from app.core.config import settings

# Import the ONE Base class
from app.models.base import Base

class DatabaseManager:
    """Advanced Database Manager with support for SQLite and PostgreSQL"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _get_database_url(self) -> str:
        """Get database URL based on configuration"""
        if settings.DATABASE_TYPE == "sqlite":
            db_path = settings.BASE_DIR / settings.SQLITE_DB_NAME
            db_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{db_path}"
        else:
            return (
                f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
                f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
            )
    
    def _initialize_engine(self):
        """Initialize database engine"""
        database_url = self._get_database_url()
        
        if settings.DATABASE_TYPE == "sqlite":
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False
            )
            
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        else:
            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=20,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_db(self) -> Generator[Session, None, None]:
        """Dependency to get database session"""
        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    
    def create_all_tables(self):
        """Create all database tables"""
        # Import models to register them with Base
        import app.models.quran
        import app.models.hadith
        import app.models.fiqh
        import app.models.user
        
        Base.metadata.create_all(bind=self.engine)
        print("✅ All database tables created successfully")
    
    def drop_all_tables(self):
        """Drop all database tables"""
        Base.metadata.drop_all(bind=self.engine)
        print("⚠️ All database tables dropped")

# Create database manager instance
db_manager = DatabaseManager()

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions"""
    db = db_manager.SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
