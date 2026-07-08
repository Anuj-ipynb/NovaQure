"""
NovaQure DTO Package

Contains every request and response schema
used throughout the backend.
"""

# ---------------------------------------------------------
# Base Schemas
# ---------------------------------------------------------

from .base_schema import (
    NovaQureSchema,
    TimestampSchema,
)

# ---------------------------------------------------------
# Project Schemas
# ---------------------------------------------------------

from .project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectSummary,
    ProjectListResponse,
)

# ---------------------------------------------------------
# Experiment Schemas
# ---------------------------------------------------------

from .experiment import (
    ExperimentCreate,
    ExperimentUpdate,
    ExperimentResponse,
    ExperimentSummary,
    ExperimentListResponse,
)

# ---------------------------------------------------------
# Molecule Schemas
# ---------------------------------------------------------

from .molecule import (
    MoleculeCreate,
    MoleculeUpdate,
    MoleculeResponse,
    MoleculeSummary,
    MoleculeListResponse,
)

# ---------------------------------------------------------
# Ranking Schemas
# ---------------------------------------------------------

from .ranking import (
    RankingCreate,
    RankingUpdate,
    RankingResponse,
    RankingSummary,
    RankingListResponse,
)

# ---------------------------------------------------------
# Authentication Schemas
# ---------------------------------------------------------

from .auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
    CurrentUser,
    AuthResponse,
)

# ---------------------------------------------------------
# Public Exports
# ---------------------------------------------------------

__all__ = [
    # Base
    "NovaQureSchema",
    "TimestampSchema",

    # Projects
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectSummary",
    "ProjectListResponse",

    # Experiments
    "ExperimentCreate",
    "ExperimentUpdate",
    "ExperimentResponse",
    "ExperimentSummary",
    "ExperimentListResponse",

    # Molecules
    "MoleculeCreate",
    "MoleculeUpdate",
    "MoleculeResponse",
    "MoleculeSummary",
    "MoleculeListResponse",

    # Rankings
    "RankingCreate",
    "RankingUpdate",
    "RankingResponse",
    "RankingSummary",
    "RankingListResponse",

    # Authentication
    "UserRegisterRequest",
    "UserLoginRequest",
    "UserResponse",
    "TokenResponse",
    "CurrentUser",
    "AuthResponse",
]
