import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def plot_confusion_matrix(model, X_test, y_test):
    """
    Plot confusion matrix.
    """

    ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        cmap="Blues"
    )

    plt.title("Customer Churn Confusion Matrix")
    plt.show()


def plot_feature_importance(model, feature_names):
    """
    Plot feature importance.
    """

    importance = model.feature_importances_

    plt.figure(figsize=(8, 5))
    plt.barh(feature_names, importance)
    plt.title("Feature Importance")
    plt.xlabel("Importance")
    plt.show()