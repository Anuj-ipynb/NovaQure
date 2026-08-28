from __future__ import annotations

from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable CRUD operations.

    All specific repositories should inherit from this class.

    Example:
        class ProjectRepository(BaseRepository[Project]):
            ...
    """

    def __init__(self, db: Session, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    # -------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------

    def create(self, **kwargs: Any) -> ModelType:
        """
        Create and persist a new database record.
        """

        instance = self.model(**kwargs)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    # -------------------------------------------------------------
    # READ
    # -------------------------------------------------------------

    def get_by_id(self, entity_id: str) -> Optional[ModelType]:
        """
        Fetch a single record using its primary key.
        """

        return self.db.get(self.model, entity_id)

    def get_all(self) -> Sequence[ModelType]:
        """
        Fetch all records for this model.
        """

        stmt = select(self.model)

        return self.db.scalars(stmt).all()

    # -------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------

    def update(
        self,
        entity: ModelType,
        **kwargs: Any,
    ) -> ModelType:
        """
        Update selected fields on an existing entity.
        """

        for key, value in kwargs.items():
            setattr(entity, key, value)

        self.db.commit()
        self.db.refresh(entity)

        return entity

    # -------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------

    def delete(self, entity: ModelType) -> None:
        """
        Permanently delete an entity.
        """

        self.db.delete(entity)
        self.db.commit()

    # -------------------------------------------------------------
    # EXISTS
    # -------------------------------------------------------------

    def exists(self, entity_id: str) -> bool:
        """
        Returns True if the entity exists.
        """

        return self.get_by_id(entity_id) is not None

    # -------------------------------------------------------------
    # COUNT
    # -------------------------------------------------------------

    def count(self) -> int:
        """
        Return total number of rows.
        """

        stmt = select(self.model)

        return len(self.db.scalars(stmt).all())
