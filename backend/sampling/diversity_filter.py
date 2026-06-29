from __future__ import annotations

from backend.contracts.molecule import Molecule

from backend.sampling.fingerprints import (
    generate_fingerprint,
    tanimoto_similarity,
)


class DiversityFilter:

    def __init__(
        self,
        threshold: float = 0.85,
    ) -> None:

        self.threshold = threshold

    def filter(
        self,
        molecules: list[Molecule],
    ) -> list[Molecule]:
        """
        Greedy diversity selection using Morgan
        fingerprints.

        Accepted molecules retain their computed
        diversity score for downstream ranking.
        """

        selected: list[Molecule] = []

        selected_fingerprints = []

        for molecule in molecules:

            fingerprint = generate_fingerprint(
                molecule.smiles
            )

            if not selected:

                molecule.metrics.diversity = 1.0

                selected.append(
                    molecule
                )

                selected_fingerprints.append(
                    fingerprint
                )

                continue

            maximum_similarity = max(

                tanimoto_similarity(
                    fingerprint,
                    existing,
                )

                for existing in selected_fingerprints

            )

            diversity = (
                1.0 - maximum_similarity
            )

            molecule.metrics.diversity = (
                diversity
            )

            if maximum_similarity < self.threshold:

                selected.append(
                    molecule
                )

                selected_fingerprints.append(
                    fingerprint
                )

        return selected