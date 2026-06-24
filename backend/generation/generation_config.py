from pathlib import Path


class GenerationConfig:

    DATASET_PATH = Path(
        "datasets/raw/sample_smiles.csv"
    )

    OUTPUT_DIR = Path(
        "outputs/artifacts"
    )

    OUTPUT_FILE = (
        OUTPUT_DIR /
        "generated_molecules.json"
    )

    MAX_MOLECULES = 100

    NOVEL_MOLECULE_COUNT = 100

    LATENT_DIM = 128

    MUTATIONS_PER_MOLECULE = 3
