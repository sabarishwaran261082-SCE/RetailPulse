import pandas as pd


def prepare_monthly_sales(df):
    """
    Aggregate monthly sales for forecasting.
    """

    data = df.copy()

    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])

    monthly_sales = (
        data
        .groupby(pd.Grouper(key="InvoiceDate", freq="ME"))
        ["TotalPrice"]
        .sum()
        .reset_index()
    )

    monthly_sales.columns = ["Date", "Sales"]

    return monthly_sales


def prepare_prophet_data(monthly_sales):
    """
    Convert dataframe to Prophet format.
    """

    prophet_df = monthly_sales.rename(
        columns={
            "Date": "ds",
            "Sales": "y"
        }
    )

    return prophet_df

from sklearn.preprocessing import MinMaxScaler
import numpy as np


def prepare_lstm_data(monthly_sales):
    """
    Scale monthly sales for LSTM.
    """

    scaler = MinMaxScaler(feature_range=(0, 1))

    scaled_data = scaler.fit_transform(
        monthly_sales[["Sales"]]
    )

    return scaled_data, scaler


def create_sequences(data, sequence_length=12):
    """
    Create input/output sequences for LSTM.
    """

    X = []
    y = []

    for i in range(sequence_length, len(data)):
        X.append(data[i-sequence_length:i])
        y.append(data[i])

    X = np.array(X)
    y = np.array(y)

    return X, y