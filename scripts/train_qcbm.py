# -*- coding: utf-8 -*-
"""Training script for the QCBM quantum sampler.

Loads the EGFR dataset, encodes molecules through the trained VJTVAE to
collect target latent vectors, then trains the QCBM circuit parameters
to match that distribution via MMD minimization.

Usage::

    python scripts/train_qcbm.py \
        --data datasets/external/chembl/processed/EGFR_selfies_train.csv \
        --epochs 50 --lr 0.1 --max-molecules 200
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Add project root to PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import numpy as np
import pandas as pd

from backend.generation.variational_jtvae import VariationalJTVAE
from backend.sampling.qcbm_sampler import QCBMSampler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train QCBM circuit on VJTVAE latent distribution")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV with 'selfies' column")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=0.1, help="Learning rate for Adam optimizer")
    parser.add_argument("--max-molecules", type=int, default=200, help="Max molecules to encode for target distribution")
    parser.add_argument("--output", type=str, default="models/qcbm_weights.npy", help="Output path for trained weights")
    args = parser.parse_args()

    # Step 1: Load dataset
    logger.info("Loading dataset from %s", args.data)
    df = pd.read_csv(args.data)
    if "selfiles" in df.columns:
        df.rename(columns={"selfiles": "selfies"}, inplace=True)
    selfies_list = df["selfies"].dropna().tolist()[:args.max_molecules]
    logger.info("Loaded %d SELFIES strings", len(selfies_list))

    # Step 2: Encode through VJTVAE to get target latent vectors
    logger.info("Encoding molecules through VJTVAE...")
    encoder = VariationalJTVAE()
    latent_vectors = []
    for i, sf in enumerate(selfies_list):
        try:
            vec = encoder.encode(sf)
            latent_vectors.append(vec)
        except Exception as e:
            logger.debug("Skipping molecule %d: %s", i, e)
    logger.info("Successfully encoded %d / %d molecules", len(latent_vectors), len(selfies_list))

    if len(latent_vectors) < 10:
        logger.error("Too few valid latent vectors (%d). Need at least 10.", len(latent_vectors))
        sys.exit(1)

    target_array = np.array(latent_vectors)

    # Step 3: Train QCBM
    logger.info("Training QCBM for %d epochs (lr=%.4f)...", args.epochs, args.lr)
    sampler = QCBMSampler()
    losses = sampler.train(target_array, epochs=args.epochs, lr=args.lr)

    # Step 4: Save weights
    sampler.save_weights(args.output)

    # Summary
    logger.info("=== Training Summary ===")
    logger.info("  Epochs: %d", args.epochs)
    logger.info("  Initial loss: %.6f", losses[0])
    logger.info("  Final loss:   %.6f", losses[-1])
    logger.info("  Weights saved to: %s", args.output)


if __name__ == "__main__":
    main()
