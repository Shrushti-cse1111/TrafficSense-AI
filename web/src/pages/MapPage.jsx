import React, { useState } from 'react';
import MapViewer from '../components/MapViewer';
import StreetViewOverlay from '../components/StreetViewOverlay';
import { motion } from 'framer-motion';
import { AlertTriangle, Layers, Moon, Sun, Globe, Search, Compass } from 'lucide-react';

const MapPage = ({ prediction, heatmapData, showHeatmap, onToggleHeatmap, onLocationSelect, locations = [] }) => {
    const [mapMode, setMapMode] = useState('dark');
    const [searchQuery, setSearchQuery] = useState('');
    const [is3DMode, setIs3DMode] = useState(false);
    const [showStreetView, setShowStreetView] = useState(false);

    const handleSearch = (e) => {
        e.preventDefault();
        
        const q = searchQuery.toLowerCase().trim();
        const found = locations.find(loc => loc.name.toLowerCase() === q);
        
        if (found) {
            console.log(`Searching for ${searchQuery} at ${found.lat}, ${found.lon}`);
            onLocationSelect(found.lat, found.lon);
            setIs3DMode(true);
            setMapMode('satellite');
        } else {
            console.warn(`Location not found: ${searchQuery}`);
            const options = locations.map(l => l.name).join(', ');
            alert(`Location not found in Pune database. Try: ${options}`);
        }
    };

    return (
        <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="page-container map-page-container"
        >
            <div className={`map-view-wrapper ${is3DMode ? 'perspective-3d' : ''}`}>
                <MapViewer 
                    prediction={prediction} 
                    heatmapData={heatmapData} 
                    showHeatmap={showHeatmap}
                    onLocationSelect={onLocationSelect}
                    mapMode={mapMode}
                    is3DMode={is3DMode}
                />
                
                {showStreetView && prediction && (
                    <StreetViewOverlay 
                        lat={prediction.latitude} 
                        lon={prediction.longitude} 
                        onClose={() => setShowStreetView(false)} 
                    />
                )}

                <div className="map-search-bar glass-card">
                    <form onSubmit={handleSearch}>
                        <Search size={18} className="search-icon" />
                        <input 
                            type="text" 
                            placeholder="Search Pune Location..." 
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </form>
                </div>

                <div className="map-controls-panel minimized glass-card">
                    <button 
                        className={`map-mode-btn ${showStreetView ? 'active' : ''}`}
                        onClick={() => setShowStreetView(!showStreetView)}
                        title="360° Street View"
                    >
                        <Compass size={18} />
                    </button>

                    <div className="v-divider"></div>

                    <button 
                        className={`map-mode-btn ${mapMode === 'dark' ? 'active' : ''}`}
                        onClick={() => { setMapMode('dark'); setIs3DMode(false); setShowStreetView(false); }}
                        title="Dark Mode"
                    >
                        <Moon size={18} />
                    </button>
                    <button 
                        className={`map-mode-btn ${mapMode === 'light' ? 'active' : ''}`}
                        onClick={() => { setMapMode('light'); setIs3DMode(false); setShowStreetView(false); }}
                        title="Light Mode"
                    >
                        <Sun size={18} />
                    </button>
                    <button 
                        className={`map-mode-btn ${mapMode === 'satellite' ? 'active' : ''}`}
                        onClick={() => setMapMode('satellite')}
                        title="Satellite Mode (3D Compatible)"
                    >
                        <Globe size={18} />
                    </button>
                    
                    <div className="v-divider"></div>
                    
                    <button 
                        className={`map-mode-btn ${showHeatmap ? 'active' : ''}`}
                        onClick={onToggleHeatmap}
                        title="Toggle Heatmap"
                    >
                        <Layers size={18} />
                    </button>
                </div>

                {prediction?.severity >= 3 && !showStreetView && (
                    <div className="map-alert-overlay">
                        <AlertTriangle size={24} color="#ef4444" />
                        <span>High Traffic Alert: {prediction.traffic_level} near Pune City</span>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default MapPage;
