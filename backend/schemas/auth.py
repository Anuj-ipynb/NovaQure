from typing import Optional

from pydantic import EmailStr
from pydantic import Field

from backend.schemas.base_schema import (
    NovaQureSchema,
    TimestampSchema,
)


# ---------------------------------------------------------
# User Registration Request
# ---------------------------------------------------------


class UserRegisterRequest(
    NovaQureSchema
):
    """
    Request payload used during
    researcher registration.
    """

    email: EmailStr = Field(
        ...,
        description="Researcher Email Address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Account Password",
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Researcher Full Name",
    )


# ---------------------------------------------------------
# Login Request
# ---------------------------------------------------------


class UserLoginRequest(
    NovaQureSchema
):
    """
    Request payload used
    for authentication.
    """

    email: EmailStr = Field(
        ...,
        description="Registered Email Address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User Password",
    )


# ---------------------------------------------------------
# User Response
# ---------------------------------------------------------


class UserResponse(
    TimestampSchema
):
    """
    Standard user object
    returned by APIs.
    """

    id: str

    email: str

    full_name: str

    role: str

    is_active: bool


# ---------------------------------------------------------
# JWT Token Response
# ---------------------------------------------------------


class TokenResponse(
    NovaQureSchema
):
    """
    JWT token returned
    after successful login.
    """

    access_token: str

    token_type: str = "bearer"

    expires_in: int


# ---------------------------------------------------------
# Current Authenticated User
# ---------------------------------------------------------


class CurrentUser(
    NovaQureSchema
):
    """
    Lightweight user object
    extracted from JWT.
    """

    user_id: str

    email: str

    role: str


# ---------------------------------------------------------
# Complete Authentication Response
# ---------------------------------------------------------


class AuthResponse(
    NovaQureSchema
):
    """
    Authentication response
    returned after login.
    """

    user: UserResponse

    token: TokenResponse
