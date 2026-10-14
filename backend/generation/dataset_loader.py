from pathlib import Path
import pandas as pd


def load_smiles_dataset(
    file_path: str | None = None,
    target_protein: str | None = None,
) -> list[str]:

    path: Path | None = None

    if target_protein:
        t_path = Path(f"datasets/external/chembl/processed/{target_protein.upper()}.csv")
        if t_path.exists():
            path = t_path

    if path is None and file_path:
        f_path = Path(file_path)
        if f_path.exists():
            path = f_path

    if path is None or not path.exists():
        fallback = Path("datasets/external/chembl/processed/EGFR.csv")
        if fallback.exists():
            path = fallback
        else:
            raise FileNotFoundError(f"Target dataset file not found for target: {target_protein} (path: {file_path})")

    target_label = target_protein.upper() if target_protein else path.stem.upper()
    print(f"INFO: [DatasetLoader] Loading target {target_label} dataset from: {path.resolve()}")

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
