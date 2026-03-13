from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import os
import sys

# Add parent directory to path to import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
import pandas as pd
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

@app.get("/")
async def root():
    return {"message": "TrafficSense AI API is running"}

@app.post("/predict")
async def get_prediction(latitude: float = None, longitude: float = None):
    """
    Returns a predicted traffic event. 
    If coordinates are provided, it simulates a prediction for that specific location.
    """
    try:
        # Use path relative to the script's directory
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "traffic_model_final.h5")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail=f"Model file not found. Please train the model first.")
            
        prediction = model_predict()
        if prediction is None:
            raise HTTPException(status_code=500, detail="Prediction failed")
        
        # Override with requested coordinates if provided (simulation)
        if latitude and longitude:
            prediction['latitude'] = latitude
            prediction['longitude'] = longitude
            
        # Add simulated rich data
        weathers = ["Clear", "Rainy", "Foggy", "Overcast", "Mist"]
        road_states = ["Normal", "Wet", "Slippery", "Construction", "Narrowed"]
        
        formatted_prediction = {}
        for k, v in prediction.items():
            if isinstance(v, np.generic):
                formatted_prediction[k] = v.item()
            else:
                formatted_prediction[k] = v
        
        # Inject simulated fields
        formatted_prediction["weather"] = random.choice(weathers)
        formatted_prediction["road_condition"] = random.choice(road_states)
        formatted_prediction["confidence"] = round(random.uniform(0.85, 0.98), 2)
        from datetime import datetime
        formatted_prediction["timestamp"] = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
        return formatted_prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/trends")
async def get_trends():
    """Returns hourly traffic speed trends based on historical data."""
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
    """Returns coordinates and intensity for heatmap visualization."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path).tail(500) # Latest 500 for performance
        heatmap_data = []
        for _, row in df.iterrows():
            heatmap_data.append([row['latitude'], row['longitude'], row['severity'] / 4.0])
        return heatmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/locations")
async def get_locations():
    """Returns a list of popular Pune locations for the search bar."""
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
    """Returns simulated traffic forecast for the next 12 hours based on data trends."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        
        # Calculate historical average for each hour to form a base
        hourly_speeds = df.groupby('hour')['speed_kmh'].mean().to_dict()
        
        from datetime import datetime, timedelta
        current_time = datetime.now()
        next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        forecast = []
        for i in range(12):
            time_slot = next_hour + timedelta(hours=i)
            hour = time_slot.hour
            
            # Predict based on historical average + some random variance representing current conditions
            base_speed = hourly_speeds.get(hour, 40)
            
            speed_variance = random.uniform(-10, 10)
            speed = max(5, base_speed + speed_variance)
            
            if speed < 20:
                severity = "Critical"
            elif speed < 35:
                severity = "Moderate"
            else:
                severity = "Clear"
                
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
    """Returns active traffic alerts based on recent severe events in the dataset."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        
        # Sort by latest and filter severe
        recent_severe = df[(df['severity'] >= 3) | (df['event_type'].isin(['ACCIDENT', 'WEATHERHAZARD']))].tail(5)
        
        alerts = []
        for _, row in recent_severe.iterrows():
            etype = row['event_type'].capitalize()
            
            # Map coordinates to a mock name
            loc_names = ["Hinjewadi", "Baner", "Shivaji Nagar", "MG Road", "Viman Nagar"]
            loc = random.choice(loc_names)
            
            severity_str = "critical" if row['severity'] == 4 else "high" if row['severity'] == 3 else "moderate"
            desc = f"Average speed dropped to {row['speed_kmh']:.1f} km/h due to {row['event_type']}."
            
            alerts.append({
                "id": str(random.randint(1000, 9999)),
                "type": etype,
                "location": loc,
                "description": desc,
                "severity": severity_str,
                "time": "Recently"
            })
        return alerts[::-1] # Newest first
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hotspots")
async def get_hotspots():
    """Identifies highly congested areas by finding clusters with lowest average speed."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path).tail(2000) # Look at recent data
        
        # Bin latitudes and longitudes to simulate "areas"
        df['lat_bin'] = df['latitude'].round(2)
        df['lon_bin'] = df['longitude'].round(2)
        
        # Group by area to find average speeds
        grouped = df.groupby(['lat_bin', 'lon_bin']).agg(
            avg_speed=('speed_kmh', 'mean'),
            incident_count=('severity', 'count')
        ).reset_index()
        
        # Sort by lowest speed
        worst_areas = grouped.sort_values(by='avg_speed', ascending=True).head(3)
        
        hotspots = []
        mock_names = ["Katraj Bypass", "Senapati Bapat Road", "Wagholi Highway", "Koregaon Park"]
        for i, row in worst_areas.iterrows():
            speed = row['avg_speed']
            status = "CRITICAL" if speed < 15 else "HIGH" if speed < 25 else "MODERATE"
            condition = "Severe Jam" if speed < 15 else "Heavy Traffic" if speed < 25 else "Slow Moving"
            
            hotspots.append({
                "name": mock_names[i % len(mock_names)],
                "status": status,
                "speed": round(speed),
                "condition": condition
            })
        return hotspots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes/suggest")
