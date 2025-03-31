"""
Post service module.
This module provides service functions for post operations.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.models.post import Post
from app.api.models.user import User
from app.api.schemas.post import PostCreate, PostDelete, PostUpdate
from app.api.utils.cache import set_cache, get_cache, clear_cache, generate_post_cache_key
from app.api.repositories.post import post_repository, async_post_repository
from app.api.services.base import BaseService, SyncServiceStrategy, AsyncServiceStrategy

class PostService(BaseService[Post]):
    """
    Post service class with support for both sync and async operations.
    """
    async def get_posts_by_user_async(self, db: AsyncSession, user_id: int) -> List[Post]:
        """
        Get all posts for a user with caching asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            user_id (int): The user ID.
            
        Returns:
            List[Post]: The list of posts.
        """
        # Generate cache key for this user's posts
        cache_key = generate_post_cache_key(user_id)
        
        # Try to get from cache
        cached_posts = get_cache(cache_key)
        if cached_posts is not None:
            return cached_posts
        
        # If not in cache, fetch from the database
        posts = await async_post_repository.get_by_user_id(db, user_id)
        
        # Cache the posts for 5 minutes
        set_cache(cache_key, posts, ttl_minutes=5)
        
        return posts
    
    def get_posts_by_user(self, db: Session, user_id: int) -> List[Post]:
        """
        Get all posts for a user with caching.
        
        Args:
            db (Session): The database session.
            user_id (int): The user ID.
            
        Returns:
            List[Post]: The list of posts.
        """
        # Generate cache key for this user's posts
        cache_key = generate_post_cache_key(user_id)
        
        # Try to get from cache
        cached_posts = get_cache(cache_key)
        if cached_posts is not None:
            return cached_posts
        
        # If not in cache, fetch from the database
        posts = post_repository.get_by_user_id(db, user_id)
        
        # Cache the posts for 5 minutes
        set_cache(cache_key, posts, ttl_minutes=5)
        
        return posts

    async def create_post_async(self, db: AsyncSession, post_data: PostCreate, user: User) -> Post:
        """
        Create a new post asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            post_data (PostCreate): The post data.
            user (User): The user creating the post.
            
        Returns:
            Post: The created post.
        """
        # Extract user_id to avoid lazy loading issues
        user_id = user.id
        
        # Create a new post using repository
        post = await async_post_repository.create(
            db=db, 
            obj_in=post_data, 
            user_id=user_id
        )
        
        # Invalidate the cached posts for this user
        cache_key = generate_post_cache_key(user_id)
        clear_cache(cache_key)
        
        return post
    
    def create_post(self, db: Session, post_data: PostCreate, user: User) -> Post:
        """
        Create a new post.
        
        Args:
            db (Session): The database session.
            post_data (PostCreate): The post data.
            user (User): The user creating the post.
            
        Returns:
            Post: The created post.
        """
        # Create a new post using repository
        post = post_repository.create(
            db=db, 
            obj_in=post_data, 
            user_id=user.id
        )
        
        # Invalidate the cached posts for this user
        cache_key = generate_post_cache_key(user.id)
        clear_cache(cache_key)
        
        return post

    async def delete_post_async(self, db: AsyncSession, post_id: int, user_id: int) -> bool:
        """
        Delete a post asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            post_id (int): The post ID to delete.
            user_id (int): The user ID of the post owner.
            
        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        # Get the post
        post = await self.get_post_by_id_async(db, post_id, user_id)
        
        if not post:
            return False
        
        # Delete the post
        await async_post_repository.delete(db, id=post_id)
        
        # Invalidate the cached posts for this user
        cache_key = generate_post_cache_key(user_id)
        clear_cache(cache_key)
        
        return True
    
    def delete_post(self, db: Session, post_id: int, user_id: int) -> bool:
        """
        Delete a post.
        
        Args:
            db (Session): The database session.
            post_id (int): The post ID to delete.
            user_id (int): The user ID of the post owner.
            
        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        # Get the post
        post = self.get_post_by_id(db, post_id, user_id)
        
        if not post:
            return False
        
        # Delete the post
        post_repository.delete(db, id=post_id)
        
        # Invalidate the cached posts for this user
        cache_key = generate_post_cache_key(user_id)
        clear_cache(cache_key)
        
        return True

    async def get_post_by_id_async(self, db: AsyncSession, post_id: int, user_id: int) -> Optional[Post]:
        """
        Get a post by ID asynchronously.
        
        Args:
            db (AsyncSession): The async database session.
            post_id (int): The post ID.
            user_id (int): The user ID of the post owner.
            
        Returns:
            Optional[Post]: The post if found, None otherwise.
        """
        return await async_post_repository.get_by_id_and_user_id(db, post_id, user_id)
    
    def get_post_by_id(self, db: Session, post_id: int, user_id: int) -> Optional[Post]:
        """
        Get a post by ID.
        
        Args:
            db (Session): The database session.
            post_id (int): The post ID.
            user_id (int): The user ID of the post owner.
            
        Returns:
            Optional[Post]: The post if found, None otherwise.
        """
        return post_repository.get_by_id_and_user_id(db, post_id, user_id)

# Create service instances with strategies
sync_strategy = SyncServiceStrategy(post_repository)
async_strategy = AsyncServiceStrategy(async_post_repository)

# Default to sync strategy
post_service = PostService(sync_strategy) 