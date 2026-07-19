from prophet import Prophet


def train_prophet(df):

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(df)

    return model


def forecast_sales(model, periods=12):

    future = model.make_future_dataframe(
        periods=periods,
        freq="ME"
    )

    forecast = model.predict(future)

    return forecast