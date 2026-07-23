import pandas as pd

def prepare_inventory_data(df):

    inventory = (
        df.groupby(["StockCode", "Description"])
        .agg(
            TotalQuantity=("Quantity", "sum"),
            TotalRevenue=("TotalPrice", "sum"),
            Orders=("Invoice", "nunique"),
            AvgQuantity=("Quantity", "mean")
        )
        .reset_index()
    )

    return inventory