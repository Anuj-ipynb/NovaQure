from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db

# ----------------------------------------------------------
# Repositories
# ----------------------------------------------------------

from backend.repositories.project_repository import (
    ProjectRepository,
)
from backend.repositories.experiment_repository import (
    ExperimentRepository,
)
from backend.repositories.molecule_repository import (
    MoleculeRepository,
)
from backend.repositories.ranking_repository import (
    RankingRepository,
)
from backend.repositories.reliability_repository import (
    ReliabilityRepository,
)

# ----------------------------------------------------------
# Services
# ----------------------------------------------------------

from backend.services.project_service import (
    ProjectService,
)
from backend.services.experiment_service import (
    ExperimentService,
)
from backend.services.molecule_service import (
    MoleculeService,
)
from backend.services.ranking_service import (
    RankingService,
)
from backend.services.reliability_service import (
    ReliabilityService,
)

# ----------------------------------------------------------
# Database
# ----------------------------------------------------------


def get_database() -> Generator[
    Session,
    None,
    None,
]:
    """
    Shared database dependency.
    """

    yield from get_db()


# ----------------------------------------------------------
# Project Service
# ----------------------------------------------------------


def get_project_service(
    db: Session = Depends(
        get_database
    ),
) -> ProjectService:

    repository = ProjectRepository(
        db
    )

    return ProjectService(
        repository
    )


# ----------------------------------------------------------
# Experiment Service
# ----------------------------------------------------------


def get_experiment_service(
    db: Session = Depends(
        get_database
    ),
) -> ExperimentService:

    repository = (
        ExperimentRepository(
            db
        )
    )

    return ExperimentService(
        repository
    )


# ----------------------------------------------------------
# Molecule Service
# ----------------------------------------------------------


def get_molecule_service(
    db: Session = Depends(
        get_database
    ),
) -> MoleculeService:

    repository = (
        MoleculeRepository(
            db
        )
    )

    return MoleculeService(
        repository
    )


# ----------------------------------------------------------
# Ranking Service
# ----------------------------------------------------------


def get_ranking_service(
    db: Session = Depends(
        get_database
    ),
) -> RankingService:

    repository = (
        RankingRepository(
            db
        )
    )

    return RankingService(
        repository
    )


# ----------------------------------------------------------
# Reliability Service
# ----------------------------------------------------------


def get_reliability_service(
    db: Session = Depends(
        get_database
    ),
) -> ReliabilityService:

    repository = (
        ReliabilityRepository(
            db
        )
    )

    return ReliabilityService(
        repository
    )
