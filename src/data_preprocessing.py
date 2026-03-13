import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

def create_sequences(data, seq_length):
    X = []
    y = []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])  # Predict the next step
    return np.array(X), np.array(y)

def preprocess_data(input_path="data/waze_synthetic_data.csv", output_dir="data", seq_length=10):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Sort by timestamp just in case
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # One-hot encode the event_type
    df = pd.get_dummies(df, columns=['event_type'], dtype=float)
    
    # Select features to scale
    # Ensure columns like 'event_type_ACCIDENT', 'event_type_JAM', etc., are included if they exist
    feature_cols = ['latitude', 'longitude', 'severity', 'speed_kmh'] + [col for col in df.columns if col.startswith('event_type_')]
    data_to_scale = df[feature_cols].values
    
    print("Normalizing features...")
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data_to_scale)
    
    print(f"Creating sequences of length {seq_length}...")
    X, y = create_sequences(scaled_data, seq_length)
    
    # Split into train and test sets (80% train, 20% test)
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    
    # Save the processed arrays and scaler configuration info
    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, "X_train.npy"), X_train)
    np.save(os.path.join(output_dir, "y_train.npy"), y_train)
    np.save(os.path.join(output_dir, "X_test.npy"), X_test)
    np.save(os.path.join(output_dir, "y_test.npy"), y_test)
    
    # Save min and max values to easily inverse-transform later without saving the whole scaler object trivially
    np.save(os.path.join(output_dir, "scaler_min.npy"), scaler.data_min_)
    np.save(os.path.join(output_dir, "scaler_range.npy"), scaler.data_range_)
    
    with open(os.path.join(output_dir, "feature_columns.txt"), "w") as f:
        f.write(",".join(feature_cols))
        
    print(f"Preprocessed data saved in {output_dir}")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    return X_train, y_train, X_test, y_test

if __name__ == "__main__":
    if not os.path.exists("data/waze_synthetic_data.csv"):
        print("Data not found. Running generate_data.py first...")
        from generate_data import generate_waze_data
        generate_waze_data()
    preprocess_data()
