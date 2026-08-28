from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import get_experiment_service
from backend.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentUpdate,
)
from backend.services.experiment_service import ExperimentService


router = APIRouter(
    prefix="/experiments",
    tags=["Experiments"],
)


# ---------------------------------------------------------
# Create Experiment
# ---------------------------------------------------------


@router.post(
    "",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(
    experiment: ExperimentCreate,
    service: Annotated[
        ExperimentService,
        Depends(get_experiment_service),
    ],
):

    try:

        created = service.create_experiment(
            project_id=experiment.project_id,
            target_protein=experiment.target_protein,
            iterations=experiment.iterations,
        )

        return created

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Experiments
# ---------------------------------------------------------


@router.get(
    "",
    response_model=list[ExperimentResponse],
)
def list_experiments(
    service: Annotated[
        ExperimentService,
        Depends(get_experiment_service),
    ],
):

    return service.list_experiments()


# ---------------------------------------------------------
# Get Experiment
# ---------------------------------------------------------


@router.get(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(
    experiment_id: str,
    service: Annotated[
        ExperimentService,
        Depends(get_experiment_service),
    ],
):

    experiment = service.get_experiment(
        experiment_id
    )

    if experiment is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found.",
        )

    return experiment


# ---------------------------------------------------------
# Update Status
# ---------------------------------------------------------


@router.patch(
    "/{experiment_id}/status",
    response_model=ExperimentResponse,
)
def update_status(
    experiment_id: str,
    update: ExperimentUpdate,
    service: Annotated[
        ExperimentService,
        Depends(get_experiment_service),
    ],
):

    if update.status is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required.",
        )

    try:

        return service.update_status(
            experiment_id,
            update.status,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Delete Experiment
# ---------------------------------------------------------


@router.delete(
    "/{experiment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experiment(
    experiment_id: str,
    service: Annotated[
        ExperimentService,
        Depends(get_experiment_service),
    ],
):

    deleted = service.delete_experiment(
        experiment_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found.",
        )

    return None
