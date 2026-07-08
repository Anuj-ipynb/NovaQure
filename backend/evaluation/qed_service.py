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

    def calculate_qed(self, smiles: str) -> float:
        """
        Compute the Quantitative Estimate of Drug-likeness (QED).

        Parameters
        ----------
        smiles : str
            Canonical SMILES representation.

        Returns
        -------
        float
            QED score in the range [0, 1].
        """
        logger.info(
            "Starting QED evaluation | smiles=%s",
            smiles,
        )

        rdkit_molecule = self._build_rdkit_molecule(smiles)

        try:
            qed_score = float(QED.qed(rdkit_molecule))

        except Exception:
            logger.exception(
                "RDKit QED calculation failed | smiles=%s",
                smiles,
            )
            raise

        logger.info(
            "Completed QED evaluation | smiles=%s | qed=%.4f",
            smiles,
            qed_score,
        )

        return qed_score

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify the QED service is operational.
        """
        try:
            self._build_rdkit_molecule("CCO")
            return True
        except Exception:
            return False

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self) -> "QEDService":
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> bool:
        # Returning False ensures exception bubbles are not swallowed
        return False