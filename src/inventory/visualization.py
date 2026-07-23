import matplotlib.pyplot as plt

def plot_top_products(inventory):

    top = inventory.nlargest(
        10,
        "TotalRevenue"
    )

    plt.figure(figsize=(10,5))

    plt.bar(
        top["StockCode"].astype(str),
        top["TotalRevenue"]
    )

    plt.xticks(rotation=90)

    plt.title("Top Revenue Products")

    plt.tight_layout()

    plt.show()


def plot_abc(inventory):

    inventory["ABC"].value_counts().plot(
        kind="bar"
    )

    plt.title("ABC Analysis")

    plt.show()