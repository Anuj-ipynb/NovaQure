import uuid

from backend.contracts.molecule import Molecule

from backend.generation.smiles_validator import (
    validate_smiles
)

from backend.generation.selfies_converter import (
    smiles_to_selfies
)


def generate_molecules(
    smiles_list: list[str]
) -> list[Molecule]:

    molecules = []

    for smiles in smiles_list:

        if not validate_smiles(
            smiles
        ):
            continue

        molecules.append(
            Molecule(
                molecule_id=str(
                    uuid.uuid4()
                ),
                smiles=smiles,
                selfies=smiles_to_selfies(
                    smiles
                ),
                source="dataset",
                validity_score=1.0,
                latent_vector=None
            )
        )

    return molecules
