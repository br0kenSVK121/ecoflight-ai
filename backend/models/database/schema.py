from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Airport(Base):
    """Airport database model"""
    __tablename__ = "airports"
    
    id = Column(Integer, primary_key=True, index=True)
    iata_code = Column(String(3), unique=True, index=True, nullable=False)
    icao_code = Column(String(4), unique=True, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_feet = Column(Float)
    timezone = Column(String(50))
    
    # Relationships
    departures = relationship("FlightRoute", foreign_keys="FlightRoute.origin_id", back_populates="origin")
    arrivals = relationship("FlightRoute", foreign_keys="FlightRoute.destination_id", back_populates="destination")

class FlightRoute(Base):
    """Flight route database model"""
    __tablename__ = "flight_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    distance_km = Column(Float, nullable=False)
    avg_flight_time_minutes = Column(Float)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    origin = relationship("Airport", foreign_keys=[origin_id], back_populates="departures")
    destination = relationship("Airport", foreign_keys=[destination_id], back_populates="arrivals")
    emissions = relationship("EmissionData", back_populates="route")

class Aircraft(Base):
    """Aircraft type database model"""
    __tablename__ = "aircraft"
    
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), unique=True, nullable=False)
    manufacturer = Column(String(100))
    capacity = Column(Integer)
    fuel_efficiency_kg_per_km = Column(Float, nullable=False)
    cruise_speed_kmh = Column(Float)
    max_range_km = Column(Float)
    co2_emission_factor = Column(Float, default=3.16)  # kg CO2 per kg fuel
    
    # Relationships
    emissions = relationship("EmissionData", back_populates="aircraft")

class EmissionData(Base):
    """CO2 emission data for specific routes and aircraft"""
    __tablename__ = "emission_data"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("flight_routes.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)
    fuel_consumption_kg = Column(Float, nullable=False)
    co2_emissions_kg = Column(Float, nullable=False)
    flight_time_minutes = Column(Float)
    altitude_ft = Column(Float)
    weather_factor = Column(Float, default=1.0)  # Multiplier for weather impact
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    route = relationship("FlightRoute", back_populates="emissions")
    aircraft = relationship("Aircraft", back_populates="emissions")

class OptimizedPath(Base):
    """AI-optimized flight paths"""
    __tablename__ = "optimized_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    origin_iata = Column(String(3), nullable=False)
    destination_iata = Column(String(3), nullable=False)
    waypoints = Column(String(1000))  # JSON string of intermediate waypoints
    total_distance_km = Column(Float, nullable=False)
    estimated_fuel_kg = Column(Float, nullable=False)
    estimated_co2_kg = Column(Float, nullable=False)
    time_cost_minutes = Column(Float, nullable=False)
    optimization_score = Column(Float)  # Combined score
    algorithm_used = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class UserQuery(Base):
    """Track user optimization requests"""
    __tablename__ = "user_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    aircraft_type = Column(String(100))
    optimization_preference = Column(String(20))  # 'eco', 'balanced', 'fast'
    created_at = Column(DateTime, default=datetime.utcnow)
    execution_time_ms = Column(Float)