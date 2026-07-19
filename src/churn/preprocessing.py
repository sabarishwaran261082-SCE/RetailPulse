import pandas as pd

def prepare_customer_data(df):
    """
    Create customer-level features for churn prediction.
    """

    customer_features = (
        df.groupby("Customer ID")
        .agg(
            Frequency=("Invoice", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            TotalSpent=("TotalPrice", "sum"),
            AvgOrderValue=("TotalPrice", "mean"),
            LastPurchase=("InvoiceDate", "max"),
            FirstPurchase=("InvoiceDate", "min")
        )
        .reset_index()
    )

    customer_features["Recency"] = (
        customer_features["LastPurchase"].max()
        - customer_features["LastPurchase"]
    ).dt.days

    customer_features["CustomerAge"] = (
        customer_features["LastPurchase"]
        - customer_features["FirstPurchase"]
    ).dt.days

    customer_features.drop(
        columns=["FirstPurchase", "LastPurchase"],
        inplace=True
    )

    return customer_features