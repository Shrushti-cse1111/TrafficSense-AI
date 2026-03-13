import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import MapPage from './pages/MapPage';
import AnalyticsPage from './pages/AnalyticsPage';
import RoutesPage from './pages/RoutesPage';
import Login from './components/Login';
import Signup from './components/Signup';
import API_BASE from './config';
import './Dashboard.css';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

function AppContent() {
  const [prediction, setPrediction] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  
  const [trends, setTrends] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [heatmapData, setHeatmapData] = useState([]);
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [routes, setRoutes] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [locations, setLocations] = useState([]);

  const getAuthHeader = () => ({
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  });

  const fetchPrediction = async (lat = 18.5204, lon = 73.8567) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/predict?latitude=${lat}&longitude=${lon}`, {}, getAuthHeader());
      setPrediction(response.data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('Error fetching prediction:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/trends`, getAuthHeader());
      setTrends(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchForecast = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/forecast`, getAuthHeader());
      setForecast(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchHeatmap = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/heatmap`, getAuthHeader());
      setHeatmapData(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchRoutes = async (sLat, sLon, dLat, dLon) => {
    try {
      const res = await axios.get(`${API_BASE}/routes/suggest?start_lat=${sLat}&start_lon=${sLon}&end_lat=${dLat}&end_lon=${dLon}`, getAuthHeader());
      setRoutes(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchHotspots = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/hotspots`, getAuthHeader());
      setHotspots(res.data);
    } catch (e) { 
      // Fallback for simulation if hotspots endpoint not in main.py yet
      setHotspots([
        {name: "MG Road", status: "Critical", speed: 12, condition: "Jam"},
        {name: "Hinjewadi Ph 3", status: "Clear", speed: 45, condition: "Fluid"}
      ]);
    }
  };

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/alerts`, getAuthHeader());
      setAlerts(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchLocations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/locations`, getAuthHeader());
      setLocations(res.data);
    } catch (e) { console.error(e); }
  };

  useEffect(() => {
    fetchPrediction();
    fetchAnalytics();
    fetchForecast();
    fetchHeatmap();
    fetchHotspots();
    fetchAlerts();
    fetchLocations();
  }, []);

  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        fetchPrediction();
        fetchAnalytics();
        fetchHeatmap();
        fetchHotspots();
        fetchAlerts();
      }, 10000);
    }
    return () => clearInterval(interval);
  }, [autoRefresh]);

  return (
    <Layout lastUpdated={lastUpdated} hotspots={hotspots} alerts={alerts}>
      <Routes>
        <Route path="/" element={
          <MapPage 
            prediction={prediction} 
            heatmapData={heatmapData} 
            showHeatmap={showHeatmap} 
            onToggleHeatmap={() => setShowHeatmap(!showHeatmap)}
            onLocationSelect={(lat, lon) => fetchPrediction(lat, lon)}
            locations={locations}
          />
        } />
        <Route path="/analytics" element={<AnalyticsPage trends={trends} forecast={forecast} />} />
        <Route path="/routes" element={<RoutesPage routes={routes} onFindRoute={fetchRoutes} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route 
          path="/*" 
          element={
            <ProtectedRoute>
              <AppContent />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
