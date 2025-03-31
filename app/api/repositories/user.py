"""
User repository module.
This module provides repository classes for user operations.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate
from app.api.repositories.base import BaseRepository, AsyncBaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for synchronous user operations.
    """
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            db: The database session.
            email: The email to search for.
        
        Returns:
            The user if found, None otherwise.
        """
        return db.query(User).filter(User.email == email).first()

class AsyncUserRepository(AsyncBaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for asynchronous user operations.
    """
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email asynchronously.
        
        Args:
            db: The async database session.
            email: The email to search for.
        
        Returns:
            The user if found, None otherwise.
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

# Create repository instances
user_repository = UserRepository(User)
async_user_repository = AsyncUserRepository(User) 