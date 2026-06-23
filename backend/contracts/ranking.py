from pydantic import BaseModel, Field


class Ranking(BaseModel):
    molecule_id: str = Field(...)

    rank: int = Field(...)
    score: float = Field(...)

    explanation: str = Field(...)
