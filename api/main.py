from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import os
import sys
import random
import pandas as pd
from datetime import datetime
from pydantic import BaseModel

# Add parent directory to path to import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.predict import predict as model_predict

app = FastAPI(title="TrafficSense AI API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock User Database for simulation
USERS = {"admin": "password123"}

class AuthRequest(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "TrafficSense AI API is running"}

@app.post("/auth/signup")
async def signup(req: AuthRequest):
    if req.username in USERS:
        raise HTTPException(status_code=400, detail="User already exists")
    USERS[req.username] = req.password
    return {"message": "User created successfully"}

@app.post("/auth/login")
async def login(req: AuthRequest):
    if req.username not in USERS or USERS[req.username] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": f"mock-jwt-token-{req.username}", "username": req.username}

@app.post("/predict")
async def get_prediction(latitude: float = None, longitude: float = None):
    try:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "traffic_model_final.h5")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model file not found. Please train the model first.")
            
        prediction = model_predict()
        if prediction is None:
            raise HTTPException(status_code=500, detail="Prediction failed")
        
        if latitude and longitude:
            prediction['latitude'] = latitude
            prediction['longitude'] = longitude
            
        weathers = ["Clear", "Rainy", "Foggy", "Overcast", "Mist"]
        road_states = ["Normal", "Wet", "Slippery", "Construction", "Narrowed"]
        
        formatted_prediction = {}
        for k, v in prediction.items():
            if isinstance(v, np.generic):
                formatted_prediction[k] = v.item()
            else:
                formatted_prediction[k] = v
        
        formatted_prediction["weather"] = random.choice(weathers)
        formatted_prediction["road_condition"] = random.choice(road_states)
        formatted_prediction["confidence"] = round(random.uniform(0.85, 0.98), 2)
        formatted_prediction["timestamp"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
        return formatted_prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/trends")
async def get_trends():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        trends = df.groupby('hour')['speed_kmh'].mean().reset_index()
        return trends.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/heatmap")
async def get_heatmap():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path).tail(500)
        heatmap_data = []
        for _, row in df.iterrows():
            heatmap_data.append({"lat": row['latitude'], "lon": row['longitude'], "intensity": row['severity'] / 4.0})
        return heatmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/locations")
async def get_locations():
    return [
        {"name": "Baner", "lat": 18.5597, "lon": 73.7799},
        {"name": "Hinjewadi", "lat": 18.5913, "lon": 73.7389},
        {"name": "MG Road", "lat": 18.5173, "lon": 73.8767},
        {"name": "Shivaji Nagar", "lat": 18.5308, "lon": 73.8475},
        {"name": "Swargate", "lat": 18.5029, "lon": 73.8565},
        {"name": "Viman Nagar", "lat": 18.5679, "lon": 73.9143},
        {"name": "Kothrud", "lat": 18.5074, "lon": 73.8077},
        {"name": "Aundh", "lat": 18.5580, "lon": 73.8075},
        {"name": "Airport", "lat": 18.5822, "lon": 73.9197},
        {"name": "Magarpatta", "lat": 18.5134, "lon": 73.9242},
        {"name": "Kharadi", "lat": 18.5515, "lon": 73.9348}
    ]

@app.get("/analytics/forecast")
async def get_forecast():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        hourly_speeds = df.groupby('hour')['speed_kmh'].mean().to_dict()
        
        from datetime import timedelta
        current_time = datetime.now()
        next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        forecast = []
        for i in range(12):
            time_slot = next_hour + timedelta(hours=i)
            hour = time_slot.hour
            base_speed = hourly_speeds.get(hour, 40)
            speed = max(5, base_speed + random.uniform(-10, 10))
            severity = "Critical" if speed < 20 else "Moderate" if speed < 35 else "Clear"
            forecast.append({
                "time": time_slot.strftime("%I %p"),
                "hour_24": hour,
                "predicted_speed": round(speed),
                "severity": severity
            })
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts")
async def get_alerts():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        recent_severe = df[(df['severity'] >= 3) | (df['event_type'].isin(['ACCIDENT', 'WEATHERHAZARD']))].tail(5)
        alerts = []
        for _, row in recent_severe.iterrows():
            loc_names = ["Hinjewadi", "Baner", "Shivaji Nagar", "MG Road", "Viman Nagar"]
            alerts.append({
                "id": str(random.randint(1000, 9999)),
                "type": row['event_type'].capitalize(),
                "location": random.choice(loc_names),
                "description": f"Average speed dropped to {row['speed_kmh']:.1f} km/h due to {row['event_type']}.",
                "severity": "critical" if row['severity'] == 4 else "high" if row['severity'] == 3 else "moderate",
                "time": "Recently"
            })
        return alerts[::-1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hotspots")
async def get_hotspots():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path).tail(2000)
        df['lat_bin'] = df['latitude'].round(2)
        df['lon_bin'] = df['longitude'].round(2)
        grouped = df.groupby(['lat_bin', 'lon_bin']).agg(avg_speed=('speed_kmh', 'mean')).reset_index()
        worst_areas = grouped.sort_values(by='avg_speed', ascending=True).head(3)
        hotspots = []
        mock_names = ["Katraj Bypass", "Senapati Bapat Road", "Wagholi Highway", "Koregaon Park"]
        for i, row in worst_areas.iterrows():
            speed = row['avg_speed']
            hotspots.append({
                "name": mock_names[i % len(mock_names)],
                "status": "CRITICAL" if speed < 15 else "HIGH" if speed < 25 else "MODERATE",
                "speed": round(speed),
                "condition": "Severe Jam" if speed < 15 else "Heavy Traffic" if speed < 25 else "Slow Moving"
            })
        return hotspots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes/suggest")
async def get_route_suggestions(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        dist_km = ((start_lat - end_lat)**2 + (start_lon - end_lon)**2)**0.5 * 111.0
        
        routes = [
            {"id": "r1", "name": "Direct Highway", "time_mins": int(dist_km * 1.1 / 25 * 60), "is_fastest": False},
            {"id": "r2", "name": "Internal Roads", "time_mins": int(dist_km * 1.3 / 30 * 60), "is_fastest": False},
            {"id": "r3", "name": "Outer Bypass", "time_mins": int(dist_km * 1.6 / 60 * 60), "is_fastest": False}
        ]
        
        fastest = min(routes, key=lambda x: x["time_mins"])
        fastest["is_fastest"] = True
        
        for r in routes:
            r["color"] = "#10b981" if r["is_fastest"] else "#f59e0b" if r["time_mins"] - fastest["time_mins"] < 10 else "#ef4444"
            r["congestion"] = "Low" if r["is_fastest"] else "Medium"
                
        return sorted(routes, key=lambda x: x["time_mins"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
