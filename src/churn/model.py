from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def prepare_train_test(customer_data):
    """
    Split customer data into train and test sets.
    """

    X = customer_data.drop(columns=["Customer ID", "Churn"])
    y = customer_data["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


def train_random_forest(X_train, y_train):
    """
    Train a Random Forest classifier.
    """

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def predict(model, X_test):
    """
    Predict churn labels.
    """

    return model.predict(X_test)