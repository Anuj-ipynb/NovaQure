from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.configs.llm_config import get_active_llm_info, set_active_llm_provider

router = APIRouter(
    prefix="/config",
    tags=["Config"],
)


class LLMConfigUpdate(BaseModel):
    provider: str


@router.get("/llm")
async def get_llm_config():
    try:
        info = get_active_llm_info()
        return {
            "status": "success",
            "active_llm": info,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/llm")
async def update_llm_config(request: LLMConfigUpdate):
    try:
        valid_providers = ["granite", "nvidia", "ollama", "deterministic", "auto"]
        prov = request.provider.lower()
        if prov not in valid_providers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider '{request.provider}'. Must be one of: {valid_providers}",
            )

        set_active_llm_provider(prov)
        info = get_active_llm_info()
        return {
            "status": "success",
            "message": f"Active LLM provider updated to '{prov}'",
            "active_llm": info,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
