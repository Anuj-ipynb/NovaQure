from rdkit import Chem


def canonicalize_smiles(
    smiles: str
) -> str:

    mol = Chem.MolFromSmiles(
        smiles
    )

    if mol is None:
        raise ValueError(
            f"Invalid smiles: {smiles}"
        )

    return Chem.MolToSmiles(
        mol,
        canonical=True
    )


def remove_duplicates(
    smiles_list: list[str]
) -> list[str]:

    return list(
        dict.fromkeys(
            smiles_list
        )
    )
