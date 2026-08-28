from collections.abc import Callable

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from backend.auth.dependencies import (
    get_current_user,
)
from backend.auth.roles import (
    UserRole,
)


def require_roles(
    *allowed_roles: UserRole,
) -> Callable:

    def role_checker(
        current_user=Depends(
            get_current_user
        ),
    ):

        user_role = current_user.get(
            "role"
        )

        allowed = {
            role.value
            for role in allowed_roles
        }

        if user_role not in allowed:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have "
                    "permission to access "
                    "this resource."
                ),
            )

        return current_user

    return role_checker
