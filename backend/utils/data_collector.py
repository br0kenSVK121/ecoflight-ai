import pandas as pd
import requests
from geopy.distance import geodesic
import json
from typing import List, Dict

class AirportDataCollector:
    """Collect and process airport data from OpenFlights"""
    
    AIRPORTS_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    ROUTES_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
    
    def __init__(self):
        self.airports_df = None
        self.routes_df = None
    
    def fetch_airports(self) -> pd.DataFrame:
        """Fetch airport data from OpenFlights"""
        print("📥 Fetching airport data...")
        
        columns = [
            'airport_id', 'name', 'city', 'country', 'iata', 'icao',
            'latitude', 'longitude', 'altitude', 'timezone_offset',
            'dst', 'timezone', 'type', 'source'
        ]
        
        try:
            df = pd.read_csv(
                self.AIRPORTS_URL,
                names=columns,
                na_values=['\\N'],
                encoding='utf-8'
            )
            
            # Filter only airports (not train stations, etc.)
            df = df[df['type'] == 'airport']
            
            # Remove entries without IATA codes
            df = df[df['iata'].notna()]
            
            # Clean data
            df['iata'] = df['iata'].str.upper()
            df['icao'] = df['icao'].str.upper()
            
            self.airports_df = df
            print(f"✅ Loaded {len(df)} airports")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching airports: {e}")
            return None
    
    def fetch_routes(self) -> pd.DataFrame:
        """Fetch route data from OpenFlights"""
        print("📥 Fetching route data...")
        
        columns = [
            'airline', 'airline_id', 'source_airport', 'source_airport_id',
            'destination_airport', 'destination_airport_id', 'codeshare',
            'stops', 'equipment'
        ]
        
        try:
            df = pd.read_csv(
                self.ROUTES_URL,
                names=columns,
                na_values=['\\N'],
                encoding='utf-8'
            )
            
            # Filter direct flights only
            df = df[df['stops'] == 0]
            
            self.routes_df = df
            print(f"✅ Loaded {len(df)} routes")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching routes: {e}")
            return None
    
    def calculate_distance(self, origin_coords: tuple, dest_coords: tuple) -> float:
        """Calculate great circle distance between two points"""
        return geodesic(origin_coords, dest_coords).kilometers
    
    def enrich_routes_with_distance(self) -> pd.DataFrame:
        """Add distance calculations to routes"""
        if self.airports_df is None or self.routes_df is None:
            print("❌ Please fetch airports and routes first")
            return None
        
        print("🔄 Calculating distances...")
        
        # Create airport lookup dictionary
        airport_lookup = {}
        for _, row in self.airports_df.iterrows():
            airport_lookup[row['iata']] = (row['latitude'], row['longitude'])
        
        distances = []
        valid_routes = []
        
        for idx, route in self.routes_df.iterrows():
            origin = route['source_airport']
            dest = route['destination_airport']
            
            if origin in airport_lookup and dest in airport_lookup:
                dist = self.calculate_distance(
                    airport_lookup[origin],
                    airport_lookup[dest]
                )
                distances.append(dist)
                valid_routes.append(route)
        
        enriched_df = pd.DataFrame(valid_routes)
        enriched_df['distance_km'] = distances
        
        print(f"✅ Calculated distances for {len(enriched_df)} routes")
        return enriched_df
    
    def get_sample_aircraft_data(self) -> List[Dict]:
        """Return sample aircraft data with realistic fuel efficiency"""
        return [
            {
                "model": "Boeing 737-800",
                "manufacturer": "Boeing",
                "capacity": 189,
                "fuel_efficiency_kg_per_km": 3.5,
                "cruise_speed_kmh": 842,
                "max_range_km": 5765,
                "co2_emission_factor": 3.16
            },
            {
                "model": "Airbus A320neo",
                "manufacturer": "Airbus",
                "capacity": 180,
                "fuel_efficiency_kg_per_km": 2.8,
                "cruise_speed_kmh": 840,
                "max_range_km": 6300,
                "co2_emission_factor": 3.16
            },
            {
                "model": "Boeing 787-9",
                "manufacturer": "Boeing",
                "capacity": 296,
                "fuel_efficiency_kg_per_km": 2.3,
                "cruise_speed_kmh": 903,
                "max_range_km": 14140,
                "co2_emission_factor": 3.16
            },
            {
                "model": "Airbus A350-900",
                "manufacturer": "Airbus",
                "capacity": 315,
                "fuel_efficiency_kg_per_km": 2.4,
                "cruise_speed_kmh": 910,
                "max_range_km": 15000,
                "co2_emission_factor": 3.16
            }
        ]
    
    def save_data(self, output_dir: str = "data/processed"):
        """Save processed data to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if self.airports_df is not None:
            self.airports_df.to_csv(
                f"{output_dir}/airports.csv",
                index=False
            )
            print(f"✅ Saved airports to {output_dir}/airports.csv")
        
        enriched_routes = self.enrich_routes_with_distance()
        if enriched_routes is not None:
            enriched_routes.to_csv(
                f"{output_dir}/routes.csv",
                index=False
            )
            print(f"✅ Saved routes to {output_dir}/routes.csv")
        
        aircraft_data = self.get_sample_aircraft_data()
        pd.DataFrame(aircraft_data).to_csv(
            f"{output_dir}/aircraft.csv",
            index=False
        )
        print(f"✅ Saved aircraft data to {output_dir}/aircraft.csv")

# Main execution
if __name__ == "__main__":
    collector = AirportDataCollector()
    collector.fetch_airports()
    collector.fetch_routes()
    collector.save_data()