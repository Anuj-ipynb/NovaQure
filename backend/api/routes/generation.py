from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.generation.generation_service import GenerationService

router = APIRouter(
    prefix="/generation",
    tags=["Generation"],
)


class GenerationRequest(BaseModel):
    experiment_id: str = "exp-default"
    num_molecules: int = 20


@router.post("/run")
async def run_generation(request: GenerationRequest):
    try:
        service = GenerationService()

        molecules = service.run()

        return {
            "experiment_id": request.experiment_id,
            "generated_count": len(molecules),
            "molecules": molecules,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )