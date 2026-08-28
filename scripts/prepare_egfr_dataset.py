# -*- coding: utf-8 -*-
"""Utility script to prepare the EGFR ChemBL dataset for the
Variational Junction‑Tree Encoder (JTVAE‑inspired).

The original EGFR CSV (``datasets/external/chembl/processed/EGFR.csv``) 
contains two columns:
    - ``smiles``    : canonical SMILES strings
    - ``pIC50``     : activity values (float)

The encoder service expects a column named ``selfies`` with SELFIES
representations of the molecules.  This script:
    1. Loads the original CSV.
    2. Validates every SMILES using RDKit – rows with invalid SMILES are
       logged and removed.
    3. Converts each valid SMILES to SELFIES via the ``selfies`` package.
    4. Writes a new CSV that includes ``selfies`` (and keeps the original
       ``pIC50`` column).
    5. Optionally creates a train/validation split (default 90/10) if the
       ``--split`` flag is provided.

The script can be invoked directly from the command line::

    python scripts/prepare_egfr_dataset.py \
        --input datasets/external/chembl/processed/EGFR.csv \
        --output datasets/external/chembl/processed/EGFR_selfies.csv \
        [--split]

The resulting ``EGFR_selfies.csv`` can be fed to ``scripts/train_jtvae.py``
without further changes.
"""

import argparse
import pathlib
import sys
from typing import Tuple, List

import pandas as pd
from rdkit import Chem
import selfies

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _load_csv(path: pathlib.Path) -> pd.DataFrame:
    """Load the CSV and ensure the expected columns exist.

    Parameters
    ----------
    path:
        Path to the original ChemBL CSV.
    Returns
    -------
    pandas.DataFrame
        Dataframe with at least ``smiles`` and ``pIC50`` columns.
    """
    df = pd.read_csv(path)
    # Columns are normalized to lower‑case later, so the required set must be lower‑case as well
    required = {"smiles", "pic50"}
    missing = required - set(df.columns.str.lower())
    if missing:
        raise ValueError(f"Missing required columns {missing} in {path}")
    # Normalise column names to lower‑case for robust downstream handling
    df.columns = [c.lower() for c in df.columns]
    return df


def _validate_smiles(smiles: str) -> bool:
    """Return ``True`` if ``smiles`` can be parsed by RDKit.
    ``None`` or empty strings are considered invalid.
    """
    if not isinstance(smiles, str) or not smiles.strip():
        return False
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None


def _convert_to_selfies(smiles: str) -> str:
    """Convert a valid SMILES to a SELFIES string.
    The ``selfies`` library raises ``ValueError`` on failure – we let the
    exception propagate because we only call this after successful validation.
    """
    return selfies.encoder(smiles)


def _process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate SMILES, convert to SELFIES, and drop invalid rows.
    The function adds a new ``selfies`` column and returns the cleaned frame.
    """
    valid_mask = df["smiles"].apply(_validate_smiles)
    if not valid_mask.all():
        invalid_idx = df[~valid_mask].index.tolist()
        print(f"[INFO] Dropping {len(invalid_idx)} rows with invalid SMILES.", file=sys.stderr)
        df = df[valid_mask]
    # Convert
    df["selfies"] = df["smiles"].apply(_convert_to_selfies)
    # Re‑order columns: selfies first (encoder expects it), then the rest
    cols = ["selfies"] + [c for c in df.columns if c != "selfies"]
    return df[cols]


def _train_val_split(df: pd.DataFrame, test_size: float = 0.1, seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Simple random split using pandas ``sample``.
    Returns ``train_df, val_df``.
    """
    val = df.sample(frac=test_size, random_state=seed)
    train = df.drop(val.index)
    return train, val

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare EGFR ChemBL dataset for JTVAE training.")
    parser.add_argument("--input", type=str, required=True, help="Path to original EGFR CSV.")
    parser.add_argument("--output", type=str, required=True, help="Path for the SELFIES‑augmented CSV.")
    parser.add_argument("--split", action="store_true", help="If set, also write train/val splits alongside the main CSV.")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = _load_csv(input_path)
    df_processed = _process_dataframe(df)
    df_processed.to_csv(output_path, index=False)
    print(f"[INFO] Processed dataset written to {output_path}")

    if args.split:
        train_df, val_df = _train_val_split(df_processed)
        train_path = output_path.with_name(output_path.stem + "_train.csv")
        val_path = output_path.with_name(output_path.stem + "_val.csv")
        train_df.to_csv(train_path, index=False)
        val_df.to_csv(val_path, index=False)
        print(f"[INFO] Train split written to {train_path}")
        print(f"[INFO] Validation split written to {val_path}")


if __name__ == "__main__":
    main()
