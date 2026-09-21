from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
import re

class AuthService:
    """Advanced Authentication and Authorization Service"""
    
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12
        )
        self.oauth2_scheme = OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/login",
            auto_error=False  # Don't auto-raise for missing token
        )
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))
    
    def create_access_token(
        self, 
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
    
    def create_refresh_token(
        self, 
        data: Dict[str, Any]
    ) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_current_user(
        self,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")),
        db: Session = Depends(get_db)
    ) -> User:
        """Get current authenticated user"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = self.decode_token(token)
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        
        if user.account_status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not active"
            )
        
        return user
    
    async def get_current_active_user(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current active user"""
        if not current_user.is_active:
            raise HTTPException(
                status_code=400,
                detail="Inactive user"
            )
        return current_user
    
    async def get_current_scholar(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current scholar user"""
        if not current_user.is_scholar and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Scholar access required"
            )
        return current_user
    
    async def get_current_admin(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current admin user"""
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user
    
    def authenticate_user(
        self,
        db: Session,
        username: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by username and password"""
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def register_user(
        self,
        db: Session,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """Register a new user"""
        
        # Validate email
        if not self.validate_email(email):
            return None, "Invalid email format"
        
        # Validate password
        is_strong, password_msg = self.validate_password_strength(password)
        if not is_strong:
            return None, password_msg
        
        # Check if username exists
        if db.query(User).filter(User.username == username).first():
            return None, "Username already taken"
        
        # Check if email exists
        if db.query(User).filter(User.email == email).first():
            return None, "Email already registered"
        
        # Create user
        user = User(
            username=username,
            email=email,
            full_name=full_name or username,
            hashed_password=self.hash_password(password),
            is_active=True,
            account_status="active",
            joined_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create user settings
        from app.models.user import UserSettings
        settings_obj = UserSettings(
            user_id=user.id,
            default_language="en",
            theme="islamic"
        )
        db.add(settings_obj)
        db.commit()
        
        return user, None
    
    def update_user_profile(
        self,
        db: Session,
        user: User,
        **kwargs
    ) -> User:
        """Update user profile"""
        allowed_fields = [
            "full_name", "bio", "country", 
            "language_preference", "madhab_preference"
        ]
        
        for field in allowed_fields:
            if field in kwargs and kwargs[field] is not None:
                setattr(user, field, kwargs[field])
        
        db.commit()
        db.refresh(user)
        return user

# Create global auth service instance
auth_service = AuthService()
