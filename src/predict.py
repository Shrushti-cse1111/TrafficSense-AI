import numpy as np
import os
import pandas as pd
from tensorflow.keras.models import load_model

def predict(input_sequence=None):
    """
    Predict the next traffic event given a sequence of recent events.
    """
    # Determine basic paths relative to this script
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(root_dir, "models", "traffic_model_final.h5")
    
    if not os.path.exists(model_path):
        print(f"Trained model not found at {model_path}. Run train.py first.")
        return
        
    print("Loading trained model...")
    model = load_model(model_path, compile=False)
    
    data_dir = os.path.join(root_dir, "data")
    
    # Load feature columns to understand prediction output
    with open(os.path.join(data_dir, "feature_columns.txt"), "r") as f:
        feature_cols = f.read().split(",")
        
    print("Loading scaler configuration...")
    # Load previously saved scaler min and range
    scaler_min = np.load(os.path.join(data_dir, "scaler_min.npy"))
    scaler_range = np.load(os.path.join(data_dir, "scaler_range.npy"))
    
    # If no input sequence is provided, let's just grab the last sequence from the test set
    if input_sequence is None:
        print("No input sequence provided. Generating prediction for a sample from the test set...")
        X_test = np.load(os.path.join(data_dir, "X_test.npy"))
        input_sequence = X_test[-1:] # Shape expands to (1, seq_length, num_features)
    else:
        # Expected shape is (1, seq_length, num_features)
        if len(input_sequence.shape) == 2:
            input_sequence = np.expand_dims(input_sequence, axis=0)
            
    # Predict the next event
    predicted_scaled = model.predict(input_sequence)
    
    # Inverse transform prediction to original scale
    # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0)) -> X_scaled = X_std * (max - min) + min
    # Inverse: X = X_scaled * scaler_range + scaler_min
    predicted_real = predicted_scaled[0] * scaler_range + scaler_min
    
    # Format the result
    result = {col: val for col, val in zip(feature_cols, predicted_real)}
    
    print("\n--- Next Event Prediction ---")
    print(f"Predicted Latitude:  {result['latitude']:.4f}")
    print(f"Predicted Longitude: {result['longitude']:.4f}")
    if 'severity' in result:
        print(f"Predicted Severity:  {result['severity']:.2f}")
    if 'speed_kmh' in result:
        print(f"Predicted Speed:     {result['speed_kmh']:.1f} km/h")
        
    # Find most likely event type
    event_type_cols = [c for c in feature_cols if c.startswith('event_type_')]
    if event_type_cols:
        event_probs = {c.replace('event_type_', ''): result[c] for c in event_type_cols}
        most_likely_event = max(event_probs, key=event_probs.get)
        print(f"Predicted Event Type: {most_likely_event}")
        
        # Display probabilities for each event type
        print("\nEvent Type Probabilities:")
        for etype, prob in event_probs.items():
            print(f"  {etype}: {max(0, min(1, prob)) * 100:.2f}%")
            
    return result

if __name__ == "__main__":
    predict()
