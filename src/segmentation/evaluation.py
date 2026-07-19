from sklearn.metrics import silhouette_score
import pandas as pd


def calculate_silhouette_score(data, labels):
    """
    Calculate silhouette score for clustering.
    """
    score = silhouette_score(data, labels)
    return round(score, 4)


def cluster_summary(rfm_cluster):
    """
    Generate summary statistics for each cluster.
    """
    summary = (
        rfm_cluster
        .groupby("Cluster")
        .agg(
            Customers=("Customer ID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .round(2)
        .reset_index()
    )

    return summary