async def get_route_suggestions(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    """Suggests alternative routes based on traffic intensity in the data."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "waze_synthetic_data.csv")
        df = pd.read_csv(data_path)
        
        # Calculate a rough bounding box between start and end
        min_lat, max_lat = min(start_lat, end_lat), max(start_lat, end_lat)
        min_lon, max_lon = min(start_lon, end_lon), max(start_lon, end_lon)
        
        # Add a small buffer to the box
        buffer = 0.05
        route_data = df[(df['latitude'] >= min_lat - buffer) & (df['latitude'] <= max_lat + buffer) &
                        (df['longitude'] >= min_lon - buffer) & (df['longitude'] <= max_lon + buffer)]
        
        # Overall average speed of the area
        area_speed = route_data['speed_kmh'].mean() if len(route_data) > 0 else 40
        
        # Calculate rough base distance (1 degree is roughly 111km)
        dist_km = ((start_lat - end_lat)**2 + (start_lon - end_lon)**2)**0.5 * 111.0
        
        # Route 1: Direct (Highway proxy) - slightly faster base distance, but susceptible to area average speed
        speed1 = max(5, area_speed * 1.2)
        time1 = (dist_km * 1.1 / speed1) * 60 # mins
        
        # Route 2: Internal/Alternative - slightly longer distance, speed may be less affected by major jams
        speed2 = max(5, 30.0 + random.uniform(-5, 5)) 
        time2 = (dist_km * 1.3 / speed2) * 60
        
        # Route 3: Bypass - much longer distance, much faster speed
        speed3 = max(5, 60.0 + random.uniform(-10, 10))
        time3 = (dist_km * 1.6 / speed3) * 60
        
        routes = [
            {"id": "r1", "name": "Direct Highway", "time_mins": int(time1), "congestion": "High" if speed1 < 20 else "Low", "color": "#ef4444" if speed1 < 20 else "#10b981", "is_fastest": False},
            {"id": "r2", "name": "Internal Roads", "time_mins": int(time2), "congestion": "High" if speed2 < 20 else "Low", "color": "#ef4444" if speed2 < 20 else "#10b981", "is_fastest": False},
            {"id": "r3", "name": "Outer Bypass", "time_mins": int(time3), "congestion": "High" if speed3 < 20 else "Low", "color": "#ef4444" if speed3 < 20 else "#10b981", "is_fastest": False}
        ]
        
        # Find fastest
        fastest = min(routes, key=lambda x: x["time_mins"])
        fastest["is_fastest"] = True
        
        # Make colors logical
        for r in routes:
            if r["time_mins"] == fastest["time_mins"]:
                r["color"] = "#10b981" # Green
                r["congestion"] = "Low"
            else:
                r["color"] = "#f59e0b" if r["time_mins"] - fastest["time_mins"] < 10 else "#ef4444"
                r["congestion"] = "Medium" if r["time_mins"] - fastest["time_mins"] < 10 else "High"
                
        routes.sort(key=lambda x: x["time_mins"])
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
