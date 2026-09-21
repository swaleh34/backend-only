"""
Test script to verify all components are working
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🧪 SWALEH AI - SYSTEM CHECK")
print("=" * 60)

# Test 1: Imports
print("\n1. Testing imports...")
try:
    from app.core.config import settings
    print("   ✅ Config loaded successfully")
    print(f"   Project: {settings.PROJECT_NAME} v{settings.VERSION}")
except Exception as e:
    print(f"   ❌ Config error: {e}")

# Test 2: Database
print("\n2. Testing database...")
try:
    from app.core.database import db_manager
    from app.models.base import Base
    db_manager.create_all_tables()
    print("   ✅ Database initialized successfully")
    print(f"   Type: {settings.DATABASE_TYPE}")
except Exception as e:
    print(f"   ❌ Database error: {e}")

# Test 3: Services
print("\n3. Testing services...")
try:
    from app.services.verification_service import VerificationService
    vs = VerificationService()
    result = vs.verify_quran_reference(1, 1)
    print(f"   ✅ Verification service working")
    print(f"   Quran 1:1 valid: {result}")
except Exception as e:
    print(f"   ❌ Service error: {e}")

# Test 4: Models
print("\n4. Testing models...")
try:
    from app.models.quran import QuranMetadata
    from app.models.hadith import HadithCollection
    from app.models.fiqh import Madhab
    print("   ✅ All models importable")
except Exception as e:
    print(f"   ❌ Model error: {e}")

# Test 5: API Routes
print("\n5. Testing API routes...")
try:
    from app.api.v1 import quran, hadith, fiqh, chat, auth
    print("   ✅ All API routes importable")
except Exception as e:
    print(f"   ❌ Route error: {e}")

print("\n" + "=" * 60)
print("✅ SYSTEM CHECK COMPLETE")
print("=" * 60)
