import plotly.express as px

CUSTOMER_ID_COLUMN = "Customer ID"


def plot_cluster_distribution(df):

    fig = px.histogram(
        df,
        x="Cluster",
        color="Cluster",
        title="Customer Distribution by Cluster"
    )

    return fig


def plot_recency_frequency(df):

    fig = px.scatter(
        df,
        x="Recency",
        y="Frequency",
        color=df["Cluster"].astype(str),
        hover_data=[CUSTOMER_ID_COLUMN],
        title="Recency vs Frequency"
    )

    return fig


def plot_frequency_monetary(df):

    fig = px.scatter(
        df,
        x="Frequency",
        y="Monetary",
        color=df["Cluster"].astype(str),
        hover_data=[CUSTOMER_ID_COLUMN],
        title="Frequency vs Monetary"
    )

    return fig


def plot_recency_monetary(df):

    fig = px.scatter(
        df,
        x="Recency",
        y="Monetary",
        color=df["Cluster"].astype(str),
        hover_data=[CUSTOMER_ID_COLUMN],
        title="Recency vs Monetary"
    )

    return fig