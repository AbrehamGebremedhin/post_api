"""
Base service module.
This module provides base classes for services with the Strategy pattern.
"""
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from app.api.utils.database import Base
from app.api.repositories.base import BaseRepository, AsyncBaseRepository

# Define type variables
ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=BaseRepository)
AsyncRepoType = TypeVar("AsyncRepoType", bound=AsyncBaseRepository)

class ServiceStrategy(ABC, Generic[ModelType]):
    """
    Abstract base class for service strategies.
    Implements the Strategy pattern for services.
    """
    @abstractmethod
    def get_repository(self):
        """
        Get the repository for this strategy.
        
        Returns:
            The repository.
        """
        pass

class SyncServiceStrategy(ServiceStrategy[ModelType], Generic[ModelType, RepoType]):
    """
    Synchronous service strategy.
    Uses a synchronous repository.
    """
    def __init__(self, repository: RepoType):
        """
        Initialize with a repository.
        
        Args:
            repository: The repository to use.
        """
        self.repository = repository
        
    def get_repository(self) -> RepoType:
        """
        Get the repository for this strategy.
        
        Returns:
            The repository.
        """
        return self.repository

class AsyncServiceStrategy(ServiceStrategy[ModelType], Generic[ModelType, AsyncRepoType]):
    """
    Asynchronous service strategy.
    Uses an asynchronous repository.
    """
    def __init__(self, repository: AsyncRepoType):
        """
        Initialize with a repository.
        
        Args:
            repository: The repository to use.
        """
        self.repository = repository
        
    def get_repository(self) -> AsyncRepoType:
        """
        Get the repository for this strategy.
        
        Returns:
            The repository.
        """
        return self.repository

class BaseService(Generic[ModelType]):
    """
    Base service class.
    Uses a strategy to determine whether to use synchronous or asynchronous operations.
    """
    def __init__(self, strategy: ServiceStrategy[ModelType]):
        """
        Initialize with a strategy.
        
        Args:
            strategy: The strategy to use.
        """
        self._strategy = strategy
        
    @property
    def repository(self):
        """
        Get the repository for the current strategy.
        
        Returns:
            The repository.
        """
        return self._strategy.get_repository()
        
    def set_strategy(self, strategy: ServiceStrategy[ModelType]):
        """
        Set the strategy.
        
        Args:
            strategy: The strategy to use.
        """
        self._strategy = strategy 