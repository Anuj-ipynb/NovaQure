from __future__ import annotations

from rdkit import Chem
from rdkit.Chem.rdFingerprintGenerator import (
    GetMorganGenerator,
)
from rdkit.DataStructs import (
    TanimotoSimilarity,
)
from rdkit.DataStructs.cDataStructs import (
    ExplicitBitVect,
)


FINGERPRINT_RADIUS = 2
FINGERPRINT_SIZE = 2048


_MORGAN_GENERATOR = GetMorganGenerator(
    radius=FINGERPRINT_RADIUS,
    fpSize=FINGERPRINT_SIZE,
)


def smiles_to_mol(
    smiles: str,
):
    """
    Convert a SMILES string into an RDKit molecule.
    """

    mol = Chem.MolFromSmiles(
        smiles
    )

    if mol is None:

        raise ValueError(
            f"Invalid SMILES: {smiles}"
        )

    return mol


def generate_fingerprint(
    smiles: str,
) -> ExplicitBitVect:
    """
    Generate a Morgan fingerprint using RDKit's
    modern MorganGenerator API.
    """

    mol = smiles_to_mol(
        smiles
    )

    return _MORGAN_GENERATOR.GetFingerprint(
        mol
    )


def tanimoto_similarity(
    fp1: ExplicitBitVect,
    fp2: ExplicitBitVect,
) -> float:
    """
    Compute the Tanimoto similarity between two fingerprints.
    """

    return float(
        TanimotoSimilarity(
            fp1,
            fp2,
        )
    )


def molecule_similarity(
    smiles_a: str,
    smiles_b: str,
) -> float:
    """
    Compute the Tanimoto similarity between two molecules.
    """

    fp_a = generate_fingerprint(
        smiles_a
    )

    fp_b = generate_fingerprint(
        smiles_b
    )

    return tanimoto_similarity(
        fp_a,
        fp_b,
    )