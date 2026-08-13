"""
NovaQure

Affinity Prediction Service

Uses a trained Chemprop model to predict molecular affinity.

Responsibilities
----------------
- Validate trained model
- Validate structural validity of SMILES strings via RDKit
- Generate temporary prediction datasets safely
- Execute Chemprop prediction cleanly by suppressing CLI stdout pollution
- Parse prediction outputs with resilient format safety guards
- Clean up file mutations upon pipeline exit or error states

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging
import subprocess
import tempfile
from pathlib import Path

import pandas as pd
from rdkit import Chem

from backend.configs.chemprop_config import (
    SMILES_COLUMN,
)

logger = logging.getLogger(__name__)


class AffinityService:
    """
    Wrapper around Chemprop prediction operations.
    """

    def __init__(self) -> None:
        self.model_path = self._find_model()

    # ---------------------------------------------------------
    # Locate Model
    # ---------------------------------------------------------

    def _find_model(self, target_protein: str | None = None) -> Path | None:
        """
        Locate the trained Chemprop model for a specific target protein or default.
        """
        from backend.configs.chemprop_config import MODEL_DIRECTORY, MODEL_PATH

        if target_protein:
            target_model = MODEL_DIRECTORY / f"{target_protein.lower()}_model.pt"
            if target_model.exists():
                logger.info("Using target-specific Chemprop model: %s", target_model)
                return target_model

        if MODEL_PATH.exists():
             logger.info("Using default Chemprop model: %s", MODEL_PATH)
             return MODEL_PATH

        logger.warning("No trained Chemprop model (best.pt) found at %s. Fallback mode enabled.", MODEL_PATH)
        return None

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify the trained model path exists (or fallback is active).
        """
        return self.model_path is None or self.model_path.exists()

    # ---------------------------------------------------------
    # Temporary File Factory Utilities
    # ---------------------------------------------------------

    def _create_input_csv(self, smiles_list: list[str]) -> Path:
        """
        Create a temporary CSV file populated with SMILES strings for prediction.
        """
        dataframe = pd.DataFrame({SMILES_COLUMN: smiles_list})

        # Explicitly closing the file descriptor immediately allows 
        # subprocess.run to write to the file smoothly across all operating systems.
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        dataframe.to_csv(temp_path, index=False)
        return temp_path

    def _create_output_path(self) -> Path:
        """
        Allocate an isolated temporary path for Chemprop to write its results.
        """
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            
        return temp_path

    # ---------------------------------------------------------
    # Execute Prediction
    # ---------------------------------------------------------

    def _run_prediction(self, input_path: Path, output_path: Path) -> None:
        """
        Execute the Chemprop prediction command using the configured model binary.
        Suppresses console output logs unless an execution error occurs.
        """
        command = [
            "chemprop",
            "predict",
            "-i",
            str(input_path),
            "-o",
            str(output_path),
            "--model-paths",
            str(self.model_path),
            "-s",
            SMILES_COLUMN,
        ]

        try:
            import os
            # Ensure the virtual environment's bin/Scripts folder is in PATH for the subprocess
            env = os.environ.copy()
            project_root = Path(__file__).resolve().parents[2]
            venv_scripts = str(project_root / "venv" / "Scripts")
            env["PATH"] = venv_scripts + os.pathsep + env.get("PATH", "")
            
            # Resolve the absolute path to chemprop.exe if running in Windows venv
            chemprop_exe = project_root / "venv" / "Scripts" / "chemprop.exe"
            if chemprop_exe.exists():
                command[0] = str(chemprop_exe)

            # capture_output=True keeps production API streams clean of recurring PyTorch
            # and Lightning optimization alerts during fast evaluation cycles.
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Chemprop prediction execution failed.")
            if exc.stdout:
                logger.error("Chemprop stdout: %s", exc.stdout)
            if exc.stderr:
                logger.error("Chemprop stderr: %s", exc.stderr)
            raise RuntimeError(
                "Unable to execute Chemprop prediction via CLI."
            ) from exc

    # ---------------------------------------------------------
    # Read Predictions
    # ---------------------------------------------------------

    def _read_predictions(self, output_path: Path) -> list[float]:
        """
        Read and extract values from the prediction CSV file generated by Chemprop.
        """
        dataframe = pd.read_csv(output_path)

        # Filters out the SMILES column to dynamically isolate the target property header,
        # handling future-proof cases where extra columns like 'uncertainty' may exist.
        prediction_columns = [
            col
            for col in dataframe.columns
            if col.lower() != SMILES_COLUMN.lower()
        ]

        if not prediction_columns:
            raise RuntimeError(
                "Unexpected prediction format: target column could not be isolated."
            )

        # Target the primary affinity prediction (the first column following smiles)
        prediction_column = prediction_columns[0]

        predictions = (
            dataframe[prediction_column]
            .astype(float)
            .tolist()
        )
        return predictions

    # ---------------------------------------------------------
    # Cleanup Temporary Files
    # ---------------------------------------------------------

    def _cleanup(self, *files: Path) -> None:
        """
        Remove temporary disk footprints generated during the inference cycle.
        """
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception as exc:
                logger.warning(
                    "Unable to delete temporary runtime file %s: %s",
                    file,
                    exc,
                )

    # ---------------------------------------------------------
    # Prediction Interface Methods
    # ---------------------------------------------------------

    def predict_batch(self, smiles_list: list[str]) -> list[float]:
        """
        Predict affinity scores for a collection of molecular SMILES structures.
        """
        if not smiles_list:
            return []

        # Client-facing chemical validation guard
        for smiles in smiles_list:
            if not smiles or not isinstance(smiles, str) or Chem.MolFromSmiles(smiles) is None:
                raise ValueError(f"Invalid or corrupted SMILES string rejected: '{smiles}'")

        if self.model_path is None:
            # Fallback return: return neutral affinity scores
            return [0.5] * len(smiles_list)

        input_csv = self._create_input_csv(smiles_list)
        output_csv = self._create_output_path()

        try:
            self._run_prediction(input_csv, output_csv)
            predictions = self._read_predictions(output_csv)
            return predictions

        finally:
            self._cleanup(input_csv, output_csv)

    def predict(self, smiles: str) -> float:
        """
        Predict the affinity score of a single molecular SMILES structure.
        """
        if not smiles or not isinstance(smiles, str) or Chem.MolFromSmiles(smiles) is None:
            raise ValueError(f"Invalid or corrupted SMILES string rejected: '{smiles}'")

        prediction = self.predict_batch([smiles])
        return prediction[0]

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self) -> "AffinityService":
        return self

    def __exit__(
        self,
        *args: object,
    ) -> bool:
        # Prevent context scope exception swallowing
        return False