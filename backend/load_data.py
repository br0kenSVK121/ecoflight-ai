"""
Load airport and route data into the database
Run this with: python load_data.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database.schema import Airport, FlightRoute, Aircraft
from utils.data_collector import AirportDataCollector
from config import settings
import sys

def load_airports(session, df):
    """Load airports into database"""
    print(f"\n📍 Loading {len(df)} airports...")
    
    count = 0
    for _, row in df.iterrows():
        try:
            airport = Airport(
                iata_code=row['iata'],
                icao_code=row['icao'] if row['icao'] else None,
                name=row['name'],
                city=row['city'],
                country=row['country'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                altitude_feet=row['altitude'],
                timezone=row['timezone']
            )
            session.add(airport)
            count += 1
            
            if count % 500 == 0:
                session.commit()
                print(f"   ✓ Loaded {count} airports...")
        except Exception as e:
            print(f"   ⚠️  Skipped {row['iata']}: {e}")
            continue
    
    session.commit()
    print(f"✅ Loaded {count} airports successfully!")
    return count

def load_routes(session, df):
    """Load routes into database"""
    print(f"\n🛫 Loading {len(df)} routes...")
    
    # Get airport ID mapping
    airports = session.query(Airport).all()
    airport_map = {a.iata_code: a.id for a in airports}
    
    count = 0
    for _, row in df.iterrows():
        try:
            origin_code = row['source_airport']
            dest_code = row['destination_airport']
            
            if origin_code not in airport_map or dest_code not in airport_map:
                continue
            
            route = FlightRoute(
                origin_id=airport_map[origin_code],
                destination_id=airport_map[dest_code],
                distance_km=row['distance_km'],
                avg_flight_time_minutes=row['distance_km'] / 14.0,  # Rough estimate
                is_active=True
            )
            session.add(route)
            count += 1
            
            if count % 1000 == 0:
                session.commit()
                print(f"   ✓ Loaded {count} routes...")
        except Exception as e:
            continue
    
    session.commit()
    print(f"✅ Loaded {count} routes successfully!")
    return count

def load_aircraft(session):
    """Load sample aircraft data"""
    print(f"\n✈️  Loading aircraft data...")
    
    collector = AirportDataCollector()
    aircraft_data = collector.get_sample_aircraft_data()
    
    for data in aircraft_data:
        aircraft = Aircraft(**data)
        session.add(aircraft)
    
    session.commit()
    print(f"✅ Loaded {len(aircraft_data)} aircraft types!")
    return len(aircraft_data)

def main():
    print("="*60)
    print("📊 EcoFlight AI - Data Loading")
    print("="*60)
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Initialize data collector
        collector = AirportDataCollector()
        
        # Fetch data
        print("\n🌐 Fetching data from OpenFlights...")
        airports_df = collector.fetch_airports()
        routes_df = collector.fetch_routes()
        
        if airports_df is None or routes_df is None:
            print("❌ Failed to fetch data!")
            sys.exit(1)
        
        # Calculate distances
        enriched_routes = collector.enrich_routes_with_distance()
        
        # Load into database
        airport_count = load_airports(session, airports_df)
        route_count = load_routes(session, enriched_routes)
        aircraft_count = load_aircraft(session)
        
        print("\n" + "="*60)
        print("✅ Data loading complete!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   ✓ Airports: {airport_count}")
        print(f"   ✓ Routes: {route_count}")
        print(f"   ✓ Aircraft: {aircraft_count}")
        print(f"\n🎯 Next: Start the API server")
        print(f"   Run: uvicorn main:app --reload")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main()