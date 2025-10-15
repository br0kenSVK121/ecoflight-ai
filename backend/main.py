"""
EcoFlight AI - Main FastAPI Application
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import flights, airports, optimization

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered carbon-aware flight optimization system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(airports.router, prefix=f"{settings.API_V1_PREFIX}/airports", tags=["Airports"])
app.include_router(flights.router, prefix=f"{settings.API_V1_PREFIX}/flights", tags=["Flights"])
app.include_router(optimization.router, prefix=f"{settings.API_V1_PREFIX}/optimize", tags=["Optimization"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EcoFlight AI",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)