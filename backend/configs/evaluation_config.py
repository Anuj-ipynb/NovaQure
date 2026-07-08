"""
NovaQure

Evaluation Configuration
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIRECTORY = (
    PROJECT_ROOT
    / "artifacts"
    / "evaluation"
)