"""
Authentication dependencies module.
This module provides dependencies for authentication.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.utils.database import get_db, get_async_db
from app.api.utils.security import SECRET_KEY, ALGORITHM
from app.api.models.user import User
from app.api.schemas.token import TokenData
from app.api.repositories.user import user_repository, async_user_repository

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user_async(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """
    Async dependency to get the current user from a token.
    
    Args:
        token (str): The token to decode.
        db (AsyncSession): The async database session.
        
    Returns:
        User: The current user.
        
    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("sub")
        email: Optional[str] = payload.get("email")
        
        if user_id is None or email is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=int(user_id), email=email)
    except JWTError:
        raise credentials_exception
        
    # Fetch the user from the database
    user = await async_user_repository.get(db, token_data.user_id)
    
    if user is None:
        raise credentials_exception
        
    return user

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current user from a token.
    
    Args:
        token (str): The token to decode.
        db (Session): The database session.
        
    Returns:
        User: The current user.
        
    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("sub")
        email: Optional[str] = payload.get("email")
        
        if user_id is None or email is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=int(user_id), email=email)
    except JWTError:
        raise credentials_exception
        
    # Fetch the user from the database
    user = user_repository.get(db, token_data.user_id)
    
    if user is None:
        raise credentials_exception
        
    return user 