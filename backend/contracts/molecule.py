from pydantic import BaseModel, Field


class Molecule(BaseModel):
    molecule_id: str
    smiles: str
    selfies: str

    source: str = "dataset"
    validity_score: float = 1.0

    latent_vector: list[float] | None = None

    generation_iteration: int = 0