import pandas as pd


def top_products(df, n=10):
    return (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


def highest_revenue_products(df, n=10):
    return (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


def most_returned_products(df, n=10):
    returns = df[df["Quantity"] < 0]

    return (
        returns.groupby("Description")["Quantity"]
        .sum()
        .sort_values()
        .head(n)
        .reset_index()
    )


def product_sales(df):
    return (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )