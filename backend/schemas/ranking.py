from typing import Optional

from pydantic import Field

from backend.schemas.base_schema import (
    NovaQureSchema,
    TimestampSchema,
)


# ---------------------------------------------------------
# Create Ranking
# ---------------------------------------------------------


class RankingCreate(NovaQureSchema):
    """
    Request DTO used when creating
    a new ranking.
    """

    molecule_id: str = Field(
        ...,
        description="Associated Molecule ID",
    )

    rank: int = Field(
        ...,
        ge=1,
        description="Ranking Position",
    )

    score: float = Field(
        ...,
        ge=0,
        description="Overall Score",
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence Score",
    )


# ---------------------------------------------------------
# Update Ranking
# ---------------------------------------------------------


class RankingUpdate(NovaQureSchema):
    """
    DTO used for updating ranking data.
    """

    rank: Optional[int] = Field(
        default=None,
        ge=1,
    )

    score: Optional[float] = Field(
        default=None,
        ge=0,
    )

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
    )


# ---------------------------------------------------------
# Ranking Response
# ---------------------------------------------------------


class RankingResponse(TimestampSchema):
    """
    Full ranking response.
    """

    id: str

    molecule_id: str

    rank: int

    score: float

    confidence: float


# ---------------------------------------------------------
# Ranking Summary
# ---------------------------------------------------------


class RankingSummary(NovaQureSchema):
    """
    Lightweight ranking object
    used in list endpoints.
    """

    id: str

    rank: int

    score: float

    confidence: float


# ---------------------------------------------------------
# Ranking List Response
# ---------------------------------------------------------


class RankingListResponse(NovaQureSchema):
    """
    Collection of rankings.
    """

    rankings: list[RankingSummary]

    total: int
