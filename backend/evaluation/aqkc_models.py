"""
NovaQure

AQKC Models

Internal models for the Adaptive Quantum Knowledge
Correction (AQKC) service.

These models are internal to the Evaluation module and
are not exposed as external API contracts.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AQKCResult(BaseModel):
    """
    Result produced by the AQKC correction pipeline.
    """

    corrected_energy: float = Field(
        ...,
        description="Quantum energy after AQKC correction.",
    )

    noise_score: float = Field(
        ...,
        description="Normalized quantum noise score.",
    )

    correction_factor: float = Field(
        ...,
        description="AQKC correction factor applied to the energy.",
    )