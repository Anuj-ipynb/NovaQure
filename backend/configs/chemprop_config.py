"""
NovaQure

Chemprop Configuration

Centralized configuration for Chemprop dataset loading,
training, evaluation, and model persistence.

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

from pathlib import Path

from backend.configs.chembl_config import (
    MODEL_ROOT,
    PROCESSED_DATASET_PATH,
)

# ==========================================================
# Dataset
# ==========================================================

DEFAULT_DATASET = PROCESSED_DATASET_PATH / "EGFR.csv"

SMILES_COLUMN = "smiles"

TARGET_COLUMN = "pIC50"

# ==========================================================
# Data Split
# ==========================================================

TRAIN_SPLIT = 0.80

VALIDATION_SPLIT = 0.10

TEST_SPLIT = 0.10

RANDOM_SEED = 42

# ==========================================================
# Training
# ==========================================================

TASK_TYPE = "regression"

EPOCHS = 50

BATCH_SIZE = 64

LEARNING_RATE = 1e-3

WEIGHT_DECAY = 0.0

# ==========================================================
# Model
# ==========================================================

MODEL_DIRECTORY = MODEL_ROOT / "chemprop"

MODEL_NAME = "egfr_model.pt"

MODEL_PATH = MODEL_DIRECTORY / MODEL_NAME

# ==========================================================
# Metrics
# ==========================================================

METRICS_FILE = MODEL_DIRECTORY / "metrics.json"

TRAINING_CONFIG_FILE = MODEL_DIRECTORY / "training_config.json"