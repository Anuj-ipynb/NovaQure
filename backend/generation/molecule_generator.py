from __future__ import annotations

import uuid

from backend.contracts.molecule import Molecule

from backend.generation.encoder_service import (
    EncoderService,
)

from backend.generation.generation_config import (
    GenerationConfig,
)

from backend.generation.mutation_engine import (
    MutationEngine,
)

from backend.generation.selfies_converter import (
    smiles_to_selfies,
    selfies_to_smiles,
)

from backend.generation.smiles_validator import (
    validate_smiles,
)

from backend.sampling.sampling_service import (
    SamplingService,
)


_sampler = SamplingService()

_encoder = EncoderService()

_mutation_engine = MutationEngine()


def build_molecule(
    smiles: str,
    source: str,
    latent: list[float],
    iteration: int,
) -> Molecule:

    return Molecule(
        molecule_id=str(
            uuid.uuid4()
        ),
        smiles=smiles,
        selfies=smiles_to_selfies(
            smiles
        ),
        source=source,
        validity_score=1.0,
        latent_vector=latent,
        generation_iteration=iteration,
    )


def generate_molecules(
    smiles_list: list[str],
) -> list[Molecule]:

    molecules: list[Molecule] = []

    seen: set[str] = set()

    for smiles in smiles_list:

        if not validate_smiles(
            smiles
        ):
            continue

        if smiles in seen:
            continue

        selfies_string = (
            smiles_to_selfies(
                smiles
            )
        )

        embedding = _encoder.encode(
            selfies_string
        )

        sampled = _sampler.sample(
            embedding
        )

        molecules.append(
            build_molecule(
                smiles=smiles,
                source="dataset",
                latent=sampled,
                iteration=0,
            )
        )

        seen.add(
            smiles
        )

        for iteration in range(
            1,
            GenerationConfig.MUTATIONS_PER_MOLECULE + 1,
        ):

            mutation_created = False

            for _ in range(
                GenerationConfig.MUTATION_MAX_RETRIES
            ):

                try:

                    mutated_selfies = (
                        _mutation_engine.mutate(
                            selfies_string
                        )
                    )

                    mutated_smiles = (
                        selfies_to_smiles(
                            mutated_selfies
                        )
                    )

                    if not validate_smiles(
                        mutated_smiles
                    ):
                        continue

                    if mutated_smiles in seen:
                        continue

                    embedding = _encoder.encode(
                        mutated_selfies
                    )

                    sampled = _sampler.sample(
                        embedding
                    )

                    molecules.append(
                        build_molecule(
                            smiles=mutated_smiles,
                            source="mutation",
                            latent=sampled,
                            iteration=iteration,
                        )
                    )

                    seen.add(
                        mutated_smiles
                    )

                    mutation_created = True

                    break

                except Exception:
                    continue

            if not mutation_created:
                continue

    return molecules[
        :GenerationConfig.NOVEL_MOLECULE_COUNT
    ]