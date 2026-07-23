import pandas as pd

def inventory_summary(inventory):
    """
    Generate summary statistics for inventory optimization.
    """

    summary = {
        "Total Products": inventory.shape[0],
        "Total Revenue": inventory["TotalRevenue"].sum(),
        "Total Quantity Sold": inventory["TotalQuantity"].sum(),
        "Average Revenue": inventory["TotalRevenue"].mean(),
        "Average Quantity": inventory["TotalQuantity"].mean(),
        "Category A Products": (inventory["ABC"] == "A").sum(),
        "Category B Products": (inventory["ABC"] == "B").sum(),
        "Category C Products": (inventory["ABC"] == "C").sum()
    }

    return summary