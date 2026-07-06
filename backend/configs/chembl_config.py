"""
NovaQure

ChEMBL Configuration

Centralized configuration for ChEMBL API access and
Chemprop dataset preparation.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

from pathlib import Path


# ==========================================================
# ChEMBL API
# ==========================================================

CHEMBL_BASE_URL: str = "https://www.ebi.ac.uk/chembl/api/data"

DEFAULT_ACTIVITY_TYPE: str = "IC50"

DEFAULT_ACTIVITY_UNITS: str = "nM"

DEFAULT_TIMEOUT: int = 30

PAGE_SIZE: int = 1000


# ==========================================================
# Dataset Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_ROOT = PROJECT_ROOT / "datasets"

EXTERNAL_DATASET_ROOT = DATASET_ROOT / "external"

CHEMBL_DATASET_ROOT = EXTERNAL_DATASET_ROOT / "chembl"

RAW_DATASET_PATH = CHEMBL_DATASET_ROOT / "raw"

PROCESSED_DATASET_PATH = CHEMBL_DATASET_ROOT / "processed"

RAW_DATASET_PATH = CHEMBL_DATASET_ROOT / "raw"

PROCESSED_DATASET_PATH = CHEMBL_DATASET_ROOT / "processed"


# ==========================================================
# Model Paths
# ==========================================================

MODEL_ROOT = PROJECT_ROOT / "models"

CHEMPROP_MODEL_PATH = MODEL_ROOT / "chemprop"


# ==========================================================
# CSV Columns
# ==========================================================

CSV_COLUMNS = [
    "smiles",
    "pIC50",
]
