# 🧠 Traffic Prediction Model Explanation

This document provides a detailed breakdown of the machine learning architecture used in TrafficSense AI.

## 🏗️ Model Architecture: LSTM (Long Short-Term Memory)
Traffic data is inherently sequential—current congestion levels are heavily dependent on previous time steps. We use an **LSTM Recurrent Neural Network** to capture these temporal dependencies.

### Layer Breakdown
1.  **Input Layer**: Accepts sequences of shape `(batch, time_steps, features)`. We currently use a window of 10 previous data points.
2.  **LSTM Layer (64 units)**: Captures long-term patterns in speed and severity trends.
3.  **LSTM Layer (32 units)**: Refines the features extracted from the first layer.
4.  **Dense Hidden Layer (16 units, ReLU)**: Adds non-linearity and processes the LSTM outputs.
5.  **Output Layer (1 unit, Sigmoid)**: Predicts the probability or severity level of a traffic event.

## 📈 Training Data
- **Source**: Synthetic Waze-like dataset generated for the Pune Metropolitan Region.
- **Features**: Latitude, Longitude, Hour of Day, Day of Week, Previous Speed, Previous Severity, Event Type (Binary Encoded).
- **Preprocessing**: Robust scaling is applied to handle outliers in traffic speed.

## ⚙️ Hyperparameters
- **Optimizer**: Adam (learning rate = 0.001)
- **Loss Function**: Mean Squared Error (MSE)
- **Epochs**: 50 (with Early Stopping)
- **Batch Size**: 32

## 🧪 Evaluation Metrics
The model is evaluated using **Mean Absolute Error (MAE)** to measure the average deviation in predicted speeds vs. actual speeds in the simulation.
