from pydantic import BaseModel, Field


class Reliability(BaseModel):
    molecule_id: str = Field(...)

    reliability_score: float = Field(...)
    confidence_score: float = Field(...)

    noise_score: float = Field(...)
