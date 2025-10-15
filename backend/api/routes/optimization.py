"""
AI-powered flight optimization API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database.connection import get_db
from models.database.schema import Airport, FlightRoute, Aircraft, OptimizedPath
from api.services.optimization_engine import FlightOptimizer, FlightPath
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Request/Response models
class OptimizationRequest(BaseModel):
    origin: str  # IATA code
    destination: str  # IATA code
    aircraft_model: Optional[str] = "Airbus A320neo"
    preference: Optional[str] = "eco"  # eco, balanced, fast
    find_alternatives: Optional[bool] = False

class PathSegment(BaseModel):
    from_airport: str
    to_airport: str
    distance_km: float

class OptimizationResponse(BaseModel):
    origin: str
    destination: str
    waypoints: List[str]
    path_segments: List[PathSegment]
    total_distance_km: float
    estimated_fuel_kg: float
    estimated_co2_kg: float
    estimated_co2_tons: float
    flight_time_hours: float
    aircraft_model: str
    optimization_preference: str
    score: float
    co2_savings_vs_direct: Optional[float] = None

class AlternativeRoutesResponse(BaseModel):
    routes: List[OptimizationResponse]
    total_options: int

def _build_optimizer(db: Session, aircraft_model: str) -> FlightOptimizer:
    """Build optimizer instance with current database data"""
    # Get all airports
    airports = db.query(Airport).all()
    airports_data = [
        {
            'iata': a.iata_code,
            'latitude': a.latitude,
            'longitude': a.longitude,
            'name': a.name
        }
        for a in airports
    ]
    
    # Get all routes
    routes = db.query(FlightRoute).all()
    routes_data = [
        {
            'origin': r.origin.iata_code,
            'destination': r.destination.iata_code,
            'distance_km': r.distance_km
        }
        for r in routes
    ]
    
    # Get aircraft efficiency
    aircraft = db.query(Aircraft).filter(
        Aircraft.model == aircraft_model
    ).first()
    
    efficiency = aircraft.fuel_efficiency_kg_per_km if aircraft else 2.8
    
    return FlightOptimizer(airports_data, routes_data, efficiency)

def _flight_path_to_response(
    path: FlightPath,
    origin: str,
    destination: str,
    aircraft_model: str,
    preference: str,
    direct_co2: Optional[float] = None
) -> OptimizationResponse:
    """Convert FlightPath to API response"""
    
    # Create path segments
    segments = []
    for i in range(len(path.waypoints) - 1):
        from geopy.distance import geodesic
        # We'd ideally get this from the optimizer, but for now calculate
        segments.append(PathSegment(
            from_airport=path.waypoints[i],
            to_airport=path.waypoints[i + 1],
            distance_km=0  # Placeholder
        ))
    
    co2_savings = None
    if direct_co2 and len(path.waypoints) > 2:
        co2_savings = round(((direct_co2 - path.estimated_co2_kg) / direct_co2) * 100, 2)
    
    return OptimizationResponse(
        origin=origin,
        destination=destination,
        waypoints=path.waypoints,
        path_segments=segments,
        total_distance_km=round(path.total_distance_km, 2),
        estimated_fuel_kg=round(path.estimated_fuel_kg, 2),
        estimated_co2_kg=round(path.estimated_co2_kg, 2),
        estimated_co2_tons=round(path.estimated_co2_kg / 1000, 3),
        flight_time_hours=round(path.flight_time_hours, 2),
        aircraft_model=aircraft_model,
        optimization_preference=preference,
        score=round(path.score, 4),
        co2_savings_vs_direct=co2_savings
    )

@router.post("/route", response_model=OptimizationResponse)
async def optimize_route(
    request: OptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Optimize flight route using AI algorithms
    
    - **origin**: Origin airport IATA code (e.g., JFK)
    - **destination**: Destination airport IATA code (e.g., LAX)
    - **aircraft_model**: Aircraft type to use
    - **preference**: Optimization preference (eco/balanced/fast)
    """
    origin = request.origin.upper()
    destination = request.destination.upper()
    
    # Validate airports exist
    origin_airport = db.query(Airport).filter(Airport.iata_code == origin).first()
    dest_airport = db.query(Airport).filter(Airport.iata_code == destination).first()
    
    if not origin_airport or not dest_airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    # Build optimizer
    optimizer = _build_optimizer(db, request.aircraft_model)
    
    # Calculate direct path for comparison
    direct_path = optimizer._create_direct_path(origin, destination)
    
    # Optimize route
    optimized_path = optimizer.optimize_path_astar(
        origin,
        destination,
        request.preference
    )
    
    # Save to database
    optimized_record = OptimizedPath(
        origin_iata=origin,
        destination_iata=destination,
        waypoints=','.join(optimized_path.waypoints),
        total_distance_km=optimized_path.total_distance_km,
        estimated_fuel_kg=optimized_path.estimated_fuel_kg,
        estimated_co2_kg=optimized_path.estimated_co2_kg,
        time_cost_minutes=optimized_path.flight_time_hours * 60,
        optimization_score=optimized_path.score,
        algorithm_used='A*',
        created_at=datetime.utcnow()
    )
    db.add(optimized_record)
    db.commit()
    
    return _flight_path_to_response(
        optimized_path,
        origin,
        destination,
        request.aircraft_model,
        request.preference,
        direct_path.estimated_co2_kg
    )

@router.post("/alternatives", response_model=AlternativeRoutesResponse)
async def find_alternative_routes(
    request: OptimizationRequest,
    db: Session = Depends(get_db)
):
    """
    Find multiple alternative optimized routes
    """
    origin = request.origin.upper()
    destination = request.destination.upper()
    
    # Build optimizer
    optimizer = _build_optimizer(db, request.aircraft_model)
    
    # Find alternatives
    paths = optimizer.find_alternative_routes(origin, destination, max_alternatives=3)
    
    # Calculate direct for comparison
    direct_path = optimizer._create_direct_path(origin, destination)
    
    routes = [
        _flight_path_to_response(
            path,
            origin,
            destination,
            request.aircraft_model,
            f"Option {i+1}",
            direct_path.estimated_co2_kg
        )
        for i, path in enumerate(paths)
    ]
    
    return AlternativeRoutesResponse(
        routes=routes,
        total_options=len(routes)
    )

@router.get("/history")
async def get_optimization_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent optimization queries"""
    history = db.query(OptimizedPath).order_by(
        OptimizedPath.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "origin": h.origin_iata,
            "destination": h.destination_iata,
            "waypoints": h.waypoints.split(','),
            "distance_km": h.total_distance_km,
            "co2_kg": h.estimated_co2_kg,
            "algorithm": h.algorithm_used,
            "created_at": h.created_at
        }
        for h in history
    ]