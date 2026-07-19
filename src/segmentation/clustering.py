import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def scale_features(rfm):

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        rfm[["Recency", "Frequency", "Monetary"]]
    )

    scaled_df = pd.DataFrame(
        scaled,
        columns=[
            "Recency",
            "Frequency",
            "Monetary"
        ]
    )

    return scaled_df, scaler


def elbow_method(data, max_clusters=10):

    inertia = []

    for k in range(1, max_clusters + 1):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(data)

        inertia.append(model.inertia_)

    return inertia


def train_kmeans(data, n_clusters=4):

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    clusters = model.fit_predict(data)

    return model, clusters


def assign_clusters(rfm, clusters):

    result = rfm.copy()

    result["Cluster"] = clusters

    return result