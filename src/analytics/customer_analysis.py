import pandas as pd

CUSTOMER_ID = "Customer ID"
TOTAL_PRICE = "TotalPrice"
INVOICE = "Invoice"


def total_customers(df):
    return df[CUSTOMER_ID].nunique()


def top_customers(df, n=10):
    return (
        df.groupby(CUSTOMER_ID)[TOTAL_PRICE]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


def customer_order_count(df):
    return (
        df.groupby(CUSTOMER_ID)[INVOICE]
        .nunique()
        .reset_index(name="Orders")
    )


def average_customer_spending(df):
    return (
        df.groupby(CUSTOMER_ID)[TOTAL_PRICE]
        .sum()
        .mean()
    )


def customer_revenue(df):
    return (
        df.groupby(CUSTOMER_ID)[TOTAL_PRICE]
        .sum()
        .reset_index(name="Revenue")
    )