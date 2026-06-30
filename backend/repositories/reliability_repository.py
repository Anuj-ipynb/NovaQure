from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.reliability import ReliabilityMetric
from backend.repositories.base_repository import BaseRepository


class ReliabilityRepository(
    BaseRepository[ReliabilityMetric]
):
    """
    Repository responsible for all
    Reliability Engine database operations.

    Provides reusable reliability queries
    used by monitoring, dashboard and
    explainability modules.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=ReliabilityMetric,
        )

    # ---------------------------------------------------------
    # Fetch reliability snapshot by id
    # ---------------------------------------------------------

    def get_reliability(
        self,
        reliability_id: str,
    ) -> Optional[ReliabilityMetric]:

        return self.get_by_id(
            reliability_id
        )

    # ---------------------------------------------------------
    # Return every reliability snapshot
    # ---------------------------------------------------------

    def list_reliability_metrics(
        self,
    ) -> list[ReliabilityMetric]:

        return list(
            self.get_all()
        )

    # ---------------------------------------------------------
    # Return latest reliability snapshot
    # ---------------------------------------------------------

    def get_latest_snapshot(
        self,
    ) -> Optional[ReliabilityMetric]:

        stmt = (
            select(
                ReliabilityMetric
            )
            .order_by(
                ReliabilityMetric.created_at.desc()
            )
            .limit(1)
        )

        return self.db.scalar(
            stmt
        )

    # ---------------------------------------------------------
    # Create reliability snapshot
    # ---------------------------------------------------------

    def create_snapshot(
        self,
        **kwargs,
    ) -> ReliabilityMetric:

        return self.create(
            **kwargs
        )

    # ---------------------------------------------------------
    # Update reliability snapshot
    # ---------------------------------------------------------

    def update_snapshot(
        self,
        reliability: ReliabilityMetric,
        **kwargs,
    ) -> ReliabilityMetric:

        return self.update(
            reliability,
            **kwargs,
        )

    # ---------------------------------------------------------
    # Delete reliability snapshot
    # ---------------------------------------------------------

    def delete_snapshot(
        self,
        reliability: ReliabilityMetric,
    ) -> None:

        self.delete(
            reliability
        )
