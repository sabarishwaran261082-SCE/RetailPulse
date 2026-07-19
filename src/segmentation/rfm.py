import pandas as pd
from datetime import timedelta


def create_rfm(df):
    """
    Create RFM Table

    Returns
    -------
    Customer ID
    Recency
    Frequency
    Monetary
    """

    data = df.copy()

    # Remove cancelled orders
    data = data[data["Quantity"] > 0]

    # Latest purchase date
    snapshot_date = data["InvoiceDate"].max() + timedelta(days=1)

    rfm = (
        data.groupby("Customer ID")
        .agg(
            {
                "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
                "Invoice": "nunique",
                "TotalPrice": "sum",
            }
        )
        .reset_index()
    )

    rfm.columns = [
        "Customer ID",
        "Recency",
        "Frequency",
        "Monetary",
    ]

    return rfm


def add_rfm_scores(rfm):

    rfm = rfm.copy()

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        5,
        labels=[5,4,3,2,1]
    )

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1,2,3,4,5]
    )

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        5,
        labels=[1,2,3,4,5]
    )

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    return rfm


def customer_summary(rfm):

    summary = {
        "Total Customers": len(rfm),
        "Average Recency": round(rfm["Recency"].mean(),2),
        "Average Frequency": round(rfm["Frequency"].mean(),2),
        "Average Monetary": round(rfm["Monetary"].mean(),2),
        "Highest Spending": round(rfm["Monetary"].max(),2),
        "Lowest Spending": round(rfm["Monetary"].min(),2)
    }

    return summary


def top_customers(rfm, n=10):

    return (
        rfm.sort_values(
            by="Monetary",
            ascending=False
        )
        .head(n)
    )


def bottom_customers(rfm, n=10):

    return (
        rfm.sort_values(
            by="Monetary"
        )
        .head(n)
    )