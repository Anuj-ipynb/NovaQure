from rdkit import Chem


def validate_smiles(
    smiles: str
) -> bool:

    try:

        mol = Chem.MolFromSmiles(
            smiles
        )

        return mol is not None

    except Exception:
        return False
