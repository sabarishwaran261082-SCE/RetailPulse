import pandas as pd


def monthly_sales(df):
    return (
        df.groupby("InvoiceMonth")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )


def daily_sales(df):
    return (
        df.groupby("Day")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )


def hourly_sales(df):
    return (
        df.groupby("Hour")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )


def quarterly_sales(df):
    return (
        df.groupby("Quarter")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )


def weekday_vs_weekend(df):
    return (
        df.groupby("IsWeekend")["TotalPrice"]
        .sum()
        .reset_index(name="Revenue")
    )


def monthly_orders(df):
    return (
        df.groupby("InvoiceMonth")["Invoice"]
        .nunique()
        .reset_index(name="Orders")
    )