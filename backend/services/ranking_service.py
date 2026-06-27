from __future__ import annotations

from typing import Optional

from backend.models.ranking import Ranking
from backend.repositories.ranking_repository import RankingRepository
from backend.services.base_service import BaseService


class RankingService(
    BaseService[RankingRepository, Ranking]
):
    """
    Ranking Service

    Handles business logic for molecule rankings.

    Responsible for validating ranking data
    before interacting with the repository.
    """

    def __init__(
        self,
        repository: RankingRepository,
    ) -> None:

        super().__init__(repository)

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

        if rank < 1:
            raise ValueError(
                "Rank must be greater than zero."
            )

        if score < 0:
            raise ValueError(
                "Score cannot be negative."
            )

        if not 0 <= confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )

        return self.repository.create_ranking(
            molecule_id=molecule_id,
            rank=rank,
            score=score,
            confidence=confidence,
        )

    # ---------------------------------------------------------
    # Fetch Single Ranking
    # ---------------------------------------------------------

    def get_ranking(
        self,
        ranking_id: str,
    ) -> Optional[Ranking]:

        return self.repository.get_ranking(
            ranking_id
        )

    # ---------------------------------------------------------
    # Fetch All Rankings
    # ---------------------------------------------------------

    def list_rankings(
        self,
    ) -> list[Ranking]:

        return self.repository.list_rankings()

    # ---------------------------------------------------------
    # Rankings For Experiment
    # ---------------------------------------------------------

    def get_experiment_rankings(
        self,
        experiment_id: str,
    ) -> list[Ranking]:

        return self.repository.get_by_experiment(
            experiment_id
        )

    # ---------------------------------------------------------
    # Top Rankings
    # ---------------------------------------------------------

    def top_rankings(
        self,
        limit: int = 10,
    ) -> list[Ranking]:

        if limit < 1:
            limit = 10

        return self.repository.get_top_rankings(
            limit
        )

    # ---------------------------------------------------------
    # Update Ranking
    # ---------------------------------------------------------

    def update_ranking(
        self,
        ranking_id: str,
        rank: int,
        score: float,
        confidence: float,
    ) -> Ranking:

        ranking = self.repository.get_ranking(
            ranking_id
        )

        if ranking is None:
            raise ValueError(
                "Ranking not found."
            )

        if rank < 1:
            raise ValueError(
                "Rank must be greater than zero."
            )

        if score < 0:
            raise ValueError(
                "Score cannot be negative."
            )

        if not 0 <= confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )

        return self.repository.update_ranking(
            ranking,
            rank,
            score,
            confidence,
        )

    # ---------------------------------------------------------
    # Delete Ranking
    # ---------------------------------------------------------

    def delete_ranking(
        self,
        ranking_id: str,
    ) -> bool:

        ranking = self.repository.get_ranking(
            ranking_id
        )

        if ranking is None:
            return False

        self.repository.delete_ranking(
            ranking
        )

        return True

    # ---------------------------------------------------------
    # Count Rankings
    # ---------------------------------------------------------

    def total_rankings(
        self,
    ) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def ranking_exists(
        self,
        ranking_id: str,
    ) -> bool:

        return self.repository.exists(
            ranking_id
        )
