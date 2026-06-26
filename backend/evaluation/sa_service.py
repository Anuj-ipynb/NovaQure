"""
NovaQure Evaluation Module

Synthetic Accessibility (SA) Service

Computes the Synthetic Accessibility (SA) score for generated
molecules using the official RDKit Contrib implementation
(Ertl & Schuffenhauer algorithm).

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from rdkit import Chem
from rdkit.Chem.rdchem import Mol
from rdkit.Contrib.SA_Score import sascorer

from backend.contracts.molecule import Molecule

logger = logging.getLogger(__name__)


class SAService:
    """
    Service responsible for computing Synthetic Accessibility (SA).

    Responsibilities
    ----------------
    - Validate molecular SMILES
    - Construct RDKit molecule
    - Compute SA score
    - Return explainable synthetic accessibility metric

    Notes
    -----
    Lower SA scores indicate molecules that are easier to synthesize.

    Typical range:
        1.0  -> Very easy
        10.0 -> Very difficult
    """

    @staticmethod
    def _build_rdkit_molecule(smiles: str) -> Mol:
        """
        Convert a SMILES string into an RDKit molecule.

        Parameters
        ----------
        smiles : str
            Canonical SMILES representation.

        Returns
        -------
        Mol
            Parsed RDKit molecule.

        Raises
        ------
        ValueError
            If the supplied SMILES is invalid.
        """

        rdkit_molecule = Chem.MolFromSmiles(smiles)

        if rdkit_molecule is None:
            raise ValueError(f"Invalid SMILES: {smiles}")

        return rdkit_molecule

    def calculate_sa(self, molecule: Molecule) -> float:
        """
        Compute the Synthetic Accessibility (SA) score.

        Parameters
        ----------
        molecule : Molecule
            Molecule contract.

        Returns
        -------
        float
            Synthetic Accessibility score.

        Notes
        -----
        Lower values indicate easier synthesis.

        Raises
        ------
        ValueError
            Invalid SMILES.

        Exception
            Any exception propagated from RDKit Contrib SA scorer.
        """

        logger.info(
            "Starting SA evaluation | molecule_id=%s",
            molecule.molecule_id,
        )

        rdkit_molecule = self._build_rdkit_molecule(
            molecule.smiles
        )

        try:
            sa_score = float(
                sascorer.calculateScore(rdkit_molecule)
            )

        except Exception:
            logger.exception(
                "SA calculation failed | molecule_id=%s",
                molecule.molecule_id,
            )
            raise

        logger.info(
            "Completed SA evaluation | molecule_id=%s | sa=%.4f",
            molecule.molecule_id,
            sa_score,
        )

        return sa_score