"""
User service module.
This module provides service functions for user operations.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.utils.security import get_password_hash, verify_password, create_access_token
from app.api.repositories.user import user_repository, async_user_repository
from app.api.services.base import BaseService, SyncServiceStrategy, AsyncServiceStrategy

class UserService(BaseService[User]):
    """
    User service class with support for both sync and async operations.
    """
    async def get_user_by_email_async(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            email (str): The email to search for.
            
        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        return await async_user_repository.get_by_email(db, email)
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            db (Session): The database session.
            email (str): The email to search for.
            
        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        return user_repository.get_by_email(db, email)

    async def create_user_async(self, db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            user_data (UserCreate): The user data.
            
        Returns:
            User: The created user.
        """
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create a dict from user_data but exclude the password field
        user_data_dict = user_data.model_dump(exclude={"password"})
        
        # Create the user using repository with hashed_password in kwargs
        return await async_user_repository.create(
            db=db, 
            obj_in=user_data_dict, 
            hashed_password=hashed_password
        )
    
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            db (Session): The database session.
            user_data (UserCreate): The user data.
            
        Returns:
            User: The created user.
        """
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create a dict from user_data but exclude the password field
        user_data_dict = user_data.model_dump(exclude={"password"})
        
        # Create the user using repository with hashed_password in kwargs
        return user_repository.create(
            db=db, 
            obj_in=user_data_dict, 
            hashed_password=hashed_password
        )

    async def authenticate_user_async(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            email (str): The user's email.
            password (str): The user's password.
            
        Returns:
            Optional[User]: The authenticated user if successful, None otherwise.
        """
        user = await self.get_user_by_email_async(db, email)
        
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            db (Session): The database session.
            email (str): The user's email.
            password (str): The user's password.
            
        Returns:
            Optional[User]: The authenticated user if successful, None otherwise.
        """
        user = self.get_user_by_email(db, email)
        
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user

    def create_user_token(self, user: User) -> str:
        """
        Create a token for a user.
        
        Args:
            user (User): The user to create a token for.
            
        Returns:
            str: The created token.
        """
        # Create token data
        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        
        # Create the token
        return create_access_token(token_data)

# Create service instances with strategies
sync_strategy = SyncServiceStrategy(user_repository)
async_strategy = AsyncServiceStrategy(async_user_repository)

# Default to sync strategy
user_service = UserService(sync_strategy) 