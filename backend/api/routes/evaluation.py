from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.evaluation.evaluation_service import EvaluationService

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


class EvaluationRequest(BaseModel):
    experiment_id: str
    molecules: list


@router.post("/run")
async def run_evaluation(request: EvaluationRequest):
    try:
        service = EvaluationService()

        results = service.evaluate(
            request.molecules
        )

        return {
            "experiment_id": request.experiment_id,
            "evaluated_count": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )