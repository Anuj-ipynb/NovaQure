from __future__ import annotations

import json
import time

from backend.generation.data_preprocessor import (
    canonicalize_smiles,
    remove_duplicates,
)

from backend.generation.dataset_loader import (
    load_smiles_dataset,
)

from backend.generation.experiment_metadata import (
    ExperimentMetadata,
)

from backend.generation.generation_config import (
    GenerationConfig,
)

from backend.generation.generation_report import (
    GenerationReport,
)

from backend.generation.molecule_generator import (
    generate_molecules,
)

from backend.sampling.candidate_selector import (
    CandidateSelector,
)


class GenerationService:
    """
    Orchestrates the complete molecular generation workflow.

    Responsibilities
    ----------------
    - Load dataset
    - Generate candidate molecules
    - Filter and rank candidates
    - Generate reports
    - Save experiment artifacts
    """

    def run(self):

        start_time = time.perf_counter()

        smiles = load_smiles_dataset(
            str(
                GenerationConfig.DATASET_PATH
            )
        )

        smiles = [

            canonicalize_smiles(
                smile
            )

            for smile in smiles

        ]

        smiles = remove_duplicates(
            smiles
        )

        molecules = generate_molecules(

            smiles[
                :GenerationConfig.MAX_MOLECULES
            ]

        )

        selector = CandidateSelector()

        molecules = selector.select(
            molecules,
            reference_smiles=smiles,
        )

        execution_time = (
            time.perf_counter()
            - start_time
        )

        report = GenerationReport.build(
            molecules=molecules,
            execution_time=execution_time,
        )

        metadata = ExperimentMetadata.build(
            molecule_count=len(
                molecules
            ),
            execution_time=execution_time,
        )

        self._print_report(
            report
        )

        self._save_outputs(
            molecules=molecules,
            report=report,
            metadata=metadata,
        )

        return molecules

    @staticmethod
    def _print_report(
        report: dict,
    ) -> None:

        def print_section(
            title: str,
            values: dict,
        ) -> None:

            print()
            print(title)
            print("-" * 60)

            for key, value in values.items():

                label = (
                    key
                    .replace("_", " ")
                    .title()
                )

                if isinstance(
                    value,
                    float,
                ):

                    print(
                        f"{label:<35}: {value:.4f}"
                    )

                else:

                    print(
                        f"{label:<35}: {value}"
                    )

        print()

        print("=" * 60)

        print(
            "NovaQure Generation Report".center(
                60
            )
        )

        print("=" * 60)

        for section, values in report.items():

            if isinstance(
                values,
                dict,
            ):

                print_section(
                    section
                    .replace(
                        "_",
                        " ",
                    )
                    .title(),
                    values,
                )

            else:

                label = (
                    section
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
                )

                if isinstance(
                    values,
                    float,
                ):

                    print(
                        f"{label:<35}: {values:.4f}"
                    )

                else:

                    print(
                        f"{label:<35}: {values}"
                    )

        print()

        print("=" * 60)

        print(
            "Artifacts".center(
                60
            )
        )

        print("=" * 60)

        print(
            f"✓ Molecules : {GenerationConfig.OUTPUT_FILE.name}"
        )

        print(
            "✓ Report    : generation_report.json"
        )

        print(
            f"✓ Metadata  : {GenerationConfig.METADATA_FILE.name}"
        )

        print("=" * 60)

    @staticmethod
    def _save_outputs(
        molecules,
        report,
        metadata,
    ) -> None:

        GenerationConfig.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            GenerationConfig.OUTPUT_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                [

                    molecule.model_dump()

                    for molecule in molecules

                ],

                file,

                indent=2,

            )

        report_file = (
            GenerationConfig.OUTPUT_DIR
            /
            "generation_report.json"
        )

        with open(
            report_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=2,
            )

        ExperimentMetadata.save(
            metadata,
            GenerationConfig.METADATA_FILE,
        )


if __name__ == "__main__":

    service = GenerationService()

    molecules = service.run()

    print()

    print(
        f"Generated {len(molecules)} molecules."
    )