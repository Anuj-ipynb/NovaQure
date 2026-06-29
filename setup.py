from pathlib import Path


def find_root() -> Path:

    current = Path.cwd().resolve()

    while current != current.parent:

        if (
            (current / "backend").exists()
            and
            (current / "datasets").exists()
        ):
            return current

        current = current.parent

    raise RuntimeError(
        "NovaQure root not found."
    )


ROOT = find_root()

TARGET = (
    ROOT
    / "backend"
    / "generation"
    / "generation_helpers.py"
)


HELPER_CODE = r'''
from __future__ import annotations

import uuid

from backend.contracts.molecule import Molecule

from backend.generation.encoder_service import (
    EncoderService,
)

from backend.generation.selfies_converter import (
    smiles_to_selfies,
)

from backend.generation.smiles_validator import (
    validate_smiles,
)

from backend.sampling.sampling_service import (
    SamplingService,
)


_encoder = EncoderService()

_sampler = SamplingService()


def create_latent(
    selfies_string: str,
) -> list[float]:

    embedding = _encoder.encode(
        selfies_string
    )

    return _sampler.sample(
        embedding
    )


def build_molecule(
    smiles: str,
    source: str,
    latent_vector: list[float],
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
        latent_vector=latent_vector,
        generation_iteration=iteration,
    )


def validate_candidate(
    smiles: str,
    seen: set[str],
) -> bool:

    if not smiles:
        return False

    if not validate_smiles(
        smiles
    ):
        return False

    if smiles in seen:
        return False

    return True


def register_candidate(
    smiles: str,
    seen: set[str],
) -> None:

    seen.add(
        smiles
    )
'''


def write_file():

    TARGET.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    TARGET.write_text(
        HELPER_CODE.strip() + "\n",
        encoding="utf-8",
    )

    print(
        f"UPDATED {TARGET.relative_to(ROOT)}"
    )


if __name__ == "__main__":

    print("=" * 60)
    print("NovaQure Generation G4.3B-1")
    print("=" * 60)

    write_file()

    print()
    print(
        "Generation helper layer installed."
    )