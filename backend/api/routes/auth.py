from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from backend.auth.dependencies import (
    get_current_user,
)

from backend.auth.jwt_handler import (
    create_access_token,
)

from backend.auth.authorization import (
    require_admin,
    require_researcher_or_admin,
    require_system,
)

from backend.auth.roles import (
    UserRole,
)

from backend.schemas.auth import (
    UserLoginRequest,
    UserRegisterRequest,
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
    to UserRepository later.
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
    """
    Login endpoint.
    Generates JWT access token for authentication.
    """

    token = create_access_token(
        {
            "user_id": "user-001",
            "id": "user-001",
            "email": payload.email,
            "full_name": "Default Researcher",
            "role": UserRole.RESEARCHER.value,
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
        get_current_user,
    ),
):
    """
    Returns authenticated user information.
    """

    return {
        "id": current_user.get("id") or current_user.get("user_id", "user-001"),
        "user_id": current_user.get("user_id") or current_user.get("id", "user-001"),
        "email": current_user.get("email", ""),
        "full_name": current_user.get("full_name", "Default Researcher"),
        "role": current_user.get("role", "researcher"),
    }


# ---------------------------------------------------------
# Research Endpoint
# ---------------------------------------------------------


@router.get(
    "/research",
)
def researcher_only(
    current_user=Depends(
        require_researcher_or_admin,
    ),
):
    """
    Accessible to researchers and admins.
    """

    return {
        "message": "Research access granted.",
        "user": current_user,
    }


# ---------------------------------------------------------
# Admin Endpoint
# ---------------------------------------------------------


@router.get(
    "/admin",
)
def admin_only(
    current_user=Depends(
        require_admin,
    ),
):
    """
    Accessible only to admins.
    """

    return {
        "message": "Welcome Admin",
        "user": current_user,
    }


# ---------------------------------------------------------
# System Endpoint
# ---------------------------------------------------------


@router.get(
    "/system",
)
def system_only(
    current_user=Depends(
        require_system,
    ),
):
    """
    Accessible only to internal system users.
    """

    return {
        "message": "System access granted.",
        "user": current_user,
    }
