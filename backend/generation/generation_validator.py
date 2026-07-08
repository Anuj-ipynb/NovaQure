from backend.contracts.molecule import (
    Molecule
)


class GenerationValidator:

    REQUIRED_VECTOR_LENGTH = 128

    @classmethod
    def validate(
        cls,
        molecules: list[Molecule]
    ) -> None:

        if not molecules:

            raise ValueError(
                "No molecules generated."
            )

        ids = set()

        for molecule in molecules:

            if molecule.molecule_id in ids:

                raise ValueError(
                    "Duplicate molecule_id."
                )

            ids.add(
                molecule.molecule_id
            )

            if not molecule.smiles:

                raise ValueError(
                    "Missing SMILES."
                )

            if not molecule.selfies:

                raise ValueError(
                    "Missing SELFIES."
                )

            if molecule.latent_vector is None:

                raise ValueError(
                    "Missing latent vector."
                )

            if len(
                molecule.latent_vector
            ) != cls.REQUIRED_VECTOR_LENGTH:

                raise ValueError(
                    "Invalid latent dimension."
                )

            if molecule.source not in (

                "dataset",

                "mutation"

            ):

                raise ValueError(
                    "Invalid source."
                )
