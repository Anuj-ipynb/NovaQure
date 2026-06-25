from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import get_molecule_service
from backend.schemas.molecule import (
    MoleculeCreate,
    MoleculeResponse,
    MoleculeUpdate,
)
from backend.services.molecule_service import MoleculeService


router = APIRouter(
    prefix="/molecules",
    tags=["Molecules"],
)


# ---------------------------------------------------------
# Create Molecule
# ---------------------------------------------------------

@router.post(
    "",
    response_model=MoleculeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_molecule(
    molecule: MoleculeCreate,
    service: Annotated[
        MoleculeService,
        Depends(get_molecule_service),
    ],
):

    try:

        created = service.create_molecule(
            experiment_id=molecule.experiment_id,
            smiles=molecule.smiles,
            selfies=molecule.selfies,
            score=molecule.score,
        )

        return created

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Molecules
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[MoleculeResponse],
)
def list_molecules(
    service: Annotated[
        MoleculeService,
        Depends(get_molecule_service),
    ],
):

    return service.list_molecules()


# ---------------------------------------------------------
# Get Molecule
# ---------------------------------------------------------

@router.get(
    "/{molecule_id}",
    response_model=MoleculeResponse,
)
def get_molecule(
    molecule_id: str,
    service: Annotated[
        MoleculeService,
        Depends(get_molecule_service),
    ],
):

    molecule = service.get_molecule(
        molecule_id
    )

    if molecule is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Molecule not found.",
        )

    return molecule


# ---------------------------------------------------------
# Delete Molecule
# ---------------------------------------------------------

@router.delete(
    "/{molecule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_molecule(
    molecule_id: str,
    service: Annotated[
        MoleculeService,
        Depends(get_molecule_service),
    ],
):

    deleted = service.delete_molecule(
        molecule_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Molecule not found.",
        )

    return None
