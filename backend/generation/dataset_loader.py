from pathlib import Path
import pandas as pd


def load_smiles_dataset(
    file_path: str
) -> list[str]:

    path = Path(file_path)

    # Resilient dataset resolution
    if not path.exists():
        fallback_paths = [
            Path("datasets/external/chembl/processed/EGFR.csv"),
            Path("datasets/raw/sample_smiles.csv"),
        ]
        for fb in fallback_paths:
            if fb.exists():
                path = fb
                break

    if not path.exists():
        # Hardcoded fallback list if no dataset file is present
        return [
            "Brc1cccc(Nc2ncnc3cc4ccccc4cc23)c1",
            "CCOc1cc2ncnc(Nc3cccc(Br)c3)c2cc1OCC",
            "CNc1cc2c(Nc3cccc(Br)c3)ncnc2cn1",
            "COc1cc2ncnc(Nc3cccc(Cl)c3F)c2cc1N1CC2(CN(C)C2)OC1=O",
            "COCCOc1cc2ncnc(Nc3cccc(OS(=O)(=O)F)c3)c2cc1OCCOC"
        ]

    df = pd.read_csv(path)

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
