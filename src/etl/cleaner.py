import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the retail dataset.
    """

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Convert InvoiceDate to datetime
    cleaned_df["InvoiceDate"] = pd.to_datetime(
        cleaned_df["InvoiceDate"],
        errors="coerce"
    )

    # Remove negative price records
    cleaned_df = cleaned_df[cleaned_df["Price"] >= 0]

    # Create cancellation flag
    cleaned_df["is_cancelled"] = (
        cleaned_df["Invoice"]
        .astype(str)
        .str.startswith("C")
    )

    return cleaned_df