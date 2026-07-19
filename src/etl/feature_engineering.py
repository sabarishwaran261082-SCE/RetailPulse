import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create business features for analytics and machine learning.
    """

    feature_df = df.copy()

    # Revenue per transaction
    feature_df["TotalPrice"] = (
        feature_df["Quantity"] * feature_df["Price"]
    )

    # Date-based features
    feature_df["Year"] = feature_df["InvoiceDate"].dt.year
    feature_df["Month"] = feature_df["InvoiceDate"].dt.month
    feature_df["Day"] = feature_df["InvoiceDate"].dt.day
    feature_df["DayOfWeek"] = feature_df["InvoiceDate"].dt.day_name()
    feature_df["Hour"] = feature_df["InvoiceDate"].dt.hour
    feature_df["Quarter"] = feature_df["InvoiceDate"].dt.quarter

    # Weekend flag
    feature_df["IsWeekend"] = (
        feature_df["InvoiceDate"].dt.dayofweek >= 5
    )

    # Month period for cohort analysis
    feature_df["InvoiceMonth"] = (
        feature_df["InvoiceDate"].dt.to_period("M")
    )

    return feature_df