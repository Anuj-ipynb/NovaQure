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


def _map_ranking_response(ranking) -> dict:
    smiles = None
    affinity = None
    qed = None
    sa = None
    iupac_name = None
    reliability = ranking.confidence
    
    if ranking.molecule:
        smiles = ranking.molecule.smiles
        if ranking.molecule.evaluation:
            affinity = ranking.molecule.evaluation.binding_affinity
            qed = ranking.molecule.evaluation.qed
            sa = ranking.molecule.evaluation.sa_score
            if hasattr(ranking.molecule.evaluation, "iupac_name"):
                iupac_name = ranking.molecule.evaluation.iupac_name

    return {
        "id": ranking.id,
        "molecule_id": ranking.molecule_id,
        "rank": ranking.rank,
        "score": ranking.score,
        "confidence": ranking.confidence,
        "created_at": ranking.created_at,
        "updated_at": ranking.updated_at,
        "smiles": smiles,
        "reliability": reliability,
        "affinity": affinity,
        "qed": qed,
        "sa": sa,
        "iupac_name": iupac_name,
    }

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

        return _map_ranking_response(created)

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

    rankings = service.list_rankings()
    return [_map_ranking_response(r) for r in rankings]


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

    return _map_ranking_response(ranking)


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
