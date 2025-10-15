import { useState, useEffect } from 'react';
import { Plane, Leaf, Clock, Fuel, TrendingDown, Sparkles, Search, ArrowRight, Globe } from 'lucide-react';
import { 
  searchAirports, 
  getAircraft, 
  optimizeRoute,
  getAirport,
  getWeather
} from './services/api';
import RouteMap from './components/RouteMap';
import EmissionChart from './components/EmissionChart';

export default function App() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [originSuggestions, setOriginSuggestions] = useState([]);
  const [destSuggestions, setDestSuggestions] = useState([]);
  const [aircraft, setAircraft] = useState([]);
  const [selectedAircraft, setSelectedAircraft] = useState('');
  const [preference, setPreference] = useState('eco');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [originAirportData, setOriginAirportData] = useState(null);
  const [destAirportData, setDestAirportData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);

  useEffect(() => {
    loadAircraft();
  }, []);

  const loadAircraft = async () => {
    try {
      const data = await getAircraft();
      setAircraft(data);
      if (data.length > 0) {
        setSelectedAircraft(data[0].model);
      }
    } catch (err) {
      console.error('Failed to load aircraft:', err);
    }
  };

  const handleOriginSearch = async (query) => {
    setOrigin(query);
    if (query.length >= 2) {
      try {
        const suggestions = await searchAirports(query);
        setOriginSuggestions(suggestions);
      } catch (err) {
        console.error('Search failed:', err);
      }
    } else {
      setOriginSuggestions([]);
    }
  };

  const handleDestSearch = async (query) => {
    setDestination(query);
    if (query.length >= 2) {
      try {
        const suggestions = await searchAirports(query);
        setDestSuggestions(suggestions);
      } catch (err) {
        console.error('Search failed:', err);
      }
    } else {
      setDestSuggestions([]);
    }
  };

  const selectOrigin = (airport) => {
    setOrigin(airport.iata);
    setOriginSuggestions([]);
  };

  const selectDest = (airport) => {
    setDestination(airport.iata);
    setDestSuggestions([]);
  };

  const handleOptimize = async () => {
    if (!origin || !destination) {
      setError('Please select both origin and destination airports');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      console.log('Fetching airport data for:', origin, destination);
      
      // Fetch airport data for map
      const [originData, destData] = await Promise.all([
        getAirport(origin),
        getAirport(destination)
      ]);
      
      console.log('Airport data received:', { originData, destData });
      
      setOriginAirportData(originData);
      setDestAirportData(destData);

      // Fetch weather for destination
      console.log('Fetching weather...');
      const weather = await getWeather(destData.latitude, destData.longitude);
      console.log('Weather data:', weather);
      setWeatherData(weather);

      // Optimize route
      console.log('Optimizing route...');
      const data = await optimizeRoute({
        origin: origin,
        destination: destination,
        aircraft_model: selectedAircraft,
        preference: preference
      });
      
      console.log('Optimization complete:', data);
      setResults(data);
    } catch (err) {
      setError('Optimization failed. Please try again.');
      console.error('Optimization error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100">
      {/* Navbar */}
      <nav className="bg-white shadow-lg border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-2.5 rounded-xl shadow-lg">
                <Plane className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-black text-gray-900">EcoFlight AI</h1>
                <p className="text-xs text-gray-600 font-medium">Carbon-Aware Optimization</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-100 rounded-lg transition">
                About
              </button>
              <button className="px-4 py-2 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg hover:shadow-lg transition">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 text-white">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="max-w-7xl mx-auto px-6 py-20 relative z-10">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm font-semibold">AI-Powered Route Optimization</span>
            </div>
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              Fly Smarter,<br />Emit Less Carbon
            </h2>
            <p className="text-xl text-white/90 max-w-2xl mx-auto mb-8">
              Advanced AI algorithms optimize your flight routes to minimize fuel consumption and CO₂ emissions
            </p>
            <div className="flex items-center justify-center space-x-8 text-sm font-semibold">
              <div className="flex items-center space-x-2">
                <Globe className="w-5 h-5" />
                <span>7,000+ Airports</span>
              </div>
              <div className="flex items-center space-x-2">
                <Leaf className="w-5 h-5" />
                <span>Eco-Friendly</span>
              </div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span>Real-Time Data</span>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-indigo-100 to-transparent"></div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 -mt-12 pb-20 relative z-10">
        {/* Input Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 mb-12">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Plan Your Optimized Route</h3>
          
          {/* Airport Inputs */}
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Origin */}
            <div className="relative">
              <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">
                From
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={origin}
                  onChange={(e) => handleOriginSearch(e.target.value)}
                  placeholder="Enter departure airport (e.g., JFK)"
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-2xl focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition outline-none text-lg font-medium"
                />
                <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
              {originSuggestions.length > 0 && (
                <div className="absolute z-20 w-full mt-2 bg-white rounded-2xl shadow-2xl border border-gray-100 max-h-80 overflow-y-auto">
                  {originSuggestions.map((airport) => (
                    <button
                      key={airport.iata}
                      onClick={() => selectOrigin(airport)}
                      className="w-full text-left px-5 py-4 hover:bg-indigo-50 transition-colors border-b border-gray-50 last:border-0 first:rounded-t-2xl last:rounded-b-2xl"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-bold text-gray-900 text-lg">{airport.iata}</div>
                          <div className="text-sm text-gray-600 mt-0.5">{airport.name}</div>
                          <div className="text-xs text-gray-500 mt-0.5">{airport.city}, {airport.country}</div>
                        </div>
                        <Plane className="w-5 h-5 text-indigo-400" />
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Destination */}
            <div className="relative">
              <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">
                To
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={destination}
                  onChange={(e) => handleDestSearch(e.target.value)}
                  placeholder="Enter arrival airport (e.g., LAX)"
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-2xl focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition outline-none text-lg font-medium"
                />
                <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
              {destSuggestions.length > 0 && (
                <div className="absolute z-20 w-full mt-2 bg-white rounded-2xl shadow-2xl border border-gray-100 max-h-80 overflow-y-auto">
                  {destSuggestions.map((airport) => (
                    <button
                      key={airport.iata}
                      onClick={() => selectDest(airport)}
                      className="w-full text-left px-5 py-4 hover:bg-purple-50 transition-colors border-b border-gray-50 last:border-0 first:rounded-t-2xl last:rounded-b-2xl"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-bold text-gray-900 text-lg">{airport.iata}</div>
                          <div className="text-sm text-gray-600 mt-0.5">{airport.name}</div>
                          <div className="text-xs text-gray-500 mt-0.5">{airport.city}, {airport.country}</div>
                        </div>
                        <Plane className="w-5 h-5 text-purple-400" />
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Options */}
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Aircraft */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">
                Aircraft Type
              </label>
              <select
                value={selectedAircraft}
                onChange={(e) => setSelectedAircraft(e.target.value)}
                className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-2xl focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition outline-none text-base font-medium cursor-pointer"
              >
                {aircraft.map((ac) => (
                  <option key={ac.model} value={ac.model}>
                    {ac.manufacturer} {ac.model}
                  </option>
                ))}
              </select>
            </div>

            {/* Optimization Mode */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">
                Optimization Priority
              </label>
              <div className="grid grid-cols-3 gap-3">
                <button
                  onClick={() => setPreference('eco')}
                  className={`p-4 rounded-2xl border-2 transition-all ${
                    preference === 'eco'
                      ? 'bg-green-50 border-green-500 shadow-md'
                      : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Leaf className={`w-6 h-6 mx-auto mb-1 ${preference === 'eco' ? 'text-green-600' : 'text-gray-400'}`} />
                  <div className={`text-xs font-bold ${preference === 'eco' ? 'text-green-700' : 'text-gray-600'}`}>
                    ECO
                  </div>
                </button>
                <button
                  onClick={() => setPreference('balanced')}
                  className={`p-4 rounded-2xl border-2 transition-all ${
                    preference === 'balanced'
                      ? 'bg-blue-50 border-blue-500 shadow-md'
                      : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Sparkles className={`w-6 h-6 mx-auto mb-1 ${preference === 'balanced' ? 'text-blue-600' : 'text-gray-400'}`} />
                  <div className={`text-xs font-bold ${preference === 'balanced' ? 'text-blue-700' : 'text-gray-600'}`}>
                    BALANCED
                  </div>
                </button>
                <button
                  onClick={() => setPreference('fast')}
                  className={`p-4 rounded-2xl border-2 transition-all ${
                    preference === 'fast'
                      ? 'bg-purple-50 border-purple-500 shadow-md'
                      : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Clock className={`w-6 h-6 mx-auto mb-1 ${preference === 'fast' ? 'text-purple-600' : 'text-gray-400'}`} />
                  <div className={`text-xs font-bold ${preference === 'fast' ? 'text-purple-700' : 'text-gray-600'}`}>
                    FAST
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-2xl text-red-700 font-medium flex items-center space-x-3">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span>{error}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            onClick={handleOptimize}
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-5 rounded-2xl font-bold text-lg shadow-xl hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center space-x-3">
                <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Calculating Optimal Route...</span>
              </span>
            ) : (
              <span className="flex items-center justify-center space-x-3">
                <Sparkles className="w-6 h-6" />
                <span>Optimize Flight Path</span>
                <ArrowRight className="w-6 h-6" />
              </span>
            )}
          </button>
        </div>

        {/* Results */}
        {results && (
          <div className="space-y-8">
            {/* Savings Banner */}
            {results.co2_savings_vs_direct && results.co2_savings_vs_direct > 0 && (
              <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-3xl p-8 shadow-2xl text-white">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    <div className="bg-white/20 p-4 rounded-2xl backdrop-blur-sm">
                      <TrendingDown className="w-10 h-10" />
                    </div>
                    <div>
                      <div className="text-6xl font-black mb-2">
                        {results.co2_savings_vs_direct}%
                      </div>
                      <div className="text-xl font-semibold text-white/90">
                        CO₂ Emissions Reduced
                      </div>
                      <div className="text-sm text-white/70 mt-1">
                        vs. standard direct route
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Stats */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                icon={<Plane className="w-7 h-7" />}
                title="Distance"
                value={results.total_distance_km.toLocaleString()}
                unit="km"
                color="blue"
              />
              <MetricCard
                icon={<Fuel className="w-7 h-7" />}
                title="Fuel Used"
                value={results.estimated_fuel_kg.toLocaleString()}
                unit="kg"
                color="orange"
              />
              <MetricCard
                icon={<Leaf className="w-7 h-7" />}
                title="CO₂ Emissions"
                value={results.estimated_co2_tons}
                unit="tons"
                color="green"
              />
              <MetricCard
                icon={<Clock className="w-7 h-7" />}
                title="Flight Time"
                value={results.flight_time_hours.toFixed(1)}
                unit="hrs"
                color="purple"
              />
            </div>

            {/* Route */}
            <div className="bg-white rounded-3xl shadow-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Flight Path</h3>
              <div className="flex flex-wrap items-center gap-4">
                {results.waypoints.map((waypoint, idx) => (
                  <div key={idx} className="flex items-center gap-4">
                    <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-bold text-2xl shadow-lg">
                      {waypoint}
                    </div>
                    {idx < results.waypoints.length - 1 && (
                      <ArrowRight className="w-6 h-6 text-gray-400" />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Route Visualization Map */}
            <RouteMap 
              waypoints={results.waypoints} 
              originData={originAirportData}
              destData={destAirportData}
              weatherData={weatherData}
            />

            {/* Emission Comparison Chart */}
            <EmissionChart optimizedData={results} />
          </div>
        )}
      </div>
    </div>
  );
}

function MetricCard({ icon, title, value, unit, color }) {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    orange: 'from-orange-500 to-orange-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600'
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg">
      <div className={`bg-gradient-to-r ${colors[color]} w-14 h-14 rounded-xl flex items-center justify-center text-white mb-4 shadow-md`}>
        {icon}
      </div>
      <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{title}</div>
      <div className="flex items-baseline space-x-2">
        <div className="text-4xl font-black text-gray-900">{value}</div>
        <div className="text-lg font-bold text-gray-500">{unit}</div>
      </div>
    </div>
  );
}