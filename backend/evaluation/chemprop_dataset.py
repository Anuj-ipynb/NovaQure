"""
NovaQure

Chemprop Dataset Builder

Builds Chemprop-compatible datasets from ChEMBL.

Responsibilities
----------------
- Retrieve activities from ChEMBL
- Validate SMILES
- Canonicalize molecules
- Convert activity values
- Export CSV

Author:
    NovaQure Evaluation Team
"""

from __future__ import annotations

import logging
import math
from pathlib import Path

import pandas as pd
from rdkit import Chem

from backend.configs.chembl_config import (
    PROCESSED_DATASET_PATH,
)

from backend.evaluation.chembl_api import ChEMBLAPI

logger = logging.getLogger(__name__)


class ChempropDatasetBuilder:
    """
    Builds Chemprop datasets from ChEMBL.

    Output CSV format

    smiles,pIC50
    """

    def __init__(self):

        self.api = ChEMBLAPI()

    # ---------------------------------------------------------
    # Canonicalize SMILES
    # ---------------------------------------------------------

    def canonicalize_smiles(
        self,
        smiles: str,
    ) -> str | None:
        """
        Convert a SMILES string into its canonical form.

        Invalid molecules return None.
        """

        try:

            molecule = Chem.MolFromSmiles(smiles)

            if molecule is None:
                return None

            return Chem.MolToSmiles(
                molecule,
                canonical=True,
            )

        except Exception:

            return None

    # ---------------------------------------------------------
    # Convert IC50 → pIC50
    # ---------------------------------------------------------

    def convert_to_pic50(
        self,
        value: float,
        units: str,
    ) -> float | None:
        """
        Convert activity value to pIC50.

        Currently supports nM only.
        """

        if value <= 0:
            return None

        units = units.lower()

        if units == "nm":

            molar = value * 1e-9

        elif units == "um":

            molar = value * 1e-6

        elif units == "mm":

            molar = value * 1e-3

        else:

            logger.debug(
                "Unsupported unit: %s",
                units,
            )

            return None

        return -math.log10(molar)

    # ---------------------------------------------------------
    # Build Dataset
    # ---------------------------------------------------------

    def build_dataset(
        self,
        protein_name: str,
    ) -> pd.DataFrame:
        """
        Build a Chemprop dataset for a target protein.

        Parameters
        ----------
        protein_name : str

        Returns
        -------
        pandas.DataFrame
        """

        logger.info(
            "Building Chemprop dataset for %s",
            protein_name,
        )

        targets = self.api.search_target(protein_name)

        if not targets:
            raise RuntimeError(
                f"No ChEMBL targets found for '{protein_name}'."
            )

        target = targets[0]

        logger.info(
            "Using target %s (%s)",
            target.chembl_id,
            target.name,
        )

        records = self.api.fetch_activity_records(target.chembl_id)

        logger.info(
            "Retrieved %d raw activity records.",
            len(records),
        )

        rows: list[dict[str, float | str]] = []
        seen_smiles: set[str] = set()

        invalid_smiles = 0
        duplicate_smiles = 0

        for item in records:

            smiles = self.canonicalize_smiles(
                item.get("canonical_smiles", "")
            )

            if not smiles:
                invalid_smiles += 1
                continue

            relation = item.get("standard_relation")
            if relation != "=":
                continue

            if item.get("standard_flag") != 1:
                continue

            if smiles in seen_smiles:
                duplicate_smiles += 1
                continue

            seen_smiles.add(smiles)

            # Prefer ChEMBL's standardized pChEMBL value
            if item.get("pchembl_value"):
                try:
                    pic50 = float(item["pchembl_value"])
                except (TypeError, ValueError):
                    continue
            else:
                value = item.get("standard_value")
                units = item.get("standard_units")

                if value is None or units is None:
                    continue

                try:
                    pic50 = self.convert_to_pic50(
                        float(value),
                        units,
                    )
                except (TypeError, ValueError):
                    continue

                if pic50 is None:
                    continue

            if pic50 < 0 or pic50 > 15:
                continue

            rows.append(
                {
                    "smiles": smiles,
                    "pIC50": round(pic50, 4),
                }
            )

        logger.info(
            "Skipped %d invalid molecules.",
            invalid_smiles,
        )

        logger.info(
            "Skipped %d duplicate molecules.",
            duplicate_smiles,
        )

        dataframe = pd.DataFrame(rows)

        if not dataframe.empty:
            dataframe = dataframe.dropna()
            dataframe = dataframe.sort_values(
                by="pIC50",
                ascending=False,
            ).reset_index(drop=True)

            logger.info(
                "pIC50 range: %.2f -> %.2f",
                dataframe["pIC50"].min(),
                dataframe["pIC50"].max(),
            )

            logger.info(
                "Average pIC50: %.2f",
                dataframe["pIC50"].mean(),
            )

        logger.info(
            "Dataset contains %d molecules.",
            len(dataframe),
        )

        return dataframe

    # ---------------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------------

    def save_dataset(
        self,
        dataframe: pd.DataFrame,
        protein_name: str,
    ) -> Path:
        """
        Save a Chemprop dataset as CSV.

        Parameters
        ----------
        dataframe : pd.DataFrame

        protein_name : str

        Returns
        -------
        pathlib.Path
        """

        expected_columns = ["smiles", "pIC50"]

        if list(dataframe.columns) != expected_columns:
            raise RuntimeError(
                "Unexpected dataset columns."
            )

        PROCESSED_DATASET_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            PROCESSED_DATASET_PATH
            / f"{protein_name.upper()}.csv"
        )

        dataframe.to_csv(
            output_path,
            index=False,
        )

        logger.info(
            "Saved %d molecules to %s",
            len(dataframe),
            output_path,
        )

        return output_path

    # ---------------------------------------------------------
    # Build & Save
    # ---------------------------------------------------------

    def build_and_save(
        self,
        protein_name: str,
    ) -> Path:
        """
        Build a dataset and save it as CSV.
        """

        dataframe = self.build_dataset(
            protein_name
        )

        return self.save_dataset(
            dataframe,
            protein_name,
        )

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    def close(self) -> None:
        """
        Close ChEMBL API session.
        """

        self.api.close()

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        self.close()