from pathlib import Path
import pandas as pd


def load_smiles_dataset(
    file_path: str
) -> list[str]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(path)

    if "smiles" not in df.columns:
        raise ValueError(
            "Missing smiles column"
        )

    return (
        df["smiles"]
        .dropna()
        .astype(str)
        .tolist()
    )
