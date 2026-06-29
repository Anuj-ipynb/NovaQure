from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

from backend.contracts.candidate_metrics import (
    CandidateMetrics,
)


class Molecule(BaseModel):
    """
    Canonical molecular representation used throughout
    the NovaQure pipeline.
    """

    molecule_id: str

    smiles: str

    selfies: str

    source: str = "dataset"

    validity_score: float = 1.0

    latent_vector: list[float] | None = None

    generation_iteration: int = 0

    metrics: CandidateMetrics = Field(
        default_factory=CandidateMetrics
    )