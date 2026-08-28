"""
NovaQure Authentication Package
"""

# JWT Utilities
from .jwt_handler import (
    create_access_token,
    decode_access_token,
)

# Authentication Dependencies
from .dependencies import (
    get_current_user,
)

# Roles
from .roles import (
    UserRole,
)

# RBAC
from .rbac import (
    require_roles,
)

# Authorization Helpers
from .authorization import (
    require_authenticated_user,
    require_admin,
    require_researcher_or_admin,
    require_system,
)

__all__ = [
    # JWT
    "create_access_token",
    "decode_access_token",

    # Dependencies
    "get_current_user",

    # Roles
    "UserRole",

    # RBAC
    "require_roles",

    # Authorization Helpers
    "require_authenticated_user",
    "require_admin",
    "require_researcher_or_admin",
    "require_system",
]
