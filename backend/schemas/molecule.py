from typing import Optional

from pydantic import Field

from backend.schemas.base_schema import (
    NovaQureSchema,
    TimestampSchema,
)


# ---------------------------------------------------------
# Create Molecule
# ---------------------------------------------------------


class MoleculeCreate(NovaQureSchema):
    """
    Request DTO used when creating
    a molecule.
    """

    experiment_id: str = Field(
        ...,
        description="Experiment Identifier",
    )

    smiles: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="SMILES Representation",
    )

    selfies: Optional[str] = Field(
        default=None,
        max_length=500,
        description="SELFIES Representation",
    )

    score: float = Field(
        default=0.0,
        ge=0,
        description="Initial Molecule Score",
    )


# ---------------------------------------------------------
# Update Molecule
# ---------------------------------------------------------


class MoleculeUpdate(NovaQureSchema):
    """
    DTO used when updating
    molecule information.
    """

    smiles: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    selfies: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    score: Optional[float] = Field(
        default=None,
        ge=0,
    )


# ---------------------------------------------------------
# Molecule Response
# ---------------------------------------------------------


class MoleculeResponse(TimestampSchema):
    """
    Complete Molecule Response
    returned by the API.
    """

    id: str

    experiment_id: str

    smiles: str

    selfies: Optional[str]

    score: float


# ---------------------------------------------------------
# Molecule Summary
# ---------------------------------------------------------


class MoleculeSummary(NovaQureSchema):
    """
    Lightweight Molecule DTO
    for list endpoints.
    """

    id: str

    smiles: str

    score: float


# ---------------------------------------------------------
# Molecule List Response
# ---------------------------------------------------------


class MoleculeListResponse(NovaQureSchema):
    """
    Collection returned by
    Molecule APIs.
    """

    molecules: list[MoleculeSummary]

    total: int
