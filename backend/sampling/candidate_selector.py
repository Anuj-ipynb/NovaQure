from __future__ import annotations

from backend.contracts.molecule import (
    Molecule
)


class CandidateSelector:

    def select(
        self,
        molecules: list[Molecule]
    ) -> list[Molecule]:

        unique = {}

        for molecule in molecules:

            unique[
                molecule.smiles
            ] = molecule

        ranked = sorted(

            unique.values(),

            key=lambda m: (
                m.validity_score,
                len(
                    m.latent_vector
                    or []
                )
            ),

            reverse=True

        )

        return ranked
