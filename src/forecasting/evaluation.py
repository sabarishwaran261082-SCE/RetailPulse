from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import numpy as np


def evaluate(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(
        actual,
        predicted
    )

    mape = (
        np.mean(
            abs((actual - predicted) / actual)
        )
    ) * 100

    return {
        "MAE": round(mae,2),
        "RMSE": round(rmse,2),
        "MAPE": round(mape,2),
        "R2": round(r2,2)
    }