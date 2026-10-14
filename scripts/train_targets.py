"""
NovaQure Target Dataset Fetcher & Model Trainer

Fetches bioactivity datasets from ChEMBL and trains Chemprop GNN models
for target proteins: KRAS, BACE1, HER2, BRAF.
"""

import sys
import logging
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.evaluation.chemprop_dataset import ChempropDatasetBuilder
from backend.evaluation.chemprop_train import ChempropTrainer
from backend.configs.chembl_config import PROCESSED_DATASET_PATH, MODEL_ROOT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("train_targets")

import argparse

TARGET_CONFIGS = [
    {
        "name": "EGFR",
        "chembl_id": "CHEMBL203",
        "description": "Epidermal Growth Factor Receptor (NSCLC)"
    },
    {
        "name": "KRAS",
        "chembl_id": "CHEMBL2189121",
        "description": "GTPase KRas (Colorectal, Pancreatic, NSCLC)"
    },
    {
        "name": "BACE1",
        "chembl_id": "CHEMBL4822",
        "description": "Beta-secretase 1 / APP processing (Alzheimer's)"
    },
    {
        "name": "HER2",
        "chembl_id": "CHEMBL1824",
        "description": "ERBB2 Kinase (Breast Cancer / EGFR counter-screen)"
    },
    {
        "name": "BRAF",
        "chembl_id": "CHEMBL5145",
        "description": "Proto-oncogene B-Raf Kinase (Melanoma)"
    },
]


def main():
    parser = argparse.ArgumentParser(description="NovaQure Multi-Target GNN Trainer")
    parser.add_argument("--force", action="store_true", help="Force retraining even if models already exist")
    args = parser.parse_args()

    logger.info("Initializing NovaQure Multi-Target Dataset & Model Pipeline...")
    model_dir = MODEL_ROOT / "chemprop"
    model_dir.mkdir(parents=True, exist_ok=True)

    with ChempropDatasetBuilder() as builder:
        for target in TARGET_CONFIGS:
            name = target["name"]
            chembl_id = target["chembl_id"]
            csv_path = PROCESSED_DATASET_PATH / f"{name}.csv"
            model_path = model_dir / f"{name.lower()}_model.pt"

            logger.info("==========================================")
            logger.info("Processing Target: %s (%s)", name, target["description"])
            logger.info("==========================================")

            # Phase 1: Dataset Fetching & Preprocessing
            if csv_path.exists() and not args.force:
                logger.info("Dataset already exists at %s", csv_path)
            else:
                logger.info("Fetching ChEMBL bioactivities for %s (%s)...", name, chembl_id)
                try:
                    builder.build_and_save(protein_name=name, target_chembl_id=chembl_id)
                    logger.info("Dataset saved successfully to %s", csv_path)
                except Exception as exc:
                    logger.error("Failed to build dataset for %s: %s", name, exc)
                    continue

            # Phase 2: Model Training
            if model_path.exists() and not args.force:
                logger.info("Trained model already exists at %s", model_path)
            else:
                logger.info("Launching Chemprop GNN training for %s...", name)
                try:
                    trainer = ChempropTrainer(dataset_path=csv_path, target_name=name)
                    trained_model = trainer.run()
                    logger.info("Trained model saved at %s", trained_model)
                except Exception as exc:
                    logger.error("Training failed for target %s: %s", name, exc)

    logger.info("Multi-Target Pipeline processing completed.")


if __name__ == "__main__":
    main()
