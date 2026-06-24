import json

from backend.generation.dataset_loader import (
    load_smiles_dataset
)

from backend.generation.data_preprocessor import (
    canonicalize_smiles,
    remove_duplicates
)

from backend.generation.molecule_generator import (
    generate_molecules
)

from backend.generation.generation_config import (
    GenerationConfig
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

        GenerationConfig.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            GenerationConfig.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [
                    molecule.model_dump()
                    for molecule in molecules
                ],
                f,
                indent=2
            )

        return molecules


if __name__ == "__main__":

    service = GenerationService()

    molecules = service.run()

    print(
        f"Generated {len(molecules)} molecules"
    )
