"""
Base repository module.
This module provides base repository classes for database operations.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.utils.database import Base

# Define a type variable for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)
# Define a type variable for Pydantic schemas
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository for synchronous database operations.
    Implements common CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the repository with a model.
        
        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: The database session.
            id: The record ID.
        
        Returns:
            The record if found, None otherwise.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            db: The database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List of records.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: The database session.
            obj_in: The input data.
            **kwargs: Additional fields.
        
        Returns:
            The created record.
        """
        obj_in_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in.dict()
        db_obj = self.model(**obj_in_data, **kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update a record.
        
        Args:
            db: The database session.
            db_obj: The database object to update.
            obj_in: The new data.
        
        Returns:
            The updated record.
        """
        obj_data = dict(db_obj.__dict__)
        update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> ModelType:
        """
        Delete a record.
        
        Args:
            db: The database session.
            id: The record ID.
        
        Returns:
            The deleted record.
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(obj)
        db.commit()
        return obj

class AsyncBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository for asynchronous database operations.
    Implements common CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the repository with a model.
        
        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: The async database session.
            id: The record ID.
        
        Returns:
            The record if found, None otherwise.
        """
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            db: The async database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List of records.
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: The async database session.
            obj_in: The input data.
            **kwargs: Additional fields.
        
        Returns:
            The created record.
        """
        obj_in_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in.dict()
        db_obj = self.model(**obj_in_data, **kwargs)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update a record.
        
        Args:
            db: The async database session.
            db_obj: The database object to update.
            obj_in: The new data.
        
        Returns:
            The updated record.
        """
        obj_data = dict(db_obj.__dict__)
        update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        Delete a record.
        
        Args:
            db: The async database session.
            id: The record ID.
        
        Returns:
            The deleted record.
        """
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        await db.delete(obj)
        await db.commit()
        return obj 