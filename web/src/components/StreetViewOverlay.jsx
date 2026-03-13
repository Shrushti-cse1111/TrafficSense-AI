import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';

const StreetViewOverlay = ({ lat, lon, onClose }) => {
    const panoramaRef = useRef(null);

    useEffect(() => {
        if (window.google && window.google.maps) {
            new window.google.maps.StreetViewPanorama(panoramaRef.current, {
                position: { lat: parseFloat(lat), lng: parseFloat(lon) },
                pov: { heading: 165, pitch: 0 },
                zoom: 1,
                addressControl: true,
                showRoadLabels: true,
                motionTracking: true,
                motionTrackingControl: true
            });
        }
    }, [lat, lon]);

    return (
        <div className="street-view-container glass-card">
            <div className="street-view-header">
                <h3>360° Real Area View - Pune</h3>
                <button onClick={onClose} className="close-sv-btn">
                    <X size={20} />
                </button>
            </div>
            <div ref={panoramaRef} className="panorama-view"></div>
            <div className="street-view-footer">
                <p>Use your mouse to rotate 360 degrees</p>
            </div>
        </div>
    );
};

export default StreetViewOverlay;
