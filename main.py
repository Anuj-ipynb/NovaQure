from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.services.optimization_pipeline import OptimizationPipeline
from app.services.ranking_service import MoleculeScore

app = FastAPI()

# Initialize pipeline
pipeline = OptimizationPipeline()


# ---------------------------
# Request Schemas
# ---------------------------

class MoleculeInput(BaseModel):
    molecule_id: str
    qed: float
    sa: float
    affinity: float
    reliability: float


class OptimizationRequest(BaseModel):
    molecules: List[MoleculeInput]
    iterations: int = 2


# ---------------------------
# Routes
# ---------------------------

@app.get("/")
def root():
    return {"message": "NovaQure Optimization API Running"}


@app.post("/optimize")
def optimize(request: OptimizationRequest):
    # Convert request input to MoleculeScore objects
    molecules = [
        MoleculeScore(
            molecule_id=m.molecule_id,
            qed=m.qed,
            sa=m.sa,
            affinity=m.affinity,
            reliability=m.reliability
        )
        for m in request.molecules
    ]

    # Run optimization pipeline
    result = pipeline.run(molecules, request.iterations)

    # Extract final iteration result (last iteration)
    final_result = result[-1]["results"] if result else []

    return {
        "status": "success",
        "iterations": len(result),
        "final_result": final_result,
        "data": result
    }