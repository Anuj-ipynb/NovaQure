from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from backend.auth.dependencies import (
    get_current_user,
)

from backend.auth.roles import (
    UserRole,
)


# ---------------------------------------------------------
# Require Authentication
# ---------------------------------------------------------


def require_authenticated_user(
    current_user=Depends(
        get_current_user,
    ),
):
    """
    Ensures user is authenticated.
    """

    return current_user


# ---------------------------------------------------------
# Require Admin
# ---------------------------------------------------------


def require_admin(
    current_user=Depends(
        get_current_user,
    ),
):
    """
    Admin-only dependency.
    """

    if (
        current_user.get("role")
        != UserRole.ADMIN.value
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user


# ---------------------------------------------------------
# Require Researcher or Admin
# ---------------------------------------------------------


def require_researcher_or_admin(
    current_user=Depends(
        get_current_user,
    ),
):
    """
    Researcher and Admin access.
    """

    allowed_roles = {
        UserRole.RESEARCHER.value,
        UserRole.ADMIN.value,
    }

    if (
        current_user.get("role")
        not in allowed_roles
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions.",
        )

    return current_user


# ---------------------------------------------------------
# Require System
# ---------------------------------------------------------


def require_system(
    current_user=Depends(
        get_current_user,
    ),
):
    """
    Internal system access.
    """

    if (
        current_user.get("role")
        != UserRole.SYSTEM.value
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System access required.",
        )

    return current_user
