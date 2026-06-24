import hashlib
import random
import uuid

import numpy as np
import selfies as sf

from backend.contracts.molecule import Molecule

from backend.generation.smiles_validator import (
    validate_smiles
)

from backend.generation.selfies_converter import (
    smiles_to_selfies,
    selfies_to_smiles
)

from backend.generation.generation_config import (
    GenerationConfig
)


SELFIES_TOKENS = [
    "[C]",
    "[O]",
    "[N]",
    "[F]",
    "[=C]",
    "[Branch1]",
]


def generate_embedding(
    selfies_string: str
) -> list[float]:

    vector = np.zeros(
        GenerationConfig.LATENT_DIM,
        dtype=np.float32
    )

    tokens = list(
        sf.split_selfies(
            selfies_string
        )
    )

    for token in tokens:

        digest = hashlib.sha256(
            token.encode()
        ).digest()

        seed = int.from_bytes(
            digest[:8],
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

    return (
        vector
        .astype(float)
        .tolist()
    )


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

    idx = random.randint(
        0,
        len(tokens) - 1
    )

    tokens[idx] = random.choice(
        SELFIES_TOKENS
    )

    return "".join(tokens)


def build_molecule(
    smiles: str,
    source: str
) -> Molecule:

    selfies_string = (
        smiles_to_selfies(
            smiles
        )
    )

    return Molecule(
        molecule_id=str(
            uuid.uuid4()
        ),
        smiles=smiles,
        selfies=selfies_string,
        source=source,
        validity_score=1.0,
        latent_vector=generate_embedding(
            selfies_string
        ),
    )


def generate_molecules(
    smiles_list: list[str]
) -> list[Molecule]:

    molecules = []

    seen_smiles = set()

    for smiles in smiles_list:

        if not validate_smiles(
            smiles
        ):
            continue

        if smiles in seen_smiles:
            continue

        molecules.append(
            build_molecule(
                smiles,
                "dataset"
            )
        )

        seen_smiles.add(
            smiles
        )

        try:

            selfies_string = (
                smiles_to_selfies(
                    smiles
                )
            )

            for _ in range(
                GenerationConfig
                .MUTATIONS_PER_MOLECULE
            ):

                mutated = mutate_selfies(
                    selfies_string
                )

                mutated_smiles = (
                    selfies_to_smiles(
                        mutated
                    )
                )

                if not validate_smiles(
                    mutated_smiles
                ):
                    continue

                if (
                    mutated_smiles
                    in seen_smiles
                ):
                    continue

                molecules.append(
                    build_molecule(
                        mutated_smiles,
                        "mutation"
                    )
                )

                seen_smiles.add(
                    mutated_smiles
                )

        except Exception:
            continue

    return molecules[
        :GenerationConfig
        .NOVEL_MOLECULE_COUNT
    ]
