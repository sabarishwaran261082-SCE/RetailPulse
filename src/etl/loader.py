from pathlib import Path
import pandas as pd


def save_processed_data(
    df: pd.DataFrame,
    filename: str = "online_retail_processed.csv"
):
    """
    Save processed dataset in the project's data/processed folder.
    """

    # Find project root from this file
    project_root = Path(__file__).resolve().parents[2]

    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    df.to_csv(output_file, index=False)

    print(f"Project Root : {project_root}")
    print(f"Saved To     : {output_file}")