from __future__ import annotations

from typing import Optional

from backend.models.molecule import Molecule
from backend.repositories.molecule_repository import MoleculeRepository
from backend.services.base_service import BaseService


class MoleculeService(
    BaseService[MoleculeRepository, Molecule]
):
    """
    Molecule Service

    Handles all molecule-related
    business logic.

    This service validates molecule
    information before interacting with
    the repository layer.
    """

    def __init__(
        self,
        repository: MoleculeRepository,
    ) -> None:

        super().__init__(repository)

    # ---------------------------------------------------------
    # Create Molecule
    # ---------------------------------------------------------

    def create_molecule(
        self,
        experiment_id: str,
        smiles: str,
        selfies: str | None = None,
        score: float = 0.0,
    ) -> Molecule:

        smiles = smiles.strip()

        if not smiles:
            raise ValueError(
                "SMILES string cannot be empty."
            )

        if score < 0:
            raise ValueError(
                "Score cannot be negative."
            )

        return self.repository.create_molecule(
            experiment_id=experiment_id,
            smiles=smiles,
            selfies=selfies,
            score=score,
        )

    # ---------------------------------------------------------
    # Fetch Single Molecule
    # ---------------------------------------------------------

    def get_molecule(
        self,
        molecule_id: str,
    ) -> Optional[Molecule]:

        return self.repository.get_molecule(
            molecule_id
        )

    # ---------------------------------------------------------
    # Fetch All Molecules
    # ---------------------------------------------------------

    def list_molecules(
        self,
    ) -> list[Molecule]:

        return self.repository.list_molecules()

    # ---------------------------------------------------------
    # Fetch Molecules For Experiment
    # ---------------------------------------------------------

    def get_experiment_molecules(
        self,
        experiment_id: str,
    ) -> list[Molecule]:

        return self.repository.get_by_experiment(
            experiment_id
        )

    # ---------------------------------------------------------
    # Search Molecules
    # ---------------------------------------------------------

    def search_molecules(
        self,
        smiles: str,
    ) -> list[Molecule]:

        smiles = smiles.strip()

        if not smiles:
            return []

        return self.repository.search_smiles(
            smiles
        )

    # ---------------------------------------------------------
    # Get Top Scoring Molecules
    # ---------------------------------------------------------

    def top_molecules(
        self,
        limit: int = 10,
    ) -> list[Molecule]:

        if limit < 1:
            limit = 10

        return self.repository.get_top_scoring(
            limit
        )

    # ---------------------------------------------------------
    # Update Molecule Score
    # ---------------------------------------------------------

    def update_score(
        self,
        molecule_id: str,
        score: float,
    ) -> Molecule:

        if score < 0:
            raise ValueError(
                "Score cannot be negative."
            )

        molecule = self.repository.get_molecule(
            molecule_id
        )

        if molecule is None:
            raise ValueError(
                "Molecule not found."
            )

        return self.repository.update_score(
            molecule,
            score,
        )

    # ---------------------------------------------------------
    # Delete Molecule
    # ---------------------------------------------------------

    def delete_molecule(
        self,
        molecule_id: str,
    ) -> bool:

        molecule = self.repository.get_molecule(
            molecule_id
        )

        if molecule is None:
            return False

        self.repository.delete_molecule(
            molecule
        )

        return True

    # ---------------------------------------------------------
    # Count Molecules
    # ---------------------------------------------------------

    def total_molecules(
        self,
    ) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Check Existence
    # ---------------------------------------------------------

    def molecule_exists(
        self,
        molecule_id: str,
    ) -> bool:

        return self.repository.exists(
            molecule_id
        )
