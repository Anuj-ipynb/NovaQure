"""
NovaQure

Internal models for ChEMBL API.

These models represent data returned from the ChEMBL REST API.
They are internal to the Evaluation module and are NOT API
contracts exposed by FastAPI.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChEMBLTarget(BaseModel):
    """
    Minimal representation of a ChEMBL target.
    """

    chembl_id: str = Field(
        ...,
        description="ChEMBL target identifier",
    )

    name: str = Field(
        ...,
        description="Preferred target name",
    )

    organism: str = Field(
        ...,
        description="Target organism",
    )

    target_type: str = Field(
        ...,
        description="Target type",
    )


class ChEMBLActivity(BaseModel):
    """
    Minimal bioactivity record.

    These values are later converted into a Chemprop
    training dataset.
    """

    smiles: str = Field(
        ...,
        description="Canonical SMILES",
    )

    activity_type: str = Field(
        ...,
        description="IC50, Ki, Kd, EC50, etc.",
    )

    value: float = Field(
        ...,
        description="Experimental activity value",
    )

    units: str = Field(
        ...,
        description="Measurement units",
    )

    relation: str = Field(
        default="=",
        description="Relation operator",
    )