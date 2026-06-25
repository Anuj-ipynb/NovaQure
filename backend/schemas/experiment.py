from typing import Optional

from pydantic import Field

from backend.schemas.base_schema import (
    NovaQureSchema,
    TimestampSchema,
)


# ---------------------------------------------------------
# Create Experiment
# ---------------------------------------------------------


class ExperimentCreate(NovaQureSchema):
    """
    Request DTO used when creating
    a new experiment.
    """

    project_id: str = Field(
        ...,
        description="Associated Project ID",
    )

    target_protein: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Target Protein",
    )

    iterations: int = Field(
        default=1,
        ge=1,
        le=100,
        description="Optimization Iterations",
    )


# ---------------------------------------------------------
# Update Experiment
# ---------------------------------------------------------


class ExperimentUpdate(NovaQureSchema):
    """
    DTO used for updating experiment
    properties.
    """

    status: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    iterations: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
    )


# ---------------------------------------------------------
# Experiment Response
# ---------------------------------------------------------


class ExperimentResponse(TimestampSchema):
    """
    Full experiment response.
    """

    id: str

    project_id: str

    target_protein: str

    iterations: int

    status: str


# ---------------------------------------------------------
# Experiment Summary
# ---------------------------------------------------------


class ExperimentSummary(NovaQureSchema):
    """
    Lightweight experiment object
    used in list APIs.
    """

    id: str

    target_protein: str

    status: str


# ---------------------------------------------------------
# Experiment List Response
# ---------------------------------------------------------


class ExperimentListResponse(NovaQureSchema):
    """
    Collection of experiments.
    """

    experiments: list[ExperimentSummary]

    total: int
