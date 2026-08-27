from pathlib import Path
import pandas as pd


def load_smiles_dataset(
    file_path: str
) -> list[str]:

    path = Path(file_path)

    # Explicit EGFR dataset resolution
    if not path.exists():
        path = Path("datasets/external/chembl/processed/EGFR.csv")

    if not path.exists():
        raise FileNotFoundError(f"Target EGFR dataset file not found at: {file_path}")

    print(f"INFO: [DatasetLoader] Loading target EGFR dataset from: {path.resolve()}")

    df = pd.read_csv(path, nrows=50)

    if "smiles" not in df.columns:
        raise ValueError(
            "Missing smiles column in dataset"
        )

    return (
        df["smiles"]
        .dropna()
        .astype(str)
        .tolist()
    )
