from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.experiment import Experiment
from backend.repositories.base_repository import BaseRepository


class ExperimentRepository(BaseRepository[Experiment]):
    """
    Repository responsible for all Experiment
    database operations.

    Contains reusable queries required by the
    Service Layer.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=Experiment,
        )

    # ---------------------------------------------------------
    # Fetch experiment by id
    # ---------------------------------------------------------

    def get_experiment(
        self,
        experiment_id: str,
    ) -> Optional[Experiment]:

        return self.get_by_id(experiment_id)

    # ---------------------------------------------------------
    # Return every experiment
    # ---------------------------------------------------------

    def list_experiments(
        self,
    ) -> list[Experiment]:

        return list(self.get_all())

    # ---------------------------------------------------------
    # Fetch all experiments for a project
    # ---------------------------------------------------------

    def get_by_project(
        self,
        project_id: str,
    ) -> list[Experiment]:

        stmt = (
            select(Experiment)
            .where(
                Experiment.project_id == project_id
            )
            .order_by(
                Experiment.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Fetch experiments by status
    # ---------------------------------------------------------

    def get_by_status(
        self,
        status: str,
    ) -> list[Experiment]:

        stmt = (
            select(Experiment)
            .where(
                Experiment.status == status
            )
            .order_by(
                Experiment.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # ---------------------------------------------------------
    # Create Experiment
    # ---------------------------------------------------------

    def create_experiment(
        self,
        project_id: str,
        target_protein: str,
        iterations: int,
    ) -> Experiment:

        return self.create(
            project_id=project_id,
            target_protein=target_protein,
            iterations=iterations,
            status="queued",
        )

    # ---------------------------------------------------------
    # Update Experiment Status
    # ---------------------------------------------------------

    def update_status(
        self,
        experiment: Experiment,
        status: str,
    ) -> Experiment:

        return self.update(
            experiment,
            status=status,
        )

    # ---------------------------------------------------------
    # Delete Experiment
    # ---------------------------------------------------------

    def delete_experiment(
        self,
        experiment: Experiment,
    ) -> None:

        self.delete(experiment)
