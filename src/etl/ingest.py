import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the retail dataset from CSV or Excel.
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format.")

    return df