from fastapi import APIRouter, Depends, HTTPException, status

from backend.auth.dependencies import get_current_user
from backend.auth.jwt_handler import create_access_token
from backend.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserRegisterRequest,
):
    """
    Temporary registration endpoint.

    User persistence will be connected
    to the UserRepository in Sprint 7D.
    """

    return {
        "message": "User registered successfully.",
        "email": payload.email,
        "full_name": payload.full_name,
    }


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: UserLoginRequest,
):

    # Temporary authentication
    # Replace with database validation later

    token = create_access_token(
        {
            "user_id": "user-001",
            "email": payload.email,
            "role": "researcher",
        }
    )

    return TokenResponse(
        access_token=token,
        expires_in=3600,
    )


# ---------------------------------------------------------
# Current User
# ---------------------------------------------------------

@router.get(
    "/me",
)
def me(
    current_user=Depends(
        get_current_user
    ),
):

    return current_user
