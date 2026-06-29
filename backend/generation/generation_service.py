import json

from backend.generation.dataset_loader import (
    load_smiles_dataset,
)

from backend.generation.data_preprocessor import (
    canonicalize_smiles,
    remove_duplicates,
)

from backend.generation.generation_config import (
    GenerationConfig,
)

from backend.generation.molecule_generator import (
    generate_molecules,
)

from backend.generation.generation_report import (
    GenerationReport,
)

from backend.sampling.candidate_selector import (
    CandidateSelector,
)


class GenerationService:

    def run(self):

        smiles = load_smiles_dataset(
            str(
                GenerationConfig.DATASET_PATH
            )
        )

        smiles = [

            canonicalize_smiles(
                s
            )

            for s in smiles

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

        report = GenerationReport.build(
            molecules
        )

        print()

        print(
            "Generation Report"
        )

        print(
            "------------------"
        )

        for key, value in report.items():

            print(
                f"{key}: {value}"
            )

        GenerationConfig.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            GenerationConfig.OUTPUT_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                [
                    molecule.model_dump()
                    for molecule in molecules
                ],
                f,
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
        ) as f:

            json.dump(
                report,
                f,
                indent=2,
            )

        return molecules


if __name__ == "__main__":

    service = GenerationService()

    molecules = service.run()

    print()

    print(
        f"Generated {len(molecules)} molecules."
    )