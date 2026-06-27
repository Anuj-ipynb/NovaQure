from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.ranking import Ranking
from backend.models.molecule import Molecule
from backend.repositories.base_repository import BaseRepository


class RankingRepository(BaseRepository[Ranking]):
    """
    Repository responsible for all Ranking
    database operations.

    Provides reusable ranking queries used by
    the optimization and dashboard modules.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=Ranking,
        )

    # ---------------------------------------------------------
    # Fetch ranking by id
    # ---------------------------------------------------------

    def get_ranking(
        self,
        ranking_id: str,
    ) -> Optional[Ranking]:

        return self.get_by_id(ranking_id)

    # ---------------------------------------------------------
    # Return every ranking
    # ---------------------------------------------------------

    def list_rankings(
        self,
    ) -> list[Ranking]:

        return list(self.get_all())

    # ---------------------------------------------------------
    # Fetch rankings belonging to an experiment
    # ---------------------------------------------------------

    def get_by_experiment(
        self,
        experiment_id: str,
    ) -> list[Ranking]:

        stmt = (
            select(Ranking)
            .join(Molecule)
            .where(
                Molecule.experiment_id == experiment_id
            )
            .order_by(
                Ranking.rank.asc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Return Top Ranked Molecules
    # ---------------------------------------------------------

    def get_top_rankings(
        self,
        limit: int = 10,
    ) -> list[Ranking]:

        stmt = (
            select(Ranking)
            .order_by(
                Ranking.rank.asc()
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Create Ranking
    # ---------------------------------------------------------

    def create_ranking(
        self,
        molecule_id: str,
        rank: int,
        score: float,
        confidence: float,
    ) -> Ranking:

        return self.create(
            molecule_id=molecule_id,
            rank=rank,
            score=score,
            confidence=confidence,
        )

    # ---------------------------------------------------------
    # Update Ranking
    # ---------------------------------------------------------

    def update_ranking(
        self,
        ranking: Ranking,
        rank: int,
        score: float,
        confidence: float,
    ) -> Ranking:

        return self.update(
            ranking,
            rank=rank,
            score=score,
            confidence=confidence,
        )

    # ---------------------------------------------------------
    # Delete Ranking
    # ---------------------------------------------------------

    def delete_ranking(
        self,
        ranking: Ranking,
    ) -> None:

        self.delete(ranking)
