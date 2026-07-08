from typing import Optional

from pydantic import Field

from backend.schemas.base_schema import (
    NovaQureSchema,
    TimestampSchema,
)


# ---------------------------------------------------------
# Create Project
# ---------------------------------------------------------


class ProjectCreate(NovaQureSchema):
    """
    DTO used when creating
    a new project.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="Project Name",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Project Description",
    )


# ---------------------------------------------------------
# Update Project
# ---------------------------------------------------------


class ProjectUpdate(NovaQureSchema):
    """
    DTO used when updating
    project information.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
    )


# ---------------------------------------------------------
# Project Response
# ---------------------------------------------------------


class ProjectResponse(TimestampSchema):
    """
    API response returned for
    a single project.
    """

    id: str

    name: str

    description: Optional[str]

    owner_id: str


# ---------------------------------------------------------
# Project Summary
# ---------------------------------------------------------


class ProjectSummary(NovaQureSchema):
    """
    Lightweight project object
    for lists.
    """

    id: str

    name: str


# ---------------------------------------------------------
# Project List
# ---------------------------------------------------------


class ProjectListResponse(NovaQureSchema):
    """
    Collection returned by
    list endpoints.
    """

    projects: list[ProjectSummary]

    total: int
