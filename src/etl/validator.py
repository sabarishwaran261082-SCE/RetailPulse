import pandas as pd


def validate_data(df: pd.DataFrame) -> dict:
    """
    Validate the retail dataset and return a data quality report.
    """

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": df.isnull().sum().to_dict(),
        "negative_quantity": int((df["Quantity"] < 0).sum()),
        "zero_quantity": int((df["Quantity"] == 0).sum()),
        "negative_price": int((df["Price"] < 0).sum()),
        "zero_price": int((df["Price"] == 0).sum()),
        "cancelled_orders": int(
            df["Invoice"].astype(str).str.startswith("C").sum()
        ),
        "unique_customers": int(df["Customer ID"].nunique()),
        "unique_products": int(df["StockCode"].nunique()),
        "unique_invoices": int(df["Invoice"].nunique()),
        "countries": int(df["Country"].nunique()),
    }

    return report