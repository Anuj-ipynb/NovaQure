from pathlib import Path


def find_root():

    current = Path.cwd().resolve()

    while current != current.parent:

        if (
            (current / "backend").exists()
            and
            (current / "datasets").exists()
        ):
            return current

        current = current.parent

    raise RuntimeError(
        "NovaQure root not found."
    )


ROOT = find_root()


VALIDATOR = (
    ROOT
    / "backend"
    / "generation"
    / "generation_validator.py"
)

PIPELINE_TEST = (
    ROOT
    / "backend"
    / "tests"
    / "test_generation_pipeline.py"
)

REPORT_TEST = (
    ROOT
    / "backend"
    / "tests"
    / "test_generation_report.py"
)


VALIDATOR_CODE = r'''
from backend.contracts.molecule import (
    Molecule
)


class GenerationValidator:

    REQUIRED_VECTOR_LENGTH = 128

    @classmethod
    def validate(
        cls,
        molecules: list[Molecule]
    ) -> None:

        if not molecules:

            raise ValueError(
                "No molecules generated."
            )

        ids = set()

        for molecule in molecules:

            if molecule.molecule_id in ids:

                raise ValueError(
                    "Duplicate molecule_id."
                )

            ids.add(
                molecule.molecule_id
            )

            if not molecule.smiles:

                raise ValueError(
                    "Missing SMILES."
                )

            if not molecule.selfies:

                raise ValueError(
                    "Missing SELFIES."
                )

            if molecule.latent_vector is None:

                raise ValueError(
                    "Missing latent vector."
                )

            if len(
                molecule.latent_vector
            ) != cls.REQUIRED_VECTOR_LENGTH:

                raise ValueError(
                    "Invalid latent dimension."
                )

            if molecule.source not in (

                "dataset",

                "mutation"

            ):

                raise ValueError(
                    "Invalid source."
                )
'''


PIPELINE_TEST_CODE = r'''
from backend.generation.generation_service import (
    GenerationService
)

from backend.generation.generation_validator import (
    GenerationValidator
)


def test_generation_pipeline():

    molecules = (
        GenerationService()
        .run()
    )

    GenerationValidator.validate(
        molecules
    )

    assert len(
        molecules
    ) > 0
'''


REPORT_TEST_CODE = r'''
import json

from pathlib import Path

from backend.generation.generation_config import (
    GenerationConfig
)


def test_generation_report_exists():

    report = (

        GenerationConfig.OUTPUT_DIR

        /

        "generation_report.json"

    )

    assert report.exists()


def test_generation_report_keys():

    report = (

        GenerationConfig.OUTPUT_DIR

        /

        "generation_report.json"

    )

    data = json.loads(

        report.read_text()

    )

    required = [

        "total_molecules",

        "unique_smiles",

        "duplicate_molecules",

        "dataset_molecules",

        "mutation_molecules",

        "average_validity",

        "average_diversity"

    ]

    for key in required:

        assert key in data
'''


def write(path, content):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )

    print(
        f"UPDATED {path.relative_to(ROOT)}"
    )


if __name__ == "__main__":

    print(
        "NovaQure Generation G3.5B"
    )

    write(
        VALIDATOR,
        VALIDATOR_CODE
    )

    write(
        PIPELINE_TEST,
        PIPELINE_TEST_CODE
    )

    write(
        REPORT_TEST,
        REPORT_TEST_CODE
    )

    print()

    print(
        "Generation validation & tests installed."
    )