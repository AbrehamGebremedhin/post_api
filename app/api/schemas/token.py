"""
Token schema module.
This module defines Pydantic schemas for token-related operations.
"""
from pydantic import BaseModel, Field

class Token(BaseModel):
    """
    Schema for access token.
    
    Attributes:
        access_token (str): The JWT token.
        token_type (str): The token type, e.g., "bearer".
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type")

class TokenData(BaseModel):
    """
    Schema for token data.
    
    Attributes:
        user_id (int): The user ID associated with the token.
        email (str): The email associated with the token.
    """
    user_id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email") 