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
    RANKING_WEIGHTS = {
    "novelty": 0.40,
    "diversity": 0.35,
    "validity": 0.25,
}

    MUTATIONS_PER_MOLECULE = 3
    MUTATION_MAX_RETRIES = 3
    MUTATION_STRATEGY = "weighted"

    MUTATION_WEIGHTS = {
    "replacement": 0.45,
    "insertion": 0.20,
    "deletion": 0.15,
    "branch": 0.20,
    }

    LATENT_NOISE_STD = 0.15

    LATENT_INTERPOLATION_STEPS = 8

    RANDOM_SEED = 42

    ENCODER = "embedding"
