import pandas as pd

def abc_analysis(inventory):

    inventory = inventory.sort_values(
        "TotalRevenue",
        ascending=False
    )

    inventory["RevenuePercent"] = (
        inventory["TotalRevenue"]
        / inventory["TotalRevenue"].sum()
    )

    inventory["Cumulative"] = (
        inventory["RevenuePercent"].cumsum()
    )

    def classify(x):

        if x <= 0.80:
            return "A"
        elif x <= 0.95:
            return "B"
        else:
            return "C"

    inventory["ABC"] = inventory["Cumulative"].apply(classify)

    inventory["Recommendation"] = inventory["ABC"].map({
        "A":"Reorder Immediately",
        "B":"Monitor",
        "C":"Overstock"
    })

    return inventory