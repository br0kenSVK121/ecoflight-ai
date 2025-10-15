"""
Flight routes and emission calculation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database.connection import get_db
from models.database.schema import FlightRoute, Airport, Aircraft, EmissionData
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Pydantic models
class FlightRouteResponse(BaseModel):
    id: int
    origin: str
    destination: str
    distance_km: float
    avg_flight_time_minutes: Optional[float]
    
    class Config:
        from_attributes = True

class EmissionCalculationRequest(BaseModel):
    origin: str  # IATA code
    destination: str  # IATA code
    aircraft_model: Optional[str] = "Airbus A320neo"

class EmissionCalculationResponse(BaseModel):
    origin: str
    destination: str
    distance_km: float
    aircraft_model: str
    fuel_consumption_kg: float
    co2_emissions_kg: float
    co2_emissions_tons: float
    flight_time_hours: float
    passengers: int
    co2_per_passenger_kg: float

@router.get("/routes")
async def get_routes(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get flight routes with optional filtering
    """
    query = db.query(FlightRoute).join(
        Airport, FlightRoute.origin_id == Airport.id
    )
    
    if origin:
        query = query.filter(Airport.iata_code == origin.upper())
    
    if destination:
        dest_alias = db.query(Airport).filter(
            Airport.iata_code == destination.upper()
        ).first()
        if dest_alias:
            query = query.filter(FlightRoute.destination_id == dest_alias.id)
    
    routes = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "origin": r.origin.iata_code,
            "origin_name": r.origin.name,
            "destination": r.destination.iata_code,
            "destination_name": r.destination.name,
            "distance_km": r.distance_km,
            "flight_time_minutes": r.avg_flight_time_minutes
        }
        for r in routes
    ]

@router.post("/calculate-emissions", response_model=EmissionCalculationResponse)
async def calculate_emissions(
    request: EmissionCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate fuel consumption and CO2 emissions for a flight
    """
    # Get airports
    origin = db.query(Airport).filter(
        Airport.iata_code == request.origin.upper()
    ).first()
    destination = db.query(Airport).filter(
        Airport.iata_code == request.destination.upper()
    ).first()
    
    if not origin or not destination:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    # Get aircraft
    aircraft = db.query(Aircraft).filter(
        Aircraft.model == request.aircraft_model
    ).first()
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft model not found")
    
    # Calculate distance using great circle
    from geopy.distance import geodesic
    distance_km = geodesic(
        (origin.latitude, origin.longitude),
        (destination.latitude, destination.longitude)
    ).kilometers
    
    # Calculate fuel consumption (simplified model)
    # Base fuel + distance-based consumption
    fuel_kg = distance_km * aircraft.fuel_efficiency_kg_per_km
    
    # Add takeoff/landing overhead (roughly 15%)
    fuel_kg *= 1.15
    
    # Calculate CO2 emissions
    co2_kg = fuel_kg * aircraft.co2_emission_factor
    co2_tons = co2_kg / 1000
    
    # Calculate flight time
    flight_time_hours = distance_km / aircraft.cruise_speed_kmh
    
    # CO2 per passenger
    co2_per_passenger = co2_kg / aircraft.capacity
    
    # Save to database (optional - skip if route_id is required)
    try:
        emission_record = EmissionData(
            route_id=None,  # We might not have this route in DB
            aircraft_id=aircraft.id,
            fuel_consumption_kg=fuel_kg,
            co2_emissions_kg=co2_kg,
            flight_time_minutes=flight_time_hours * 60,
            altitude_ft=35000,  # Standard cruise altitude
            calculated_at=datetime.utcnow()
        )
        db.add(emission_record)
        db.commit()
    except Exception as e:
        # If saving fails, just log and continue
        print(f"Warning: Could not save emission record: {e}")
        db.rollback()
    
    return EmissionCalculationResponse(
        origin=request.origin.upper(),
        destination=request.destination.upper(),
        distance_km=round(distance_km, 2),
        aircraft_model=aircraft.model,
        fuel_consumption_kg=round(fuel_kg, 2),
        co2_emissions_kg=round(co2_kg, 2),
        co2_emissions_tons=round(co2_tons, 3),
        flight_time_hours=round(flight_time_hours, 2),
        passengers=aircraft.capacity,
        co2_per_passenger_kg=round(co2_per_passenger, 2)
    )

@router.get("/aircraft")
async def get_aircraft(db: Session = Depends(get_db)):
    """Get list of available aircraft"""
    aircraft = db.query(Aircraft).all()
    
    return [
        {
            "model": a.model,
            "manufacturer": a.manufacturer,
            "capacity": a.capacity,
            "fuel_efficiency": a.fuel_efficiency_kg_per_km,
            "cruise_speed": a.cruise_speed_kmh,
            "max_range": a.max_range_km
        }
        for a in aircraft
    ]   