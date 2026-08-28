"""
NovaQure

Evaluation Models

Unified models for the complete evaluation pipeline.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """
    Complete molecular evaluation result.
    """

    qed: float = Field(
        ...,
        description="Quantitative Estimate of Drug-likeness (QED).",
    )

    sa_score: float = Field(
        ...,
        description="Synthetic accessibility score.",
    )

    lipinski_pass: bool = Field(
        ...,
        description="Lipinski Rule of Five evaluation result.",
    )

    affinity: float = Field(
        ...,
        description="Predicted binding affinity (pIC50).",
    )

    corrected_energy: float = Field(
        ...,
        description="AQKC-corrected quantum energy.",
    )

    noise_score: float = Field(
        ...,
        description="AQKC noise score.",
    )

    correction_factor: float = Field(
        ...,
        description="AQKC correction factor.",
    )

    reliability_score: float = Field(
        ...,
        description="NQRE reliability score.",
    )

    confidence_score: float = Field(
        ...,
        description="NQRE confidence score.",
    )

    iupac_name: str = Field(
        default="Unknown Candidate",
        description="Official IUPAC chemical name.",
    )