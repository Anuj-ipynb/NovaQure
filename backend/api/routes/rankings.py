from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import get_ranking_service
from backend.schemas.ranking import (
    RankingCreate,
    RankingResponse,
    RankingUpdate,
)
from backend.services.ranking_service import RankingService


router = APIRouter(
    prefix="/rankings",
    tags=["Rankings"],
)


# ---------------------------------------------------------
# Create Ranking
# ---------------------------------------------------------


@router.post(
    "",
    response_model=RankingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ranking(
    ranking: RankingCreate,
    service: Annotated[
        RankingService,
        Depends(get_ranking_service),
    ],
):

    try:

        created = service.create_ranking(
            molecule_id=ranking.molecule_id,
            rank=ranking.rank,
            score=ranking.score,
            confidence=ranking.confidence,
        )

        return created

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Rankings
# ---------------------------------------------------------


@router.get(
    "",
    response_model=list[RankingResponse],
)
def list_rankings(
    service: Annotated[
        RankingService,
        Depends(get_ranking_service),
    ],
):

    return service.list_rankings()


# ---------------------------------------------------------
# Get Ranking
# ---------------------------------------------------------


@router.get(
    "/{ranking_id}",
    response_model=RankingResponse,
)
def get_ranking(
    ranking_id: str,
    service: Annotated[
        RankingService,
        Depends(get_ranking_service),
    ],
):

    ranking = service.get_ranking(
        ranking_id
    )

    if ranking is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ranking not found.",
        )

    return ranking


# ---------------------------------------------------------
# Delete Ranking
# ---------------------------------------------------------


@router.delete(
    "/{ranking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ranking(
    ranking_id: str,
    service: Annotated[
        RankingService,
        Depends(get_ranking_service),
    ],
):

    deleted = service.delete_ranking(
        ranking_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ranking not found.",
        )

    return None
