# ✈️ EcoFlight AI - Carbon-Aware Flight Optimization System

![EcoFlight AI](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.3-61dafb?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python)

An intelligent flight route optimization system that uses AI algorithms to minimize carbon emissions and fuel consumption while maintaining efficient flight times.
 
---

## 📸 Screenshots

<img width="1424" height="823" alt="image" src="https://github.com/user-attachments/assets/1dde1122-d899-4d7d-b070-7903c4964f5b" />
<img width="1424" height="483" alt="image" src="https://github.com/user-attachments/assets/f949eeb0-8a3a-43ab-90c3-832cf74c716b" />
<img width="1424" height="684" alt="image" src="https://github.com/user-attachments/assets/10ca5f15-c228-42d5-857b-c4b6c51c7c96" />
<img width="1424" height="740" alt="image" src="https://github.com/user-attachments/assets/42939021-4fa5-4100-aeeb-7c32b1b86970" />

---

## 🌟 Features

- 🤖 **AI-Powered Optimization** - A* pathfinding algorithm for optimal routes
- 🌍 **Real-World Data** - 7,000+ airports and 60,000+ flight routes
- 📊 **Emission Tracking** - Real-time CO₂ and fuel consumption calculations
- 🎯 **Multi-Objective** - Balance between eco-friendliness, time, and efficiency
- 📈 **Visual Analytics** - Interactive charts and route visualizations
- ⚡ **Fast API** - RESTful backend with comprehensive documentation

---

## 🏗️ Architecture

```
ecoflight-ai/
├── backend/                 # FastAPI Backend
│   ├── api/                # API endpoints
│   │   ├── routes/         # Route handlers
│   │   └── services/       # Business logic
│   ├── models/             # Database models
│   │   ├── database/       # SQLAlchemy schemas
│   │   └── ml/             # ML models
│   └── utils/              # Utilities
│
└── frontend/               # React Frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── services/       # API integration
    │   └── App.jsx         # Main application
    └── public/
```

---

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Embedded database
- **NetworkX** - Graph algorithms for route optimization
- **Scikit-learn** - Machine learning utilities
- **Geopy** - Geographic calculations

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd ecoflight-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize database
python init_database.py

# Load airport and route data
python load_data.py

# Start the API server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 🎯 Usage

### 1. **Select Airports**
- Enter departure and arrival airports
- Autocomplete suggestions appear as you type

### 2. **Choose Aircraft**
- Select from 4 real aircraft models
- Each with different fuel efficiency ratings

### 3. **Set Optimization Mode**
- **ECO**: Minimize CO₂ emissions (70% weight on fuel)
- **BALANCED**: Balance time and emissions (50/50)
- **FAST**: Prioritize speed (70% weight on time)

### 4. **View Results**
- Total distance and flight time
- Fuel consumption and CO₂ emissions
- CO₂ savings vs. direct route
- Optimized waypoint path
- Visual route map and comparison charts

---

## 🧠 AI Optimization Algorithm

The system uses **A* pathfinding** with custom heuristics:

```python
# Cost function
cost = w_fuel × fuel_consumption + w_time × flight_time

# Heuristic (great circle distance)
h(n) = geodesic_distance(current_node, goal_node)

# Total score
f(n) = g(n) + h(n)
```

### Optimization Modes

| Mode | Fuel Weight | Time Weight |
|------|-------------|-------------|
| ECO | 0.7 | 0.3 |
| BALANCED | 0.5 | 0.5 |
| FAST | 0.3 | 0.7 |

---

## 📡 API Endpoints

### Airports
- `GET /api/v1/airports` - List airports
- `GET /api/v1/airports/{iata}` - Get specific airport
- `GET /api/v1/airports/search/autocomplete` - Search airports

### Flights
- `POST /api/v1/flights/calculate-emissions` - Calculate CO₂
- `GET /api/v1/flights/aircraft` - List aircraft

### Optimization
- `POST /api/v1/optimize/route` - Optimize single route
- `POST /api/v1/optimize/alternatives` - Find alternatives
- `GET /api/v1/optimize/history` - View history

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📊 Database Schema

- **airports** - 7,000+ airports worldwide
- **flight_routes** - 60,000+ real routes
- **aircraft** - Aircraft specifications
- **emission_data** - Calculated emissions
- **optimized_paths** - AI-optimized routes

---

## 🌱 Environmental Impact

### CO₂ Emission Factors
- Jet fuel: **3.16 kg CO₂ per kg fuel** (ICAO standard)
- Based on real aircraft fuel efficiency data
- Considers takeoff/landing overhead (15%)

### Sample Savings
- **JFK → LAX (Eco Mode)**: ~8-12% CO₂ reduction
- **Longer Routes**: Up to 15-20% savings possible

---

## 🎨 UI Features

- Modern gradient design
- Smooth animations
- Responsive layout
- Real-time search
- Interactive visualizations
- Professional data presentation

---

## 🔜 Future Enhancements

- [ ] 3D Globe visualization with Mapbox GL
- [ ] Weather data integration
- [ ] Historical flight data analysis
- [ ] User accounts and saved routes
- [ ] Carbon offset calculator
- [ ] Mobile app
- [ ] Real-time flight tracking
- [ ] Multi-leg journey optimization

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 👨‍💻 Author

**Steve Thomas Mulamoottil**

Built with ❤️ for a sustainable future in aviation

---

## 🙏 Acknowledgments

- OpenFlights.org for airport and route data
- ICAO for CO₂ emission standards
- Aircraft manufacturers for fuel efficiency data
- Open-Meteo for weather API
- Esri for satellite imagery

---

## 📞 Support

For issues or questions, please open an issue on GitHub.

**Let's make aviation more sustainable, one optimized route at a time! 🌍✈️**


