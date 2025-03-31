"""
Authentication routes module.
This module defines routes for user authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.utils.database import get_db, get_async_db
from app.api.schemas.user import UserCreate, UserResponse
from app.api.schemas.token import Token
from app.api.services.user import user_service
from app.api.services.base import AsyncServiceStrategy
from app.api.repositories.user import async_user_repository

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """
    Sign up a new user.
    
    Args:
        user_data (UserCreate): The user data.
        db (AsyncSession): The database session.
        
    Returns:
        Token: The access token.
        
    Raises:
        HTTPException: If the email is already registered.
    """
    # Set async strategy for this request
    user_service.set_strategy(AsyncServiceStrategy(async_user_repository))
    
    # Check if the email is already registered
    db_user = await user_service.get_user_by_email_async(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create the user
    user = await user_service.create_user_async(db=db, user_data=user_data)
    
    # Generate a token
    token = user_service.create_user_token(user)
    
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_async_db)
):
    """
    Log in a user.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.
        db (AsyncSession): The database session.
        
    Returns:
        Token: The access token.
        
    Raises:
        HTTPException: If authentication fails.
    """
    # Set async strategy for this request
    user_service.set_strategy(AsyncServiceStrategy(async_user_repository))
    
    # Authenticate the user
    user = await user_service.authenticate_user_async(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate a token
    token = user_service.create_user_token(user)
    
    return {"access_token": token, "token_type": "bearer"} 