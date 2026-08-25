from pathlib import Path


class GenerationConfig:

    DATASET_NAME = "chembl_egfr"

    DATASET_PATH = Path(
        "datasets/external/chembl/processed/EGFR.csv"
    )

    OUTPUT_DIR = Path(
        "outputs/artifacts"
    )

    OUTPUT_FILE = (
        OUTPUT_DIR /
        "generated_molecules.json"
    )

    METADATA_FILE = (
        OUTPUT_DIR /
        "experiment_metadata.json"
    )

    MAX_MOLECULES = 5

    EXPORT_LATENT_VECTORS = False

    LATENT_VECTOR_PRECISION = 4

    NOVEL_MOLECULE_COUNT = 100

    LATENT_DIM = 128

    LATENT_NOISE_STD = 0.15

    LATENT_INTERPOLATION_STEPS = 8

    RANDOM_SEED = 42

    ENCODER = "vjtv"

    SAMPLER = "qcbm"

    MUTATION_STRATEGY = "weighted"

    RANKING_STRATEGY = "weighted"

    GENERATION_VERSION = "3.6"

    PIPELINE_VERSION = "generation-v3"

    MUTATIONS_PER_MOLECULE = 3

    MUTATION_MAX_RETRIES = 3

    MUTATION_WEIGHTS = {
        "replacement": 0.45,
        "insertion": 0.20,
        "deletion": 0.15,
        "branch": 0.20,
    }

    RANKING_WEIGHTS = {
        "novelty": 0.40,
        "diversity": 0.35,
        "validity": 0.25,
    }