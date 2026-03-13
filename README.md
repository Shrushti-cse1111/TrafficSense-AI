# 🚦 TrafficSense AI

An AI-powered Intelligent Traffic Prediction and Management System designed for the Pune Metropolitan Region. The system uses simulated traffic data and a deep learning approach (Recurrent Neural Networks via Keras) to forecast traffic severity, provide smart route recommendations, and detect hotspots.

## ✨ Advanced Features Included

This project includes a comprehensive suite of advanced traffic management features:
1. **Pune Location Search**: Search across major localities in Pune (Baner, Hinjewadi, MG Road, etc.).
2. **Smart Route Recommendation**: Intelligent A-to-B routing that suggests the fastest path while avoiding heavy congestion.
3. **Traffic Heatmaps**: Visualizes congestion density across the city.
4. **Live Traffic Hotspots**: Identifies specific areas experiencing abnormal traffic conditions.
5. **AI Traffic Prediction**: Deep learning models predict upcoming traffic incidents.
6. **Traffic Alerts**: Real-time alerts for accidents, weather impacts, and peak hours.
7. **Traffic Analytics Dashboard**: Interactive charts tracking hourly speed trends.
8. **Peak Hour & Accident Detection**: Flagging anomalous traffic stops.
9. **Traffic Forecast Timeline**: A 12-hour futuristic outlook on city-wide traffic severity.

---

## 🏗️ Project Structure
The repository is divided into 3 main components:
- `api/`: FastAPI Backend serving predictions and analytics to the frontend.
- `web/`: React + Vite Frontend application featuring an interactive Map dashboard.
- `src/` & `models/`: The core Machine Learning pipeline where data is generated, preprocessed, and the RNN model is trained.

---

## 🚀 Getting Started

To run the full stack application, you need to start both the Python backend and the Node.js frontend.

### 1. Start the Backend API (FastAPI)
The backend requires Python and serves the machine learning model and data streams on port 8000.

```bash
# Navigate to the API folder
cd api

# Install requirements
pip install -r ../requirements.txt

# Run the FastAPI server
python main.py
```
*(The API will be available at `http://localhost:8000`).*

### 2. Start the Frontend Web App (React + Vite)
The frontend requires Node.js and npm. It connects to the backend to visualize the data.

```bash
# Open a NEW terminal side-by-side
# Navigate to the web folder
cd web

# Install Node dependencies
npm install

# Start the dev server
npm run dev
```
*(The Web App will be available at `http://localhost:5173`).*

---

## 🗺️ Google Maps Error Note
If you see a "Google Maps cannot load correctly" or "Oops! Something went wrong" error on the map, this means the placeholder API key in `web/.env` is inactive or lacks billing. 

**To use the map fully (including 3D mode and Street View):**
Insert your valid Google Cloud API key into `web/.env`:
`VITE_GOOGLE_MAPS_API_KEY=your_real_key_here`

---

## 🧠 Model Training (Optional)
If you wish to retrain the neural network on fresh synthetic data:
```bash
python src/generate_data.py        # 1. Generate new Waze-like data
python src/data_preprocessing.py   # 2. Process sequences
python src/train.py                # 3. Train the Keras RNN Model
```
