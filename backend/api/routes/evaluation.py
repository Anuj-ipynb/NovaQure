from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.evaluation.evaluation_service import EvaluationService

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


class EvaluationItem(BaseModel):
    smiles: str
    energy: float = -0.85
    variance: float = 0.12
    noise: float = 0.08
    convergence: float = 0.93


class EvaluationRequest(BaseModel):
    experiment_id: str = "exp-default"
    molecules: list[EvaluationItem]


@router.post("/run")
async def run_evaluation(request: EvaluationRequest):
    try:
        service = EvaluationService()

        results = []
        for item in request.molecules:
            res = service.evaluate(
                smiles=item.smiles,
                energy=item.energy,
                variance=item.variance,
                noise=item.noise,
                convergence=item.convergence,
            )
            results.append(res)

        return {
            "experiment_id": request.experiment_id,
            "evaluated_count": len(results),
            "results": [r.model_dump() for r in results],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )