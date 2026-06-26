"""
NovaQure Evaluation Module

Lipinski Service

Evaluates Lipinski's Rule of Five using RDKit.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging

from rdkit import Chem
from rdkit.Chem import Crippen
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem.rdchem import Mol

from backend.contracts.molecule import Molecule

logger = logging.getLogger(__name__)


class LipinskiService:
    """
    Service responsible for evaluating Lipinski's Rule of Five.

    Responsibilities
    ----------------
    - Validate molecular SMILES
    - Compute Rule of Five descriptors
    - Determine pass/fail status

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

    def evaluate(self, molecule: Molecule) -> bool:
        """
        Evaluate Lipinski's Rule of Five.

        Parameters
        ----------
        molecule : Molecule
            Molecule contract.

        Returns
        -------
        bool
            True if all Lipinski rules are satisfied.
        """

        logger.info(
            "Starting Lipinski evaluation | molecule_id=%s",
            molecule.molecule_id,
        )

        rdkit_molecule = self._build_rdkit_molecule(
            molecule.smiles
        )

        try:

            molecular_weight = Descriptors.MolWt(rdkit_molecule)
            logp = Crippen.MolLogP(rdkit_molecule)
            hydrogen_donors = Lipinski.NumHDonors(rdkit_molecule)
            hydrogen_acceptors = Lipinski.NumHAcceptors(rdkit_molecule)

        except Exception:
            logger.exception(
                "Lipinski calculation failed | molecule_id=%s",
                molecule.molecule_id,
            )
            raise

        lipinski_pass = (
            molecular_weight <= 500
            and logp <= 5
            and hydrogen_donors <= 5
            and hydrogen_acceptors <= 10
        )

        logger.info(
            (
                "Completed Lipinski evaluation | "
                "molecule_id=%s | "
                "mw=%.2f | "
                "logp=%.2f | "
                "hbd=%d | "
                "hba=%d | "
                "pass=%s"
            ),
            molecule.molecule_id,
            molecular_weight,
            logp,
            hydrogen_donors,
            hydrogen_acceptors,
            lipinski_pass,
        )

        return lipinski_pass