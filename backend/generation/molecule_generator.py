import hashlib
import random
import uuid

import numpy as np
import selfies as sf

from backend.contracts.molecule import Molecule

from backend.generation.generation_config import (
    GenerationConfig
)

from backend.generation.selfies_converter import (
    smiles_to_selfies,
    selfies_to_smiles
)

from backend.generation.smiles_validator import (
    validate_smiles
)

from backend.sampling.sampling_service import (
    SamplingService
)


SELFIES_TOKENS = [
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
    "[Branch1]",
]


_sampler = SamplingService()


def generate_embedding(
    selfies_string: str
) -> list[float]:

    vector = np.zeros(
        GenerationConfig.LATENT_DIM,
        dtype=np.float32
    )

    for token in sf.split_selfies(
        selfies_string
    ):

        seed = int.from_bytes(
            hashlib.sha256(
                token.encode()
            ).digest()[:8],
            "big"
        )

        rng = np.random.default_rng(
            seed
        )

        vector += rng.normal(
            0,
            1,
            GenerationConfig.LATENT_DIM
        )

    norm = np.linalg.norm(
        vector
    )

    if norm > 0:
        vector /= norm

    return vector.astype(float).tolist()


def mutate_selfies(
    selfies_string: str
) -> str:

    tokens = list(
        sf.split_selfies(
            selfies_string
        )
    )

    if not tokens:
        return selfies_string

    index = random.randrange(
        len(tokens)
    )

    tokens[index] = random.choice(
        SELFIES_TOKENS
    )

    return "".join(tokens)


def build_molecule(
    smiles: str,
    source: str,
    latent: list[float],
    iteration: int
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
    smiles_list: list[str]
) -> list[Molecule]:

    molecules = []

    seen = set()

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

        embedding = generate_embedding(
            selfies_string
        )

        sampled = _sampler.sample(
            embedding
        )

        molecules.append(
            build_molecule(
                smiles,
                "dataset",
                sampled,
                0
            )
        )

        seen.add(smiles)

        for iteration in range(
            1,
            GenerationConfig.MUTATIONS_PER_MOLECULE + 1
        ):

            try:

                mutated_selfies = (
                    mutate_selfies(
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

                sampled = _sampler.sample(
                    generate_embedding(
                        mutated_selfies
                    )
                )

                molecules.append(
                    build_molecule(
                        mutated_smiles,
                        "mutation",
                        sampled,
                        iteration
                    )
                )

                seen.add(
                    mutated_smiles
                )

            except Exception:
                continue

    return molecules[
        :GenerationConfig.NOVEL_MOLECULE_COUNT
    ]
