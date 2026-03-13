import numpy as np
import os
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from model import build_rnn_model, build_lstm_model

def train():
    data_dir = "data"
    
    print("Loading preprocessed data...")
    X_train = np.load(os.path.join(data_dir, "X_train.npy"))
    y_train = np.load(os.path.join(data_dir, "y_train.npy"))
    X_test = np.load(os.path.join(data_dir, "X_test.npy"))
    y_test = np.load(os.path.join(data_dir, "y_test.npy"))
    
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    
    input_shape = (X_train.shape[1], X_train.shape[2])
    output_dim = y_train.shape[1]
    
    print("Building model...")
    # Using LSTM for better long-term sequence learning
    model = build_lstm_model(input_shape, output_dim)
    model.summary()
    
    os.makedirs('models', exist_ok=True)
    checkpoint = ModelCheckpoint(
        "models/traffic_model.h5", 
        monitor='val_loss', 
        save_best_only=True, 
        mode='min',
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=10, 
        restore_best_weights=True,
        verbose=1
    )
    
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=50,
        batch_size=32,
        callbacks=[checkpoint, early_stop],
        verbose=1
    )
    
    model.save("models/traffic_model_final.h5")
    print("Training complete! Model saved to models/traffic_model_final.h5")

if __name__ == "__main__":
    if not os.path.exists("data/X_train.npy"):
        print("Preprocessed data not found. Running data_preprocessing.py first...")
        from data_preprocessing import preprocess_data
        preprocess_data()
    train()
