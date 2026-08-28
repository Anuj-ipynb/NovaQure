from __future__ import annotations

from typing import Optional

from backend.models.experiment import Experiment
from backend.repositories.experiment_repository import ExperimentRepository
from backend.services.base_service import BaseService


class ExperimentService(
    BaseService[ExperimentRepository, Experiment]
):
    """
    Experiment Service

    Responsible for all experiment-related
    business logic.

    The service layer validates requests,
    applies business rules and delegates
    persistence to the repository layer.
    """

    VALID_STATUSES = {
        "queued",
        "running",
        "completed",
        "failed",
        "cancelled",
    }

    def __init__(
        self,
        repository: ExperimentRepository,
    ) -> None:

        super().__init__(repository)

    # ---------------------------------------------------------
    # Create Experiment
    # ---------------------------------------------------------

    def create_experiment(
        self,
        project_id: str,
        target_protein: str,
        iterations: int,
    ) -> Experiment:

        target_protein = target_protein.strip().upper()

        if not target_protein:
            raise ValueError(
                "Target protein cannot be empty."
            )

        if iterations < 1:
            raise ValueError(
                "Iterations must be greater than zero."
            )

        return self.repository.create_experiment(
            project_id=project_id,
            target_protein=target_protein,
            iterations=iterations,
        )

    # ---------------------------------------------------------
    # Fetch Single Experiment
    # ---------------------------------------------------------

    def get_experiment(
        self,
        experiment_id: str,
    ) -> Optional[Experiment]:

        return self.repository.get_experiment(
            experiment_id
        )

    # ---------------------------------------------------------
    # Fetch All Experiments
    # ---------------------------------------------------------

    def list_experiments(
        self,
    ) -> list[Experiment]:

        return self.repository.list_experiments()

    # ---------------------------------------------------------
    # Fetch Experiments For Project
    # ---------------------------------------------------------

    def get_project_experiments(
        self,
        project_id: str,
    ) -> list[Experiment]:

        return self.repository.get_by_project(
            project_id
        )

    # ---------------------------------------------------------
    # Fetch Experiments By Status
    # ---------------------------------------------------------

    def get_by_status(
        self,
        status: str,
    ) -> list[Experiment]:

        status = status.lower()

        if status not in self.VALID_STATUSES:
            return []

        return self.repository.get_by_status(
            status
        )

    # ---------------------------------------------------------
    # Update Experiment Status
    # ---------------------------------------------------------

    def update_status(
        self,
        experiment_id: str,
        status: str,
    ) -> Experiment:

        status = status.lower()

        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid experiment status: {status}"
            )

        experiment = self.repository.get_experiment(
            experiment_id
        )

        if experiment is None:
            raise ValueError(
                "Experiment not found."
            )

        return self.repository.update_status(
            experiment,
            status,
        )

    # ---------------------------------------------------------
    # Delete Experiment
    # ---------------------------------------------------------

    def delete_experiment(
        self,
        experiment_id: str,
    ) -> bool:

        experiment = self.repository.get_experiment(
            experiment_id
        )

        if experiment is None:
            return False

        self.repository.delete_experiment(
            experiment
        )

        return True

    # ---------------------------------------------------------
    # Count Experiments
    # ---------------------------------------------------------

    def total_experiments(
        self,
    ) -> int:

        return self.repository.count()

    # ---------------------------------------------------------
    # Check Existence
    # ---------------------------------------------------------

    def experiment_exists(
        self,
        experiment_id: str,
    ) -> bool:

        return self.repository.exists(
            experiment_id
        )
