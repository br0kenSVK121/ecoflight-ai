import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR.parent / "data"
    
    # Database configuration
    # Set USE_SQLITE=true in .env for SQLite, or configure PostgreSQL
    USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    if USE_SQLITE:
        # SQLite configuration (easier for development)
        SQLITE_DB_PATH = BASE_DIR / "ecoflight.db"
        DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
        print(f"📁 Using SQLite database at: {SQLITE_DB_PATH}")
    else:
        # PostgreSQL configuration
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "ecoflight")
        
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"🐘 Using PostgreSQL database: {DB_NAME}")
    
    # API Configuration
    API_V1_PREFIX = "/api/v1"
    PROJECT_NAME = "EcoFlight AI"
    VERSION = "1.0.0"
    
    # CORS settings
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]
    
    # AI Model settings
    DEFAULT_AIRCRAFT = "Airbus A320neo"
    CO2_PER_KG_FUEL = 3.16  # kg CO2 per kg of jet fuel
    
    # Optimization preferences
    OPTIMIZATION_MODES = {
        "eco": {"fuel_weight": 0.7, "time_weight": 0.3},
        "balanced": {"fuel_weight": 0.5, "time_weight": 0.5},
        "fast": {"fuel_weight": 0.3, "time_weight": 0.7}
    }
    
    # Data source URLs
    AIRPORTS_DATA_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    ROUTES_DATA_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
    
    class Config:
        case_sensitive = True

settings = Settings()