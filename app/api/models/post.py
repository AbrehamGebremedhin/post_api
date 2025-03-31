"""
Post model module.
This module defines the SQLAlchemy model for the post entity.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.api.utils.database import Base

class Post(Base):
    """
    Post model for storing post related details.
    
    Attributes:
        id (int): The primary key.
        text (str): The post content.
        user_id (int): The foreign key referencing the user.
        created_at (datetime): The timestamp when the post was created.
        updated_at (datetime): The timestamp when the post was last updated.
        user (User): The relationship to the user who created the post.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Define relationship to the User model
    user = relationship("User", backref="posts") 