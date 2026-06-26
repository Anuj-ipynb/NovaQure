"""
NovaQure Evaluation Module

QED Service

Computes the Quantitative Estimate of Drug-likeness (QED)
for a generated molecule using RDKit.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from rdkit import Chem
from rdkit.Chem import QED

from backend.contracts.molecule import Molecule

logger = logging.getLogger(__name__)


class QEDService:
    """
    Computes RDKit QED scores.

    Responsibilities
    ----------------
    - Validate SMILES
    - Parse RDKit molecule
    - Compute QED
    - Return explainable score

    This service is stateless.
    """

    def calculate_qed(self, molecule: Molecule) -> float:
        """
        Calculate the RDKit QED score.

        Parameters
        ----------
        molecule:
            Molecule contract.

        Returns
        -------
        float
            QED score between 0 and 1.

        Raises
        ------
        ValueError
            Invalid SMILES.
        RuntimeError
            RDKit computation failure.
        """

        logger.info(
            "Starting QED evaluation for molecule_id=%s",
            molecule.molecule_id,
        )

        rdkit_molecule = Chem.MolFromSmiles(molecule.smiles)

        if rdkit_molecule is None:
            logger.error(
                "Invalid SMILES for molecule_id=%s",
                molecule.molecule_id,
            )

            raise ValueError(
                f"Invalid SMILES: {molecule.smiles}"
            )

        try:

            score = float(QED.qed(rdkit_molecule))

        except Exception as exc:

            logger.exception(
                "RDKit QED calculation failed for molecule_id=%s",
                molecule.molecule_id,
            )

            raise RuntimeError(
                "QED calculation failed."
            ) from exc

        logger.info(
            "Finished QED evaluation for molecule_id=%s score=%.4f",
            molecule.molecule_id,
            score,
        )

        return score