import React, { useState } from 'react';
import RouteSuggestions from '../components/RouteSuggestions';
import MapViewer from '../components/MapViewer';
import { motion } from 'framer-motion';
import { MapPin, ArrowRight } from 'lucide-react';

const RoutesPage = ({ routes, onFindRoute }) => {
    const [source, setSource] = useState('Hinjewadi Phase 1');
    const [destination, setDestination] = useState('Koregaon Park');
    const [currentRouteCoords, setCurrentRouteCoords] = useState(null);

    const handleFindRoute = () => {
        // Mocking coordination lookup for Pune locations
        const locations = {
            'hinjewadi': [18.5913, 73.7389],
            'hinjewadi phase 1': [18.5913, 73.7389],
            'koregaon park': [18.5362, 73.8940],
            'baner': [18.5597, 73.7799],
            'viman nagar': [18.5679, 73.9143],
            'shivaji nagar': [18.5308, 73.8475],
            'mg road': [18.5173, 73.8767]
        };

        const sCoord = locations[source.toLowerCase()] || [18.52, 73.85];
        const dCoord = locations[destination.toLowerCase()] || [18.55, 73.90];

        // Trigger the AI query
        onFindRoute(sCoord[0], sCoord[1], dCoord[0], dCoord[1]);

        // Tell the MapViewer to draw the physical lines
        setCurrentRouteCoords({
            startLat: sCoord[0],
            startLng: sCoord[1],
            endLat: dCoord[0],
            endLng: dCoord[1]
        });
    };

    return (
        <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="page-container routes-page"
        >
            <div className="routes-header">
                <h2>Smart Route AI Planner</h2>
                <p>Traffic-aware navigation for Pune commuters</p>
            </div>

            <div className="routes-split" style={{ display: 'flex', gap: '2rem', height: 'calc(100vh - 160px)' }}>
                {/* Left Sidebar for Inputs and Suggestions */}
                <div className="routes-content" style={{ width: '380px', flexShrink: 0, display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="route-picker glass-card">
                        <div className="route-input">
                            <MapPin size={18} color="#818cf8" />
                            <input 
                                type="text" 
                                placeholder="Starting from..." 
                                value={source}
                                onChange={(e) => setSource(e.target.value)}
                            />
                        </div>
                        <div className="route-divider">
                            <ArrowRight size={16} />
                        </div>
                        <div className="route-input">
                            <MapPin size={18} color="#ef4444" />
                            <input 
                                type="text" 
                                placeholder="Destination..." 
                                value={destination}
                                onChange={(e) => setDestination(e.target.value)}
                            />
                        </div>
                        <button className="optimize-btn" onClick={handleFindRoute}>
                            Find Fastest Route
                        </button>
                    </div>

                    <div className="suggestions-list" style={{ flex: 1, overflowY: 'auto' }}>
                        {currentRouteCoords && (
                            <div className="route-summary-pill neon-glass" style={{ marginBottom: '1rem' }}>
                                <span>Optimizing: {source} → {destination}</span>
                            </div>
                        )}
                        <RouteSuggestions routes={routes} />
                    </div>
                </div>

                {/* Right Area for Live Map Rendering */}
                <div className="routes-map glass-card" style={{ flex: 1, padding: '4px' }}>
                    <MapViewer routeCoords={currentRouteCoords} />
                </div>
            </div>
        </motion.div>
    );
};

export default RoutesPage;
