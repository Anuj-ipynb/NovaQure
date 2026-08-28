from __future__ import annotations

import json
import platform
import sys
import time
import uuid
from datetime import UTC
from datetime import datetime
from pathlib import Path

from rdkit import rdBase

from backend.generation.generation_config import (
    GenerationConfig,
)


class ExperimentMetadata:
    """
    Builds reproducible metadata describing a
    generation experiment.
    """

    @classmethod
    def build(
        cls,
        molecule_count: int,
        execution_time: float,
    ) -> dict:

        return {

            "run_id": str(
                uuid.uuid4()
            ),

            "timestamp": datetime.now(
                UTC
            ).isoformat(),

            "generation_version":
            GenerationConfig.GENERATION_VERSION,

            "dataset": {

                "name":
                GenerationConfig.DATASET_NAME,

                "path":
                str(
                    GenerationConfig.DATASET_PATH
                ),

                "molecule_count":
                molecule_count,

            },

            "encoder": {

                "name":
                GenerationConfig.ENCODER,

                "latent_dimension":
                GenerationConfig.LATENT_DIM,

            },

            "sampler": {

                "name":
                GenerationConfig.SAMPLER,

            },

            "mutation": {

                "strategy":
                GenerationConfig.MUTATION_STRATEGY,

                "mutations_per_molecule":
                GenerationConfig.MUTATIONS_PER_MOLECULE,

                "max_retries":
                GenerationConfig.MUTATION_MAX_RETRIES,

            },

            "ranking": {

                "strategy":
                GenerationConfig.RANKING_STRATEGY,

                "weights":
                GenerationConfig.RANKING_WEIGHTS,

            },

            "random_seed":
            GenerationConfig.RANDOM_SEED,

            "execution_time_seconds":
            round(
                execution_time,
                4,
            ),

            "python_version":
            sys.version.split()[0],

            "platform":
            platform.platform(),

            "rdkit_version":
            rdBase.rdkitVersion,

        }

    @staticmethod
    def save(
        metadata: dict,
        output_file: Path,
    ) -> None:

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
            )