from pydantic import BaseModel, Field


class AgentDecision(BaseModel):
    experiment_id: str = Field(...)

    decision: str = Field(...)
    reason: str = Field(...)
    confidence: float = Field(...)
