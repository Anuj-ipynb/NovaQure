from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.api.deps import (
    get_reliability_service,
)
from backend.schemas.reliability import (
    ReliabilityCreate,
    ReliabilityResponse,
)
from backend.services.reliability_service import (
    ReliabilityService,
)


router = APIRouter(
    prefix="/reliability",
    tags=["Reliability"],
)


# ---------------------------------------------------------
# Create Reliability Snapshot
# ---------------------------------------------------------

@router.post(
    "",
    response_model=ReliabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_snapshot(
    snapshot: ReliabilityCreate,
    service: Annotated[
        ReliabilityService,
        Depends(
            get_reliability_service
        ),
    ],
):

    try:

        created_snapshot = (
            service.create_snapshot(
                **snapshot.model_dump()
            )
        )

        return created_snapshot

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Reliability Snapshots
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[
        ReliabilityResponse
    ],
)
def list_snapshots(
    service: Annotated[
        ReliabilityService,
        Depends(
            get_reliability_service
        ),
    ],
):

    return service.list_snapshots()


# ---------------------------------------------------------
# Get Reliability Snapshot
# ---------------------------------------------------------

@router.get(
    "/{reliability_id}",
    response_model=ReliabilityResponse,
)
def get_snapshot(
    reliability_id: str,
    service: Annotated[
        ReliabilityService,
        Depends(
            get_reliability_service
        ),
    ],
):

    snapshot = service.get_snapshot(
        reliability_id
    )

    if snapshot is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reliability snapshot not found.",
        )

    return snapshot


# ---------------------------------------------------------
# Delete Reliability Snapshot
# ---------------------------------------------------------

@router.delete(
    "/{reliability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_snapshot(
    reliability_id: str,
    service: Annotated[
        ReliabilityService,
        Depends(
            get_reliability_service
        ),
    ],
):

    deleted = service.delete_snapshot(
        reliability_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reliability snapshot not found.",
        )

    return None
