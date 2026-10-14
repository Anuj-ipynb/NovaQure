"""
NovaQure Target Proteins API Router
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from backend.proteins.protein_service import ProteinService
from backend.evaluation.affinity_service import AffinityService

router = APIRouter(
    prefix="/proteins",
    tags=["Proteins"],
)


class SelectivityRequest(BaseModel):
    smiles: str
    primary_target: str = "EGFR"
    counter_targets: Optional[List[str]] = None


@router.get("/targets")
async def list_target_proteins():
    try:
        service = ProteinService()
        return service.get_all_targets()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/targets/{target_id}")
async def get_target_protein(target_id: str):
    service = ProteinService()
    target = service.get_target(target_id)
    if not target:
        raise HTTPException(status_code=404, detail=f"Target '{target_id}' not found.")
    return target


@router.post("/selectivity")
async def predict_selectivity(request: SelectivityRequest):
    try:
        counters = request.counter_targets or ["KRAS", "BACE1", "HER2", "BRAF"]
        all_targets = [request.primary_target] + [t for t in counters if t != request.primary_target]
        
        affinity_service = AffinityService()
        
        affinities: Dict[str, float] = {}
        for target in all_targets:
            aff = affinity_service.predict(request.smiles, target_protein=target)
            affinities[target] = round(aff, 3)
            
        primary_aff = affinities.get(request.primary_target, 7.0)
        selectivity_deltas: Dict[str, float] = {}
        selectivity_ratios: Dict[str, float] = {}
        
        for t, aff in affinities.items():
            if t != request.primary_target:
                delta = round(primary_aff - aff, 3)
                ratio = round(10 ** delta, 2)
                selectivity_deltas[t] = delta
                selectivity_ratios[t] = ratio

        return {
            "smiles": request.smiles,
            "primary_target": request.primary_target,
            "affinities": affinities,
            "selectivity_deltas_pic50": selectivity_deltas,
            "selectivity_ratios_fold": selectivity_ratios,
            "is_selective": all(d >= 0.5 for d in selectivity_deltas.values()),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
