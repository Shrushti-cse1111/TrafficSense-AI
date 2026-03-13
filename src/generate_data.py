import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_waze_data(num_records=10000, output_path="data/waze_synthetic_data.csv"):
    """
    Generates a synthetic dataset mimicking Waze Open Dataset traffic events.
    """
    np.random.seed(42)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Simulate a bounding box for Pune City, India
    lat_min, lat_max = 18.45, 18.60
    lon_min, lon_max = 73.75, 73.95
    
    # Time settings
    start_time = datetime(2023, 1, 1, 0, 0, 0)
    
    # Event types and severities
    event_types = ['JAM', 'ACCIDENT', 'WEATHERHAZARD', 'ROAD_CLOSED']
    severities = [1, 2, 3, 4] # 1: minor, 4: severe
    
    data = []
    
    current_time = start_time
    for _ in range(num_records):
        # Time increment (average 5 minutes between events)
        time_increment = timedelta(minutes=np.random.exponential(scale=5))
        current_time += time_increment
        
        # Determine temporal weighting (Morning Peak: 7-9, Evening Peak: 16-19, Weekends: quieter)
        hour = current_time.hour
        is_weekend = current_time.weekday() >= 5
        
        # Base probability weight for incidents
        load_factor = 1.0
        if 7 <= hour <= 9 or 16 <= hour <= 19:
            load_factor = 2.5 if not is_weekend else 1.2
        elif is_weekend:
            load_factor = 0.6
            
        # Location
        lat = np.random.uniform(lat_min, lat_max)
        lon = np.random.uniform(lon_min, lon_max)
        
        # Type and severity (JAM more likely during peaks)
        p_jam = 0.7 * load_factor
        p_others = (1 - p_jam) / 3 if p_jam < 1 else 0 # Simple normalization
        if p_jam >= 1: p_jam, p_others = 0.9, 0.033
        
        event_type = np.random.choice(event_types, p=[p_jam, 0.1, 0.1, 0.1])
        
        if event_type == 'JAM':
            # Higher severity during peaks
            p_sev = [0.4, 0.3, 0.2, 0.1]
            if load_factor > 1.5: p_sev = [0.1, 0.2, 0.4, 0.3]
            severity = np.random.choice(severities, p=p_sev)
        else:
            severity = np.random.choice(severities)
            
        # Simulate traffic speed (km/h) based on severity and load
        base_speed = 60 if not is_weekend else 70
        if severity == 1:
            speed = np.random.uniform(base_speed*0.6, base_speed*0.8)
        elif severity == 2:
            speed = np.random.uniform(base_speed*0.4, base_speed*0.6)
        elif severity == 3:
            speed = np.random.uniform(base_speed*0.2, base_speed*0.4)
        else:
            speed = np.random.uniform(0, base_speed*0.2)
            
        data.append({
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'latitude': lat,
            'longitude': lon,
            'event_type': event_type,
            'severity': severity,
            'speed_kmh': speed,
            'day_type': 'Weekend' if is_weekend else 'Weekday',
            'is_peak': 'Yes' if (7 <= hour <= 9 or 16 <= hour <= 19) else 'No'
        })
        
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} synthetic Waze records at {output_path}")

if __name__ == "__main__":
    generate_waze_data()
