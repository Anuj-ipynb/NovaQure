from __future__ import annotations

from typing import Optional

from backend.models.project import Project
from backend.repositories.project_repository import ProjectRepository
from backend.services.base_service import BaseService


class ProjectService(
    BaseService[ProjectRepository, Project]
):
    """
    Project Service

    Handles all business logic related
    to Projects.

    Routers should interact only with this
    service rather than repositories.
    """

    def __init__(
        self,
        repository: ProjectRepository,
    ) -> None:

        super().__init__(repository)

    # ---------------------------------------------------------
    # Create Project
    # ---------------------------------------------------------

    def create_project(
        self,
        owner_id: str,
        name: str,
        description: str,
    ) -> Project:
        """
        Creates a new project.

        Duplicate project names for the same
        owner are not allowed.
        """

        exists = self.repository.project_exists(
            owner_id=owner_id,
            name=name,
        )

        if exists:
            raise ValueError(
                "A project with this name already exists."
            )

        return self.repository.create_project(
            owner_id=owner_id,
            name=name,
            description=description,
        )

    # ---------------------------------------------------------
    # Fetch Single Project
    # ---------------------------------------------------------

    def get_project(
        self,
        project_id: str,
    ) -> Optional[Project]:

        return self.repository.get_project(
            project_id
        )

    # ---------------------------------------------------------
    # Fetch All Projects
    # ---------------------------------------------------------

    def list_projects(
        self,
    ) -> list[Project]:

        return self.repository.list_projects()

    # ---------------------------------------------------------
    # Fetch Projects For Owner
    # ---------------------------------------------------------

    def get_projects_for_owner(
        self,
        owner_id: str,
    ) -> list[Project]:

        return self.repository.get_projects_by_owner(
            owner_id
        )

    # ---------------------------------------------------------
    # Search Projects
    # ---------------------------------------------------------

    def search_projects(
        self,
        keyword: str,
    ) -> list[Project]:

        keyword = keyword.strip()

        if not keyword:
            return []

        return self.repository.search_projects(
            keyword
        )

    # ---------------------------------------------------------
    # Delete Project
    # ---------------------------------------------------------

    def delete_project(
        self,
        project_id: str,
    ) -> bool:

        project = self.repository.get_project(
            project_id
        )

        if project is None:
            return False

        self.repository.delete_project(
            project
        )

        return True

    # ---------------------------------------------------------
    # Count Projects
    # ---------------------------------------------------------

    def total_projects(self) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Check Existence
    # ---------------------------------------------------------

    def project_exists(
        self,
        project_id: str,
    ) -> bool:

        return self.repository.exists(
            project_id
        )
