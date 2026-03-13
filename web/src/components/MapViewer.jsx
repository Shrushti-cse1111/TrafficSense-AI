import React, { useEffect, useRef, useState } from 'react';

const MapViewer = ({ prediction, heatmapData, showHeatmap, onLocationSelect, mapMode = 'dark', is3DMode = false, routeCoords = null }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const directionsRenderer = useRef(null);
  const directionsService = useRef(null);
  const heatmapLayer = useRef(null);
  const carMarker = useRef(null);
  const startMarker = useRef(null);
  const endMarker = useRef(null);
  const animationRef = useRef(null);
  const [position, setPosition] = useState({ lat: 18.5204, lng: 73.8567 }); // Pune Central

  useEffect(() => {
    if (window.google && mapRef.current && !mapInstance.current) {
        mapInstance.current = new window.google.maps.Map(mapRef.current, {
            center: position,
            zoom: 13,
            gestureHandling: 'greedy',
            mapId: '987654321', 
            tilt: 45,
            heading: 0,
            mapTypeId: mapMode === 'satellite' ? 'satellite' : 'roadmap',
            styles: mapMode === 'dark' ? [
                { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
                { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
                { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
                { featureType: "road", elementType: "geometry", stylers: [{ color: "#38414e" }] },
                { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#212a37" }] },
                { featureType: "water", elementType: "geometry", stylers: [{ color: "#17263c" }] },
            ] : []
        });

        // Initialize Directions Handlers
        directionsService.current = new window.google.maps.DirectionsService();
        directionsRenderer.current = new window.google.maps.DirectionsRenderer({
            map: mapInstance.current,
            suppressMarkers: true,
            polylineOptions: {
                strokeColor: '#3b82f6',
                strokeOpacity: 0.8,
                strokeWeight: 6
            }
        });

        // Initialize Heatmap
        heatmapLayer.current = new window.google.maps.visualization.HeatmapLayer({
            data: [],
            map: mapInstance.current,
            radius: 40,
            opacity: 0.8
        });

        const trafficLayer = new window.google.maps.TrafficLayer();
        trafficLayer.setMap(mapInstance.current);

        mapInstance.current.addListener('click', (e) => {
            if (onLocationSelect) {
                onLocationSelect(e.latLng.lat(), e.latLng.lng());
            }
        });
    }
  }, []);

  useEffect(() => {
    if (mapInstance.current && !routeCoords) {
        const zoom = is3DMode ? 18 : 13;
        mapInstance.current.panTo(position);
        mapInstance.current.setZoom(zoom);
        if (is3DMode) {
            mapInstance.current.setTilt(45);
        } else {
            mapInstance.current.setTilt(0);
        }
    }
  }, [position, is3DMode, routeCoords]);

  useEffect(() => {
    if (mapInstance.current) {
        mapInstance.current.setMapTypeId(mapMode === 'satellite' ? 'satellite' : 'roadmap');
    }
  }, [mapMode]);

  useEffect(() => {
    if (prediction && prediction.location) {
        setPosition({ lat: prediction.location.lat, lng: prediction.location.lon });
    }
  }, [prediction]);

  // Update Heatmap data
  useEffect(() => {
    if (heatmapLayer.current) {
        if (showHeatmap && heatmapData && heatmapData.length > 0) {
            const points = heatmapData.map(p => ({
                location: new window.google.maps.LatLng(p.lat, p.lon),
                weight: p.intensity || 1
            }));
            heatmapLayer.current.setData(points);
            heatmapLayer.current.setMap(mapInstance.current);
        } else {
            heatmapLayer.current.setMap(null);
        }
    }
  }, [heatmapData, showHeatmap]);

  const clearRouteMarkers = () => {
        if (carMarker.current) { carMarker.current.setMap(null); carMarker.current = null; }
        if (startMarker.current) { startMarker.current.setMap(null); startMarker.current = null; }
        if (endMarker.current) { endMarker.current.setMap(null); endMarker.current = null; }
        if (animationRef.current) { clearInterval(animationRef.current); animationRef.current = null; }
  };

  useEffect(() => {
    if (directionsService.current && directionsRenderer.current && routeCoords) {
        clearRouteMarkers();
        const origin = { lat: routeCoords.startLat, lng: routeCoords.startLng };
        const destination = { lat: routeCoords.endLat, lng: routeCoords.endLng };

        directionsService.current.route({
            origin: origin,
            destination: destination,
            travelMode: window.google.maps.TravelMode.DRIVING,
        }, (result, status) => {
            if (status === window.google.maps.DirectionsStatus.OK) {
                directionsRenderer.current.setDirections(result);
                startMarker.current = new window.google.maps.Marker({
                    position: origin,
                    map: mapInstance.current,
                    icon: { path: window.google.maps.SymbolPath.CIRCLE, scale: 8, fillColor: '#818cf8', fillOpacity: 1, strokeColor: 'white', strokeWeight: 2 }
                });
                endMarker.current = new window.google.maps.Marker({
                    position: destination,
                    map: mapInstance.current,
                    icon: { path: window.google.maps.SymbolPath.CIRCLE, scale: 8, fillColor: '#ef4444', fillOpacity: 1, strokeColor: 'white', strokeWeight: 2 }
                });

                const routePath = result.routes[0].overview_path;
                carMarker.current = new window.google.maps.Marker({
                    position: routePath[0],
                    map: mapInstance.current,
                    icon: {
                        path: 'M17.402,0H5.643C2.526,0,0,3.467,0,6.584v34.804c0,3.116,2.526,5.644,5.643,5.644h11.759c3.116,0,5.644-2.527,5.644-5.644 V6.584C23.044,3.467,20.518,0,17.402,0z M22.057,14.188v11.665l-2.729,0.351v-4.806L22.057,14.188z M20.625,10.773 c-1.016,3.9-2.219,8.51-2.219,8.51H4.638l-2.222-8.51C2.417,10.773,11.3,7.755,20.625,10.773z M3.748,21.713v4.492l-2.73-0.349 V14.502L3.748,21.713z M1.018,37.938V27.579l2.73,0.343v8.196L1.018,37.938z M2.575,40.882l2.218-3.336h13.771l2.219,3.336H2.575z M19.328,35.805v-7.872l2.729-0.355v10.048L19.328,35.805z',
                        scale: 0.7, fillColor: '#ffffff', fillOpacity: 1, strokeColor: '#000000', strokeWeight: 1, anchor: new window.google.maps.Point(11, 23),
                        rotation: window.google.maps.geometry ? window.google.maps.geometry.spherical.computeHeading(routePath[0], routePath[1]) : 0
                    },
                    zIndex: 999
                });

                let step = 0, numSteps = 500, currentPointIndex = 0;
                animationRef.current = setInterval(() => {
                    if (currentPointIndex >= routePath.length - 1) { clearInterval(animationRef.current); return; }
                    const p1 = routePath[currentPointIndex], p2 = routePath[currentPointIndex + 1];
                    const fraction = step / numSteps;
                    const pos = new window.google.maps.LatLng(p1.lat() + (p2.lat() - p1.lat()) * fraction, p1.lng() + (p2.lng() - p1.lng()) * fraction);
                    carMarker.current.setPosition(pos);
                    if (window.google.maps.geometry) {
                        const icon = carMarker.current.getIcon();
                        icon.rotation = window.google.maps.geometry.spherical.computeHeading(p1, p2);
                        carMarker.current.setIcon(icon);
                    }
                    step += 15;
                    if (step >= numSteps) { step = 0; currentPointIndex++; }
                }, 50);
            }
        });
    } else if (directionsRenderer.current && !routeCoords) {
        directionsRenderer.current.setDirections({routes: []});
        clearRouteMarkers();
    }
    return () => clearRouteMarkers();
  }, [routeCoords]);

  return (
    <div className="map-container-google" style={{ height: '100%', width: '100%' }}>
      <div ref={mapRef} style={{ height: '100%', width: '100%', borderRadius: '12px', overflow: 'hidden' }} />
    </div>
  );
};

export default MapViewer;
