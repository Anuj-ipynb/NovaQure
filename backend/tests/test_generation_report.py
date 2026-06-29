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
