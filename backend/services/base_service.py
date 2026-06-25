from __future__ import annotations

from typing import Generic, Optional, TypeVar


RepositoryType = TypeVar("RepositoryType")
ModelType = TypeVar("ModelType")


class BaseService(Generic[RepositoryType, ModelType]):
    """
    Base Service

    All business services inherit from this class.

    Responsibilities:

    - Hold repository instance
    - Common validation
    - Shared helper methods
    """

    def __init__(
        self,
        repository: RepositoryType,
    ) -> None:

        self.repository = repository

    # ---------------------------------------------------------
    # Generic Entity Lookup
    # ---------------------------------------------------------

    def get_by_id(
        self,
        entity_id: str,
    ) -> Optional[ModelType]:

        return self.repository.get_by_id(entity_id)

    # ---------------------------------------------------------
    # Generic Existence Check
    # ---------------------------------------------------------

    def exists(
        self,
        entity_id: str,
    ) -> bool:

        return self.repository.exists(entity_id)

    # ---------------------------------------------------------
    # Generic Count
    # ---------------------------------------------------------

    def count(self) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Delete Entity
    # ---------------------------------------------------------

    def delete(
        self,
        entity: ModelType,
    ) -> None:

        self.repository.delete(entity)
