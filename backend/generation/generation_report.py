from __future__ import annotations

from collections import Counter

import numpy as np

from backend.contracts.molecule import Molecule

from backend.sampling.diversity import (
    DiversityCalculator,
)


class GenerationReport:

    @staticmethod
    def build(
        molecules: list[Molecule],
        execution_time: float,
    ) -> dict:

        total = len(
            molecules
        )

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

        average_validity = (

            sum(

                molecule.validity_score

                for molecule in molecules

            )

            /

            max(
                total,
                1,
            )

        )

        validity_rate = (

            sum(

                molecule.validity_score > 0

                for molecule in molecules

            )

            /

            max(
                total,
                1,
            )

        )

        uniqueness_rate = (

            unique_smiles

            /

            max(
                total,
                1,
            )

        )

        average_diversity = (

            DiversityCalculator.average_diversity(
                vectors
            )

        )

        latent_norms = [

            np.linalg.norm(
                vector
            )

            for vector in vectors

        ]

        average_latent_norm = (

            float(
                np.mean(
                    latent_norms
                )
            )

            if latent_norms

            else 0.0

        )

        throughput = (

            total

            /

            execution_time

            if execution_time > 0

            else 0.0

        )

        return {

            "generation": {

                "total_molecules":
                total,

                "dataset_molecules":
                sources.get(
                    "dataset",
                    0,
                ),

                "mutation_molecules":
                sources.get(
                    "mutation",
                    0,
                ),

                "unique_smiles":
                unique_smiles,

                "duplicate_molecules":
                total
                - unique_smiles,

            },

            "quality": {

                "average_validity":
                round(
                    average_validity,
                    4,
                ),

                "validity_rate":
                round(
                    validity_rate,
                    4,
                ),

                "uniqueness_rate":
                round(
                    uniqueness_rate,
                    4,
                ),

                "average_diversity":
                round(
                    average_diversity,
                    4,
                ),

            },

            "latent_space": {

                "latent_dimension":
                len(
                    vectors[0]
                )

                if vectors

                else 0,

                "average_latent_norm":
                round(
                    average_latent_norm,
                    4,
                ),

            },

            "performance": {

                "execution_time_seconds":
                round(
                    execution_time,
                    4,
                ),

                "throughput_molecules_per_second":
                round(
                    throughput,
                    2,
                ),

            },

        }