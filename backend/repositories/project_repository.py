from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.project import Project
from backend.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Repository responsible for all Project
    database operations.

    This class extends BaseRepository and
    adds project-specific queries.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(db=db, model=Project)

    # -----------------------------------------------------
    # Get project using project id
    # -----------------------------------------------------

    def get_project(
        self,
        project_id: str,
    ) -> Optional[Project]:
        return self.get_by_id(project_id)

    # -----------------------------------------------------
    # Return every project
    # -----------------------------------------------------

    def list_projects(self):
        return self.get_all()

    # -----------------------------------------------------
    # Fetch all projects belonging to a user
    # -----------------------------------------------------

    def get_projects_by_owner(
        self,
        owner_id: str,
    ) -> list[Project]:

        stmt = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .order_by(Project.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    # -----------------------------------------------------
    # Search projects by name
    # -----------------------------------------------------

    def search_projects(
        self,
        keyword: str,
    ) -> list[Project]:

        stmt = (
            select(Project)
            .where(Project.name.ilike(f"%{keyword}%"))
            .order_by(Project.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    # -----------------------------------------------------
    # Check duplicate project
    # -----------------------------------------------------

    def project_exists(
        self,
        owner_id: str,
        name: str,
    ) -> bool:

        stmt = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .where(Project.name == name)
        )

        project = self.db.scalar(stmt)

        return project is not None

    # -----------------------------------------------------
    # Create project
    # -----------------------------------------------------

    def create_project(
        self,
        name: str,
        description: str,
        owner_id: str,
    ) -> Project:

        return self.create(
            name=name,
            description=description,
            owner_id=owner_id,
        )

    # -----------------------------------------------------
    # Delete project
    # -----------------------------------------------------

    def delete_project(
        self,
        project: Project,
    ) -> None:

        self.delete(project)
