from __future__ import annotations

from collections import Counter

from backend.contracts.molecule import Molecule

from backend.sampling.diversity import (
    DiversityCalculator
)


class GenerationReport:

    @staticmethod
    def build(
        molecules: list[Molecule]
    ) -> dict:

        vectors = [

            molecule.latent_vector

            for molecule in molecules

            if molecule.latent_vector

        ]

        sources = Counter(

            molecule.source

            for molecule in molecules

        )

        unique_smiles = len(

            {

                molecule.smiles

                for molecule in molecules

            }

        )

        report = {

            "total_molecules":
            len(
                molecules
            ),

            "unique_smiles":
            unique_smiles,

            "duplicate_molecules":
            len(
                molecules
            ) - unique_smiles,

            "dataset_molecules":
            sources.get(
                "dataset",
                0
            ),

            "mutation_molecules":
            sources.get(
                "mutation",
                0
            ),

            "average_validity":

            round(

                sum(
                    molecule.validity_score
                    for molecule in molecules
                )
                /
                max(
                    len(molecules),
                    1
                ),

                4

            ),

            "average_diversity":

            round(

                DiversityCalculator.average_diversity(
                    vectors
                ),

                4

            ),
            "sampling_strategy": "qcbm",
                "latent_dimension": len(vectors[0]) if vectors else 0,
            "generation_version": "3.5",

        }

        return report
