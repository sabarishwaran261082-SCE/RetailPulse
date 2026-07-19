import plotly.express as px


def forecast_plot(forecast):

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Sales Forecast"
    )

    return fig


def trend_plot(forecast):

    fig = px.line(
        forecast,
        x="ds",
        y="trend",
        title="Trend"
    )

    return fig