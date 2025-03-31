"""
User schema module.
This module defines Pydantic schemas for user-related operations.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
import re

class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Attributes:
        email (EmailStr): The user's email address.
    """
    email: EmailStr = Field(..., description="User email address")

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    password: str = Field(
        ..., 
        description="User password", 
        min_length=8, 
        max_length=100
    )
    
    @field_validator("password")
    def password_strength(cls, v):
        """
        Validate password strength.
        
        Args:
            v (str): The password to validate.
        
        Returns:
            str: The validated password.
        
        Raises:
            ValueError: If the password is too weak.
        """
        # Check for at least one lowercase letter, one uppercase letter, one digit, and one special character
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, "
                "one digit, and one special character"
            )
        return v

class UserUpdate(BaseModel):
    """
    Schema for updating user data.
    
    Attributes:
        email (Optional[EmailStr]): The user's email address.
        password (Optional[str]): The user's password.
    """
    email: Optional[EmailStr] = Field(None, description="User email address")
    password: Optional[str] = Field(
        None, 
        description="User password", 
        min_length=8, 
        max_length=100
    )
    
    @field_validator("password")
    def password_strength(cls, v):
        """
        Validate password strength.
        
        Args:
            v (str): The password to validate.
        
        Returns:
            str: The validated password.
        
        Raises:
            ValueError: If the password is too weak.
        """
        if v is None:
            return v
            
        # Check for at least one lowercase letter, one uppercase letter, one digit, and one special character
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, "
                "one digit, and one special character"
            )
        return v

class UserInDB(UserBase):
    """
    Schema for user data as stored in the database.
    
    Attributes:
        id (int): The user's ID.
        email (EmailStr): The user's email address.
        hashed_password (str): The user's hashed password.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    """
    Schema for user response data.
    
    Attributes:
        id (int): The user's ID.
        email (EmailStr): The user's email address.
        created_at (datetime): The timestamp when the user was created.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password") 