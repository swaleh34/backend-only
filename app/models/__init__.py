# Import Base first - only ONE Base class
from app.models.base import Base, BaseModel

# Import all models AFTER Base
from app.models.quran import (
    QuranMetadata, QuranVerse, QuranTranslation, 
    QuranTafsir, QuranWord, QuranRoot
)
from app.models.hadith import (
    HadithCollection, Hadith, HadithNarrator,
    HadithGrade, HadithChapter
)
from app.models.fiqh import (
    FiqhTopic, FiqhRuling, FiqhEvidence,
    FiqhScholar, Madhab, FiqhCategory
)
from app.models.user import (
    User, UserQuery, UserFavorite, 
    UserNote, UserSettings
)

__all__ = [
    "Base",
    "BaseModel",
    "QuranMetadata", "QuranVerse", "QuranTranslation",
    "QuranTafsir", "QuranWord", "QuranRoot",
    "HadithCollection", "Hadith", "HadithNarrator",
    "HadithGrade", "HadithChapter",
    "FiqhTopic", "FiqhRuling", "FiqhEvidence",
    "FiqhScholar", "Madhab", "FiqhCategory",
    "User", "UserQuery", "UserFavorite",
    "UserNote", "UserSettings"
]
