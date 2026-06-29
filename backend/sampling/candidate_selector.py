from __future__ import annotations

from backend.contracts.molecule import Molecule

from backend.sampling.candidate_ranker import (
    CandidateRanker,
)

from backend.sampling.diversity_filter import (
    DiversityFilter,
)

from backend.sampling.novelty_filter import (
    NoveltyFilter,
)


class CandidateSelector:
    """
    Coordinates candidate filtering and ranking.

    Pipeline

        Dataset
            │
            ▼
      Novelty Filter
            │
            ▼
     Diversity Filter
            │
            ▼
      Candidate Ranker
            │
            ▼
      Final Candidates
    """

    def __init__(
        self,
        diversity_threshold: float = 0.85,
        novelty_threshold: float = 0.90,
    ) -> None:

        self._novelty_filter = NoveltyFilter(
            threshold=novelty_threshold,
        )

        self._diversity_filter = DiversityFilter(
            threshold=diversity_threshold,
        )

        self._ranker = CandidateRanker()

    def select(
        self,
        molecules: list[Molecule],
        reference_smiles: list[str],
    ) -> list[Molecule]:
        """
        Preserve dataset molecules.

        Apply novelty filtering,
        diversity filtering,
        then rank the generated molecules.
        """

        dataset_molecules = [

            molecule

            for molecule in molecules

            if molecule.source == "dataset"

        ]

        generated_molecules = [

            molecule

            for molecule in molecules

            if molecule.source != "dataset"

        ]

        generated_molecules = (
            self._novelty_filter.filter(
                generated_molecules,
                reference_smiles,
            )
        )

        generated_molecules = (
            self._diversity_filter.filter(
                generated_molecules,
            )
        )

        generated_molecules = (
            self._ranker.rank(
                generated_molecules,
            )
        )

        return (
            dataset_molecules
            + generated_molecules
        )