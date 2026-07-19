import pandas as pd


def revenue_by_country(df):
    return (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def orders_by_country(df):
    return (
        df.groupby("Country")["Invoice"]
        .nunique()
        .sort_values(ascending=False)
        .reset_index(name="Orders")
    )


def customers_by_country(df):
    return (
        df.groupby("Country")["Customer ID"]
        .nunique()
        .sort_values(ascending=False)
        .reset_index(name="Customers")
    )