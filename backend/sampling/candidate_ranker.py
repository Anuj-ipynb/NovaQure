from __future__ import annotations

from backend.contracts.molecule import Molecule

from backend.generation.generation_config import (
    GenerationConfig,
)


class CandidateRanker:
    """
    Rank molecules using metrics already computed by
    the filtering stages.

    This class intentionally performs no chemistry.
    It simply aggregates quality metrics into a single
    score for downstream selection.
    """

    def rank(
        self,
        molecules: list[Molecule],
    ) -> list[Molecule]:

        if not molecules:
            return []

        weights = (
            GenerationConfig.RANKING_WEIGHTS
        )

        for molecule in molecules:

            molecule.metrics.validity = (
                molecule.validity_score
            )

            molecule.metrics.compute_score(
                novelty_weight=weights[
                    "novelty"
                ],
                diversity_weight=weights[
                    "diversity"
                ],
                validity_weight=weights[
                    "validity"
                ],
            )
        for molecule in molecules:
            print(
        molecule.smiles,
        molecule.metrics.novelty,
        molecule.metrics.diversity,
        molecule.metrics.overall_score,
        )

        return sorted(
            molecules,
            key=lambda molecule:
            molecule.metrics.overall_score,
            reverse=True,
        )