"""
Post schema module.
This module defines Pydantic schemas for post-related operations.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class PostBase(BaseModel):
    """
    Base schema for post data.
    
    Attributes:
        text (str): The post content.
    """
    text: str = Field(
        ..., 
        description="Post content",
        min_length=1,
        max_length=1000000  # 1MB limit for text content
    )
    
    @field_validator("text")
    def validate_content_size(cls, v):
        """
        Validate that the post content size is within limits.
        
        Args:
            v (str): The post content to validate.
            
        Returns:
            str: The validated post content.
            
        Raises:
            ValueError: If the content size exceeds the limit.
        """
        # Calculate size in bytes (UTF-8 encoding)
        size_in_bytes = len(v.encode('utf-8'))
        
        # 1MB = 1048576 bytes
        if size_in_bytes > 1048576:
            raise ValueError("Post content size exceeds the limit of 1MB")
        return v

class PostCreate(PostBase):
    """
    Schema for creating a new post.
    
    Attributes:
        text (str): The post content.
    """
    pass

class PostUpdate(BaseModel):
    """
    Schema for updating post data.
    
    Attributes:
        text (Optional[str]): The updated post content.
    """
    text: Optional[str] = Field(
        None,
        description="Updated post content",
        min_length=1,
        max_length=1000000  # 1MB limit for text content
    )
    
    @field_validator("text")
    def validate_content_size(cls, v):
        """
        Validate that the post content size is within limits.
        
        Args:
            v (str): The post content to validate.
            
        Returns:
            str: The validated post content.
            
        Raises:
            ValueError: If the content size exceeds the limit.
        """
        if v is None:
            return v
            
        # Calculate size in bytes (UTF-8 encoding)
        size_in_bytes = len(v.encode('utf-8'))
        
        # 1MB = 1048576 bytes
        if size_in_bytes > 1048576:
            raise ValueError("Post content size exceeds the limit of 1MB")
        return v

class Post(PostBase):
    """
    Schema for full post data.
    
    Attributes:
        id (int): The post ID.
        user_id (int): The ID of the user who created the post.
        created_at (datetime): The timestamp when the post was created.
        updated_at (datetime): The timestamp when the post was last updated.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostResponse(Post):
    """
    Schema for post response data.
    
    Attributes:
        id (int): The post ID.
        text (str): The post content.
        user_id (int): The ID of the user who created the post.
        created_at (datetime): The timestamp when the post was created.
        updated_at (datetime): The timestamp when the post was last updated.
    """
    pass

class PostDelete(BaseModel):
    """
    Schema for post deletion.
    
    Attributes:
        post_id (int): The ID of the post to delete.
    """
    post_id: int = Field(..., description="Post ID to delete")

class PostListResponse(BaseModel):
    """
    Schema for a list of posts.
    
    Attributes:
        posts (List[Post]): A list of posts.
    """
    posts: List[Post]

    model_config = ConfigDict(from_attributes=True) 