"""
NovaQure Evaluation Module

QED Service

Computes the Quantitative Estimate of Drug-likeness (QED)
for generated molecules using RDKit.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from rdkit import Chem
from rdkit.Chem import QED
from rdkit.Chem.rdchem import Mol

from backend.contracts.molecule import Molecule

logger = logging.getLogger(__name__)


class QEDService:
    """
    Service responsible for computing RDKit QED scores.

    Responsibilities
    ----------------
    - Validate molecular SMILES
    - Construct RDKit molecule
    - Compute QED score
    - Return explainable drug-likeness metric

    This service is stateless and thread-safe.
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

    def calculate_qed(self, molecule: Molecule) -> float:
        """
        Compute the Quantitative Estimate of Drug-likeness (QED).

        Parameters
        ----------
        molecule : Molecule
            Molecule contract.

        Returns
        -------
        float
            QED score in the range [0, 1].
        """

        logger.info(
            "Starting QED evaluation | molecule_id=%s",
            molecule.molecule_id,
        )

        rdkit_molecule = self._build_rdkit_molecule(
            molecule.smiles
        )

        try:
            qed_score = float(QED.qed(rdkit_molecule))

        except Exception:
            logger.exception(
                "RDKit QED calculation failed | molecule_id=%s",
                molecule.molecule_id,
            )
            raise

        logger.info(
            "Completed QED evaluation | molecule_id=%s | qed=%.4f",
            molecule.molecule_id,
            qed_score,
        )

        return qed_score