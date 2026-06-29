from __future__ import annotations

from backend.contracts.molecule import Molecule

from backend.sampling.fingerprints import (
    generate_fingerprint,
    tanimoto_similarity,
)


class NoveltyFilter:

    def __init__(
        self,
        threshold: float = 0.90,
    ) -> None:

        self.threshold = threshold

    def filter(
        self,
        molecules: list[Molecule],
        reference_smiles: list[str],
    ) -> list[Molecule]:
        """
        Filter molecules that are too similar to the
        reference dataset while preserving the computed
        novelty score for downstream ranking.
        """

        reference_fingerprints = [

            generate_fingerprint(
                smiles
            )

            for smiles in reference_smiles

        ]

        accepted: list[Molecule] = []

        for molecule in molecules:

            fingerprint = generate_fingerprint(
                molecule.smiles
            )

            if not reference_fingerprints:

                molecule.metrics.novelty = 1.0
                molecule.metrics.validity = (
                    molecule.validity_score
                )

                accepted.append(
                    molecule
                )

                continue

            maximum_similarity = max(

                tanimoto_similarity(
                    fingerprint,
                    reference,
                )

                for reference in reference_fingerprints

            )

            novelty = (
                1.0 - maximum_similarity
            )

            molecule.metrics.novelty = novelty

            molecule.metrics.validity = (
                molecule.validity_score
            )

            if maximum_similarity < self.threshold:

                accepted.append(
                    molecule
                )

        return accepted