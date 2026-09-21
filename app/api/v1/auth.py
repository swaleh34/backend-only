from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import auth_service
from app.models.user import User
from datetime import timedelta

router = APIRouter()

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    """
    user, error = auth_service.register_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {
        "status": "success",
        "message": "Account created successfully. Alhamdulillah!",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login to get access token.
    """
    user = auth_service.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.account_status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )
    
    # Create tokens
    access_token = auth_service.create_access_token(
        data={"sub": user.id, "username": user.username}
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_scholar": user.is_scholar
        }
    }

@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token.
    """
    try:
        payload = auth_service.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        new_access_token = auth_service.create_access_token(
            data={"sub": user.id, "username": user.username}
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(auth_service.get_current_active_user)
):
    """
    Get current user information.
    """
    return {
        "status": "success",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "bio": current_user.bio,
            "country": current_user.country,
            "language_preference": current_user.language_preference,
            "madhab_preference": current_user.madhab_preference,
            "is_scholar": current_user.is_scholar,
            "is_admin": current_user.is_admin,
            "joined_at": str(current_user.joined_at)
        }
    }

@router.put("/profile")
async def update_profile(
    full_name: Optional[str] = None,
    bio: Optional[str] = None,
    country: Optional[str] = None,
    language_preference: Optional[str] = None,
    madhab_preference: Optional[str] = None,
    current_user: User = Depends(auth_service.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile.
    """
    updated_user = auth_service.update_user_profile(
        db=db,
        user=current_user,
        full_name=full_name,
        bio=bio,
        country=country,
        language_preference=language_preference,
        madhab_preference=madhab_preference
    )
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "user": {
            "id": updated_user.id,
            "username": updated_user.username,
            "full_name": updated_user.full_name,
            "bio": updated_user.bio
        }
    }
