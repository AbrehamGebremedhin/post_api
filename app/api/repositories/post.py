"""
Post repository module.
This module provides repository classes for post operations.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.api.models.post import Post
from app.api.schemas.post import PostCreate, PostUpdate
from app.api.repositories.base import BaseRepository, AsyncBaseRepository

class PostRepository(BaseRepository[Post, PostCreate, PostUpdate]):
    """
    Repository for synchronous post operations.
    """
    def get_by_user_id(self, db: Session, user_id: int) -> List[Post]:
        """
        Get all posts for a user.
        
        Args:
            db: The database session.
            user_id: The user ID.
        
        Returns:
            List of posts.
        """
        return db.query(Post).filter(Post.user_id == user_id).all()
        
    def get_by_id_and_user_id(self, db: Session, post_id: int, user_id: int) -> Optional[Post]:
        """
        Get a post by ID and user ID.
        
        Args:
            db: The database session.
            post_id: The post ID.
            user_id: The user ID.
        
        Returns:
            The post if found, None otherwise.
        """
        return db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()

class AsyncPostRepository(AsyncBaseRepository[Post, PostCreate, PostUpdate]):
    """
    Repository for asynchronous post operations.
    """
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> List[Post]:
        """
        Get all posts for a user asynchronously.
        
        Args:
            db: The async database session.
            user_id: The user ID.
        
        Returns:
            List of posts.
        """
        result = await db.execute(select(Post).filter(Post.user_id == user_id))
        return result.scalars().all()
        
    async def get_by_id_and_user_id(self, db: AsyncSession, post_id: int, user_id: int) -> Optional[Post]:
        """
        Get a post by ID and user ID asynchronously.
        
        Args:
            db: The async database session.
            post_id: The post ID.
            user_id: The user ID.
        
        Returns:
            The post if found, None otherwise.
        """
        result = await db.execute(select(Post).filter(Post.id == post_id, Post.user_id == user_id))
        return result.scalars().first()

# Create repository instances
post_repository = PostRepository(Post)
async_post_repository = AsyncPostRepository(Post) 