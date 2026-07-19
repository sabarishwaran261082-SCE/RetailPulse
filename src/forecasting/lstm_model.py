from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense


def build_lstm_model(input_shape):

    model = Sequential()

    model.add(
        LSTM(
            64,
            activation="relu",
            input_shape=input_shape
        )
    )

    model.add(Dense(32, activation="relu"))

    model.add(Dense(1))

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model


def train_lstm(
    model,
    X_train,
    y_train,
    epochs=100,
    batch_size=8
):

    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )

    return history


def predict_lstm(
    model,
    X_test
):

    predictions = model.predict(
        X_test
    )

    return predictions