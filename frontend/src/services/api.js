import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Airport endpoints
export const searchAirports = async (query) => {
  const response = await api.get(`/airports/search/autocomplete?q=${query}`);
  return response.data;
};

export const getAirport = async (iataCode) => {
  const response = await api.get(`/airports/${iataCode}`);
  return response.data;
};

export const getAirports = async (params = {}) => {
  const response = await api.get('/airports', { params });
  return response.data;
};

// Flight endpoints
export const getAircraft = async () => {
  const response = await api.get('/flights/aircraft');
  return response.data;
};

export const calculateEmissions = async (data) => {
  const response = await api.post('/flights/calculate-emissions', data);
  return response.data;
};

// Optimization endpoints
export const optimizeRoute = async (data) => {
  const response = await api.post('/optimize/route', data);
  return response.data;
};

export const findAlternatives = async (data) => {
  const response = await api.post('/optimize/alternatives', data);
  return response.data;
};

export const getOptimizationHistory = async () => {
  const response = await api.get('/optimize/history');
  return response.data;
};

// Weather API (using Open-Meteo - free, no API key needed)
export const getWeather = async (latitude, longitude) => {
  try {
    const response = await axios.get(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,windspeed_10m,weathercode&timezone=auto`
    );
    
    const data = response.data.current;
    const weatherCode = data.weathercode;
    
    // Map weather codes to conditions
    const weatherConditions = {
      0: 'Clear Sky',
      1: 'Mainly Clear',
      2: 'Partly Cloudy',
      3: 'Overcast',
      45: 'Foggy',
      48: 'Foggy',
      51: 'Light Drizzle',
      61: 'Light Rain',
      63: 'Moderate Rain',
      65: 'Heavy Rain',
      71: 'Light Snow',
      73: 'Moderate Snow',
      95: 'Thunderstorm'
    };
    
    return {
      temperature: Math.round(data.temperature_2m),
      windSpeed: Math.round(data.windspeed_10m),
      condition: weatherConditions[weatherCode] || 'Unknown',
      weatherCode: weatherCode
    };
  } catch (error) {
    console.error('Weather fetch failed:', error);
    return null;
  }
};

export default api;