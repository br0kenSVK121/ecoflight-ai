🚀 EcoFlight AI - Backend API
Carbon-aware flight optimization system with AI-powered route planning.

🎯 Quick Start
1. Create Package Structure
bash# Run this from the backend directory
bash -c "$(cat << 'EOF'
touch api/__init__.py
touch api/routes/__init__.py
touch api/services/__init__.py
touch models/__init__.py
touch models/database/__init__.py
touch models/ml/__init__.py
touch utils/__init__.py
EOF
)"
2. Start the API Server
bashuvicorn main:app --reload
The API will be available at: http://localhost:8000
3. View API Documentation
Open your browser and go to:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc


🧪 Test the API
In a new terminal (while server is running):
bashpython test_api.py
This will test all endpoints and show you example requests/responses.

📡 API Endpoints
Airports

GET /api/v1/airports - List airports
GET /api/v1/airports/{iata} - Get specific airport
GET /api/v1/airports/search/autocomplete?q=query - Search airports

Flights

GET /api/v1/flights/routes - Get flight routes
GET /api/v1/flights/aircraft - List aircraft types
POST /api/v1/flights/calculate-emissions - Calculate CO₂ emissions

Optimization (AI Engine)

POST /api/v1/optimize/route - Optimize single route
POST /api/v1/optimize/alternatives - Find alternative routes
GET /api/v1/optimize/history - View optimization history


💡 Example Requests
Calculate Emissions
bashcurl -X POST "http://localhost:8000/api/v1/flights/calculate-emissions" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "JFK",
    "destination": "LAX",
    "aircraft_model": "Airbus A320neo"
  }'
Optimize Route
bashcurl -X POST "http://localhost:8000/api/v1/optimize/route" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "JFK",
    "destination": "LAX",
    "aircraft_model": "Airbus A320neo",
    "preference": "eco"
  }'
Search Airports
bashcurl "http://localhost:8000/api/v1/airports/search/autocomplete?q=london"

🎨 Optimization Modes

eco: Minimizes CO₂ emissions (70% weight on fuel efficiency)
balanced: Balance between emissions and time (50/50 split)
fast: Prioritizes speed (70% weight on distance/time)


🧠 AI Algorithms

A Pathfinding*: Finds optimal routes through the flight network
Multi-Objective Optimization: Balances fuel efficiency vs flight time
Heuristic Search: Uses great-circle distance as heuristic


📊 Database Schema

airports: 7,000+ airports worldwide
flight_routes: 60,000+ real flight routes
aircraft: 4 aircraft models with fuel efficiency data
emission_data: Calculated emissions for routes
optimized_paths: AI-optimized flight paths


🔧 Troubleshooting
Server won't start
bash# Make sure you're in the backend directory
cd backend

# Check if packages are installed
python test_setup.py

# Try running with specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Import errors
bash# Create __init__.py files
find . -type d -name "__pycache__" -prune -o -type d -exec touch {}/__init__.py \;
Database errors
bash# Reinitialize database
python init_database.py
python load_data.py

🚀 Next Steps
Once the backend is running:

✅ Test all endpoints with python test_api.py
📱 Build the frontend React dashboard
🗺️ Add Mapbox visualization
📈 Create emission comparison charts


📝 Notes

The API uses SQLite by default (no PostgreSQL needed)
All calculations use real airport coordinates
CO₂ factor: 3.16 kg CO₂ per kg of jet fuel (ICAO standard)
Aircraft efficiency based on real manufacturer data
