import { useEffect, useRef, useState } from 'react';
import { MapPin, Navigation, Cloud, Wind, Thermometer, Plane as PlaneIcon } from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function RouteMap({ waypoints, originData, destData, weatherData }) {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [mapReady, setMapReady] = useState(false);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    // Initialize map with beautiful satellite view
    map.current = L.map(mapContainer.current, {
      center: [20, 0],
      zoom: 2,
      zoomControl: true,
      scrollWheelZoom: true
    });

    // Add beautiful tile layer (Esri World Imagery - Free!)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Esri',
      maxZoom: 18
    }).addTo(map.current);

    // Add labels overlay
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Esri',
      maxZoom: 18
    }).addTo(map.current);

    setMapReady(true);

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!map.current || !mapReady || !waypoints || waypoints.length < 2) {
      console.log('Map not ready or no waypoints:', { mapReady, waypoints });
      return;
    }
    if (!originData || !destData) {
      console.log('No airport data:', { originData, destData });
      return;
    }

    console.log('Drawing route with data:', { originData, destData, waypoints });

    // Clear existing layers
    map.current.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline || layer instanceof L.Circle) {
        map.current.removeLayer(layer);
      }
    });

    const originCoords = [originData.latitude, originData.longitude];
    const destCoords = [destData.latitude, destData.longitude];

    // Custom origin marker (blue)
    const originIcon = L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border: 4px solid white;
          border-radius: 50%;
          box-shadow: 0 4px 12px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
            <path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/>
          </svg>
        </div>
      `,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });

    // Custom destination marker (pink)
    const destIcon = L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          border: 4px solid white;
          border-radius: 50%;
          box-shadow: 0 4px 12px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
            <circle cx="12" cy="12" r="8"/>
          </svg>
        </div>
      `,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });

    // Add origin marker
    const originMarker = L.marker(originCoords, { icon: originIcon })
      .addTo(map.current)
      .bindPopup(`
        <div style="padding: 12px; font-family: system-ui; min-width: 200px;">
          <div style="font-size: 20px; font-weight: bold; color: #667eea; margin-bottom: 6px;">
            ${originData.iata_code}
          </div>
          <div style="color: #333; font-size: 14px; font-weight: 600; margin-bottom: 4px;">
            ${originData.name}
          </div>
          <div style="color: #666; font-size: 12px;">
            ${originData.city}, ${originData.country}
          </div>
          <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; color: #999; font-size: 11px;">
            📍 ${originData.latitude.toFixed(4)}°, ${originData.longitude.toFixed(4)}°
          </div>
        </div>
      `);

    // Add destination marker
    const destMarker = L.marker(destCoords, { icon: destIcon })
      .addTo(map.current)
      .bindPopup(`
        <div style="padding: 12px; font-family: system-ui; min-width: 200px;">
          <div style="font-size: 20px; font-weight: bold; color: #f5576c; margin-bottom: 6px;">
            ${destData.iata_code}
          </div>
          <div style="color: #333; font-size: 14px; font-weight: 600; margin-bottom: 4px;">
            ${destData.name}
          </div>
          <div style="color: #666; font-size: 12px;">
            ${destData.city}, ${destData.country}
          </div>
          <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; color: #999; font-size: 11px;">
            📍 ${destData.latitude.toFixed(4)}°, ${destData.longitude.toFixed(4)}°
          </div>
        </div>
      `);

    // Create animated flight path with arc
    const latlngs = [];
    const steps = 100;
    
    for (let i = 0; i <= steps; i++) {
      const fraction = i / steps;
      const lat = originData.latitude + (destData.latitude - originData.latitude) * fraction;
      const lng = originData.longitude + (destData.longitude - originData.longitude) * fraction;
      latlngs.push([lat, lng]);
    }

    // Draw the route line with gradient effect
    const routeLine = L.polyline(latlngs, {
      color: '#667eea',
      weight: 4,
      opacity: 0.8,
      dashArray: '10, 10',
      smoothFactor: 1
    }).addTo(map.current);

    // Add pulsing circles at endpoints
    const originCircle = L.circle(originCoords, {
      color: '#667eea',
      fillColor: '#667eea',
      fillOpacity: 0.2,
      radius: 100000,
      weight: 2
    }).addTo(map.current);

    const destCircle = L.circle(destCoords, {
      color: '#f5576c',
      fillColor: '#f5576c',
      fillOpacity: 0.2,
      radius: 100000,
      weight: 2
    }).addTo(map.current);

    // Fit map to show entire route
    const bounds = L.latLngBounds([originCoords, destCoords]);
    map.current.fitBounds(bounds, { padding: [80, 80], maxZoom: 6 });

    // Animate flight path
    let pathIndex = 0;
    const animatePath = () => {
      if (pathIndex < latlngs.length) {
        const currentPath = latlngs.slice(0, pathIndex + 1);
        routeLine.setLatLngs(currentPath);
        pathIndex += 2;
        requestAnimationFrame(animatePath);
      }
    };
    setTimeout(() => animatePath(), 500);

  }, [mapReady, waypoints, originData, destData]);

  return (
    <div className="bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100">
      {/* Header */}
      <div className="p-6 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-purple-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-3 rounded-xl shadow-lg">
              <Navigation className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-900">Interactive Flight Route</h3>
              <p className="text-sm text-gray-600 mt-1">Satellite view with real-time visualization</p>
            </div>
          </div>
          
          {weatherData && (
            <div className="flex items-center space-x-4 bg-white rounded-xl px-6 py-3 shadow-md">
              <div className="flex items-center space-x-2">
                <Cloud className="w-5 h-5 text-blue-500" />
                <div>
                  <div className="text-xs text-gray-500 font-semibold">Weather</div>
                  <div className="text-sm font-bold text-gray-900">{weatherData.condition}</div>
                </div>
              </div>
              <div className="w-px h-8 bg-gray-200"></div>
              <div className="flex items-center space-x-2">
                <Wind className="w-5 h-5 text-indigo-500" />
                <div>
                  <div className="text-xs text-gray-500 font-semibold">Wind</div>
                  <div className="text-sm font-bold text-gray-900">{weatherData.windSpeed} km/h</div>
                </div>
              </div>
              <div className="w-px h-8 bg-gray-200"></div>
              <div className="flex items-center space-x-2">
                <Thermometer className="w-5 h-5 text-orange-500" />
                <div>
                  <div className="text-xs text-gray-500 font-semibold">Temp</div>
                  <div className="text-sm font-bold text-gray-900">{weatherData.temperature}°C</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Map Container */}
      <div className="relative">
        {!waypoints || waypoints.length < 2 ? (
          <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-20 flex flex-col items-center justify-center min-h-[550px]">
            <div className="bg-white/90 backdrop-blur-sm rounded-3xl p-12 shadow-2xl text-center max-w-md">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
                <MapPin className="w-10 h-10 text-white" />
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-3">
                Ready for Takeoff!
              </h4>
              <p className="text-gray-600 text-base leading-relaxed">
                Select departure and arrival airports, then click optimize to see the beautiful satellite route visualization with real-time weather data
              </p>
            </div>
          </div>
        ) : (
          <div ref={mapContainer} className="h-[550px] w-full" />
        )}
      </div>

      {/* Airport Info Footer */}
      {waypoints && waypoints.length >= 2 && originData && destData && (
        <div className="p-6 bg-gradient-to-r from-indigo-50 to-purple-50 border-t border-gray-100">
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white rounded-2xl p-5 shadow-md hover:shadow-xl transition-shadow">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-4 h-4 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg"></div>
                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Departure</span>
              </div>
              <div className="text-3xl font-black text-gray-900 mb-2">{originData.iata_code}</div>
              <div className="text-sm font-semibold text-gray-700">{originData.name}</div>
              <div className="text-xs text-gray-500 mt-1">{originData.city}, {originData.country}</div>
            </div>
            
            <div className="bg-white rounded-2xl p-5 shadow-md hover:shadow-xl transition-shadow">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-4 h-4 rounded-full bg-gradient-to-r from-pink-500 to-red-500 shadow-lg"></div>
                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Arrival</span>
              </div>
              <div className="text-3xl font-black text-gray-900 mb-2">{destData.iata_code}</div>
              <div className="text-sm font-semibold text-gray-700">{destData.name}</div>
              <div className="text-xs text-gray-500 mt-1">{destData.city}, {destData.country}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}