from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.pipeline.pipeline_service import PipelineService


router = APIRouter(
    prefix="/pipeline",
    tags=["Pipeline"],
)


class PipelineRequest(BaseModel):
    energy: float = -0.85
    variance: float = 0.12
    noise: float = 0.08
    convergence: float = 0.93


@router.post("/run")
async def run_pipeline(
    request: PipelineRequest,
):
    try:

        service = PipelineService()

        return service.run(
            energy=request.energy,
            variance=request.variance,
            noise=request.noise,
            convergence=request.convergence,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )