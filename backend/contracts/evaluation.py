from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    molecule_id: str = Field(...)

    qed: float = Field(...)
    sa_score: float = Field(...)
    affinity: float = Field(...)

    lipinski_pass: bool = Field(...)
