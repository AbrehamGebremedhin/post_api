"""
Posts routes module.
This module defines routes for post operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.utils.database import get_async_db
from app.api.dependencies.auth import get_current_user, get_current_user_async
from app.api.models.user import User
from app.api.schemas.post import PostCreate, PostResponse, PostListResponse, PostDelete
from app.api.services.post import post_service
from app.api.services.base import AsyncServiceStrategy
from app.api.repositories.post import async_post_repository
from app.api.repositories.user import async_user_repository

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def add_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user_async)
):
    """
    Create a new post.
    
    Args:
        post_data (PostCreate): The post data.
        db (AsyncSession): The database session.
        current_user (User): The authenticated user.
        
    Returns:
        PostResponse: The created post.
    """
    # Set async strategy for this request
    post_service.set_strategy(AsyncServiceStrategy(async_post_repository))
    
    # Extract user ID here to avoid lazy loading issues
    user_id = current_user.id
    
    # Get a fully loaded user instance to avoid async lazy loading issues
    user = await async_user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return await post_service.create_post_async(db=db, post_data=post_data, user=user)

@router.get("/", response_model=PostListResponse)
async def get_posts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user_async)
):
    """
    Get all posts for the current user with caching.
    
    Args:
        db (AsyncSession): The database session.
        current_user (User): The authenticated user.
        
    Returns:
        PostListResponse: The list of posts.
    """
    # Set async strategy for this request
    post_service.set_strategy(AsyncServiceStrategy(async_post_repository))
    
    # Extract user ID to avoid lazy loading issues
    user_id = current_user.id
    
    posts = await post_service.get_posts_by_user_async(db=db, user_id=user_id)
    return {"posts": posts}

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user_async)
):
    """
    Delete a post.
    
    Args:
        post_id (int): The post ID to delete.
        db (AsyncSession): The database session.
        current_user (User): The authenticated user.
        
    Raises:
        HTTPException: If the post is not found.
    """
    # Set async strategy for this request
    post_service.set_strategy(AsyncServiceStrategy(async_post_repository))
    
    # Extract user ID to avoid lazy loading issues
    user_id = current_user.id
    
    # Check if the post exists and belongs to the current user
    post = await post_service.get_post_by_id_async(db, post_id=post_id, user_id=user_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Delete the post
    success = await post_service.delete_post_async(db=db, post_id=post_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        ) 