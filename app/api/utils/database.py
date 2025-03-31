"""
Database connection utility module.
This module provides database connection functions for the application.
"""
import os
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the DATABASE_URL to make it async-compatible
ASYNC_DATABASE_URL = DATABASE_URL.replace('mysql+mysqlconnector', 'mysql+aiomysql')

# Create engines - keep sync engine for init, use async for operations
sync_engine = create_engine(DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=async_engine
)

# Create base class for models
Base = declarative_base()

def init_db() -> None:
    """
    Initialize the database by creating all tables defined in models.
    This function should be called when starting the application.
    """
    # Import all models here to ensure they are registered with Base
    from app.api.models import user, post  # noqa
    
    # Create tables
    Base.metadata.create_all(bind=sync_engine)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.
    
    Returns:
        AsyncGenerator: An async database session generator.
    
    Yields:
        AsyncSession: An async database session.
    """
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()

def get_db() -> Generator:
    """
    Get a synchronous database session (for compatibility).
    
    Returns:
        Generator: A database session generator.
    
    Yields:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()