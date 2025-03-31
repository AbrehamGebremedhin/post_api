"""
Unit of Work pattern module.
This module provides a Unit of Work implementation for managing database transactions.
"""
from typing import AsyncContextManager, Callable, ContextManager
from contextlib import asynccontextmanager, contextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.utils.database import get_db, get_async_db

class UnitOfWork:
    """
    Synchronous Unit of Work implementation.
    Provides a context manager for managing database transactions.
    """
    def __init__(self, session_factory: Callable[[], ContextManager[Session]]):
        """
        Initialize the Unit of Work.
        
        Args:
            session_factory: A callable that returns a Session context manager.
        """
        self.session_factory = session_factory

    @contextmanager
    def __call__(self):
        """
        Get a database session and handle transaction management.
        
        Yields:
            Session: A database session.
        """
        with self.session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

class AsyncUnitOfWork:
    """
    Asynchronous Unit of Work implementation.
    Provides an async context manager for managing database transactions.
    """
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]):
        """
        Initialize the Async Unit of Work.
        
        Args:
            session_factory: A callable that returns an AsyncSession context manager.
        """
        self.session_factory = session_factory

    @asynccontextmanager
    async def __call__(self):
        """
        Get an async database session and handle transaction management.
        
        Yields:
            AsyncSession: An async database session.
        """
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

# Create instances
sync_uow = UnitOfWork(get_db)
async_uow = AsyncUnitOfWork(get_async_db) 