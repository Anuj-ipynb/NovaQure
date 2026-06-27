from __future__ import annotations

from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.models.molecule import Molecule
from backend.repositories.base_repository import BaseRepository


class MoleculeRepository(BaseRepository[Molecule]):
    """
    Repository responsible for all Molecule
    database operations.

    Provides reusable queries required by the
    Service Layer and AI pipeline.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=Molecule,
        )

    # ---------------------------------------------------------
    # Fetch molecule by id
    # ---------------------------------------------------------

    def get_molecule(
        self,
        molecule_id: str,
    ) -> Optional[Molecule]:

        return self.get_by_id(molecule_id)

    # ---------------------------------------------------------
    # Return all molecules
    # ---------------------------------------------------------

    def list_molecules(
        self,
    ) -> list[Molecule]:

        return list(self.get_all())

    # ---------------------------------------------------------
    # Fetch molecules for an experiment
    # ---------------------------------------------------------

    def get_by_experiment(
        self,
        experiment_id: str,
    ) -> list[Molecule]:

        stmt = (
            select(Molecule)
            .where(
                Molecule.experiment_id == experiment_id
            )
            .order_by(
                Molecule.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Search molecules using SMILES string
    # ---------------------------------------------------------

    def search_smiles(
        self,
        smiles: str,
    ) -> list[Molecule]:

        stmt = (
            select(Molecule)
            .where(
                Molecule.smiles.ilike(f"%{smiles}%")
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Get top scoring molecules
    # ---------------------------------------------------------

    def get_top_scoring(
        self,
        limit: int = 10,
    ) -> list[Molecule]:

        stmt = (
            select(Molecule)
            .order_by(
                desc(Molecule.score)
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Create molecule
    # ---------------------------------------------------------

    def create_molecule(
        self,
        experiment_id: str,
        smiles: str,
        selfies: str | None = None,
        score: float = 0.0,
    ) -> Molecule:

        return self.create(
            experiment_id=experiment_id,
            smiles=smiles,
            selfies=selfies,
            score=score,
        )

    # ---------------------------------------------------------
    # Update score
    # ---------------------------------------------------------

    def update_score(
        self,
        molecule: Molecule,
        score: float,
    ) -> Molecule:

        return self.update(
            molecule,
            score=score,
        )

    # ---------------------------------------------------------
    # Delete molecule
    # ---------------------------------------------------------

    def delete_molecule(
        self,
        molecule: Molecule,
    ) -> None:

        self.delete(molecule)
