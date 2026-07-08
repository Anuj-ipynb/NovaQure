from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CandidateMetrics:
    """
    Stores quality metrics associated with a generated
    molecule throughout the NovaQure pipeline.

    These metrics are progressively populated by the
    Generation and Evaluation modules and are used for
    candidate ranking and benchmarking.
    """

    novelty: float = 0.0

    diversity: float = 0.0

    validity: float = 1.0

    overall_score: float = 0.0

    def compute_score(
        self,
        novelty_weight: float,
        diversity_weight: float,
        validity_weight: float,
    ) -> float:
        """
        Compute the weighted overall score.
        """

        self.overall_score = (

            novelty_weight * self.novelty

            +

            diversity_weight * self.diversity

            +

            validity_weight * self.validity

        )

        return self.overall_score