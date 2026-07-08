from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import get_project_service
from backend.schemas.project import (
    ProjectCreate,
    ProjectResponse,
)
from backend.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# ---------------------------------------------------------
# Create Project
# ---------------------------------------------------------

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: ProjectCreate,
    service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
):

    try:

        created_project = service.create_project(
            owner_id="demo-user",
            name=project.name,
            description=project.description or "",
        )

        return created_project

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Projects
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
):

    return service.list_projects()


# ---------------------------------------------------------
# Get Project
# ---------------------------------------------------------

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: str,
    service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
):

    project = service.get_project(project_id)

    if project is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


# ---------------------------------------------------------
# Delete Project
# ---------------------------------------------------------

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: str,
    service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
):

    deleted = service.delete_project(
        project_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return None
