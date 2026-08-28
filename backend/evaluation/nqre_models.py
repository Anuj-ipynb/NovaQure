"""
NovaQure

NQRE Models

Internal models for the NovaQure Quantum Reliability
Evaluation service.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class NQREResult(BaseModel):
    """
    Result produced by the NQRE evaluation pipeline.
    """

    reliability_score: float = Field(
        ...,
        description="Overall reliability score.",
    )

    confidence_score: float = Field(
        ...,
        description="Confidence score for the evaluated quantum result.",
    )