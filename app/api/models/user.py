"""
User model module.
This module defines the SQLAlchemy model for the user entity.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.api.utils.database import Base

class User(Base):
    """
    User model for storing user related details.
    
    Attributes:
        id (int): The primary key.
        email (str): The user's email address.
        hashed_password (str): The hashed password.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 