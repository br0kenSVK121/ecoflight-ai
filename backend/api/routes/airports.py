"""
Airport API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database.connection import get_db
from models.database.schema import Airport
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for API responses
class AirportResponse(BaseModel):
    id: int
    iata_code: str
    icao_code: Optional[str]
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
    altitude_feet: Optional[float]
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AirportResponse])
async def get_airports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    country: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of airports with optional filtering
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **country**: Filter by country name
    - **search**: Search in airport name, city, or IATA code
    """
    query = db.query(Airport)
    
    # Apply filters
    if country:
        query = query.filter(Airport.country.ilike(f"%{country}%"))
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Airport.name.ilike(search_term)) |
            (Airport.city.ilike(search_term)) |
            (Airport.iata_code.ilike(search_term))
        )
    
    # Get results
    airports = query.offset(skip).limit(limit).all()
    return airports

@router.get("/{iata_code}", response_model=AirportResponse)
async def get_airport(
    iata_code: str,
    db: Session = Depends(get_db)
):
    """
    Get specific airport by IATA code
    
    - **iata_code**: 3-letter IATA code (e.g., JFK, LAX, LHR)
    """
    iata_code = iata_code.upper()
    
    airport = db.query(Airport).filter(Airport.iata_code == iata_code).first()
    
    if not airport:
        raise HTTPException(status_code=404, detail=f"Airport {iata_code} not found")
    
    return airport

@router.get("/search/autocomplete")
async def autocomplete_airports(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Autocomplete search for airports
    Returns airports matching the query string
    """
    search_term = f"%{q}%"
    
    airports = db.query(Airport).filter(
        (Airport.iata_code.ilike(search_term)) |
        (Airport.name.ilike(search_term)) |
        (Airport.city.ilike(search_term))
    ).limit(limit).all()
    
    return [
        {
            "iata": a.iata_code,
            "name": a.name,
            "city": a.city,
            "country": a.country,
            "label": f"{a.iata_code} - {a.name} ({a.city}, {a.country})"
        }
        for a in airports
    ]