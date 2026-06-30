from __future__ import annotations

from typing import Optional

from backend.models.reliability import ReliabilityMetric
from backend.repositories.reliability_repository import (
    ReliabilityRepository,
)
from backend.services.base_service import BaseService


class ReliabilityService(
    BaseService[
        ReliabilityRepository,
        ReliabilityMetric,
    ]
):
    """
    Reliability Service

    Handles business logic for the
    Reliability Intelligence Engine.

    Responsible for validating
    reliability metrics before
    interacting with the repository.
    """

    def __init__(
        self,
        repository: ReliabilityRepository,
    ) -> None:

        super().__init__(
            repository
        )

    # ---------------------------------------------------------
    # Create Reliability Snapshot
    # ---------------------------------------------------------

    def create_snapshot(
        self,
        **kwargs,
    ) -> ReliabilityMetric:

        overall_reliability = kwargs.get(
            "overall_reliability",
            0.0,
        )

        ai_confidence = kwargs.get(
            "ai_confidence",
            0.0,
        )

        quantum_noise = kwargs.get(
            "quantum_noise",
            0.0,
        )

        if not 0 <= overall_reliability <= 100:
            raise ValueError(
                "Overall reliability must be between 0 and 100."
            )

        if not 0 <= ai_confidence <= 100:
            raise ValueError(
                "AI confidence must be between 0 and 100."
            )

        if not 0 <= quantum_noise <= 100:
            raise ValueError(
                "Quantum noise must be between 0 and 100."
            )

        return self.repository.create_snapshot(
            **kwargs
        )

    # ---------------------------------------------------------
    # Fetch Snapshot By Id
    # ---------------------------------------------------------

    def get_snapshot(
        self,
        reliability_id: str,
    ) -> Optional[ReliabilityMetric]:

        return self.repository.get_reliability(
            reliability_id
        )

    # ---------------------------------------------------------
    # Fetch Latest Snapshot
    # ---------------------------------------------------------

    def latest_snapshot(
        self,
    ) -> Optional[ReliabilityMetric]:

        return self.repository.get_latest_snapshot()

    # ---------------------------------------------------------
    # Fetch All Snapshots
    # ---------------------------------------------------------

    def list_snapshots(
        self,
    ) -> list[ReliabilityMetric]:

        return (
            self.repository
            .list_reliability_metrics()
        )

    # ---------------------------------------------------------
    # Update Snapshot
    # ---------------------------------------------------------

    def update_snapshot(
        self,
        reliability_id: str,
        **kwargs,
    ) -> ReliabilityMetric:

        reliability = (
            self.repository
            .get_reliability(
                reliability_id
            )
        )

        if reliability is None:
            raise ValueError(
                "Reliability snapshot not found."
            )

        return (
            self.repository
            .update_snapshot(
                reliability,
                **kwargs,
            )
        )

    # ---------------------------------------------------------
    # Delete Snapshot
    # ---------------------------------------------------------

    def delete_snapshot(
        self,
        reliability_id: str,
    ) -> bool:

        reliability = (
            self.repository
            .get_reliability(
                reliability_id
            )
        )

        if reliability is None:
            return False

        self.repository.delete_snapshot(
            reliability
        )

        return True

    # ---------------------------------------------------------
    # Count Snapshots
    # ---------------------------------------------------------

    def total_snapshots(
        self,
    ) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def snapshot_exists(
        self,
        reliability_id: str,
    ) -> bool:

        return self.repository.exists(
            reliability_id
        )
