import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout

def build_rnn_model(input_shape, output_dim):
    """
    Builds a Recurrent Neural Network for predicting traffic events.
    """
    model = Sequential([
        SimpleRNN(64, activation='relu', input_shape=input_shape, return_sequences=True),
        Dropout(0.2),
        SimpleRNN(32, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(output_dim, activation='sigmoid')  # Sigmoid works well for minmax scaled data
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def build_lstm_model(input_shape, output_dim):
    """
    Builds an LSTM network as an alternative for longer sequence dependencies.
    """
    model = Sequential([
        tf.keras.layers.LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
        Dropout(0.2),
        tf.keras.layers.LSTM(32, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(output_dim, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model
