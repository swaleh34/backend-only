from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import db_manager
from app.api.v1 import quran, hadith, fiqh, chat, auth
from app.services.cache_service import cache_service
# After database initialization
from app.services.rag_service import rag_service
rag_service.initialize()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("=" * 70)
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   SWALEH AI - ISLAMIC ASSISTANT               ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Version: {settings.VERSION:<50}║")
    print(f"║  Environment: {settings.ENVIRONMENT:<43}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ                       ║")
    print("║  In the name of Allah, the Most Gracious, the Most Merciful ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("=" * 70)
    
    print("\n📚 Initializing Islamic Knowledge Base...")
    try:
        db_manager.create_all_tables()
        print("✅ Database tables ready")
    except Exception as e:
        print(f"⚠️ Database warning: {e}")
    
    print(f"\n🚀 Server running at http://{settings.HOST}:{settings.PORT}")
    print(f"📖 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"📚 ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print("=" * 70)
    print("✅ Swaleh AI is ready! Alhamdulillah.\n")
    
    yield
    
    # Shutdown
    print("\n" + "=" * 70)
    print("👋 Shutting down Swaleh AI...")
    print("🕌 JazakAllah khair for using Swaleh AI")
    print("=" * 70)

# Create FastAPI app
app = FastAPI(
    title="Swaleh AI - Islamic Assistant",
    version=settings.VERSION,
    description="""
    # 🕌 Swaleh AI - Advanced Islamic Assistant
    
    ## 📖 Authentic Islamic Knowledge
    
    * **📚 Quran** - Search, read, and understand the Holy Quran with authentic tafsir
    * **📜 Hadith** - Access authentic hadith from major collections with verification
    * **⚖️ Fiqh** - Islamic jurisprudence from recognized madhabs
    * **🤖 AI Chat** - Intelligent Islamic Q&A with source verification
    
    ## ⚠️ Important
    All information is based on Quran and authentic Sunnah.
    Always verify with qualified scholars for important matters.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(quran.router, prefix="/api/v1/quran", tags=["📚 Quran"])
app.include_router(hadith.router, prefix="/api/v1/hadith", tags=["📜 Hadith"])
app.include_router(fiqh.router, prefix="/api/v1/fiqh", tags=["⚖️ Fiqh"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["🤖 AI Chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["🔐 Auth"])

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "name": "Swaleh AI",
        "version": settings.VERSION,
        "bismillah": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "status": "Alhamdulillah - Running",
        "docs": "/docs",
        "endpoints": {
            "quran": "/api/v1/quran/surahs",
            "hadith": "/api/v1/hadith/collections",
            "fiqh": "/api/v1/fiqh/madhabs",
            "chat": "/api/v1/chat/ask",
            "auth": "/api/v1/auth/login"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )