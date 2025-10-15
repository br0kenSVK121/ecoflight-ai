"""
Test the EcoFlight API endpoints
Run after starting the server with: uvicorn main:app --reload
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_api():
    """Run all API tests"""
    
    print("\n" + "="*60)
    print("🚀 EcoFlight AI - API Testing")
    print("="*60)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    sleep(1)
    
    # Test 2: Get airports
    print("\n2️⃣ Testing airports endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/airports?limit=5")
    print_response("Get Airports", response)
    
    sleep(1)
    
    # Test 3: Search airports
    print("\n3️⃣ Testing airport search...")
    response = requests.get(f"{BASE_URL}/api/v1/airports/search/autocomplete?q=New York")
    print_response("Search Airports", response)
    
    sleep(1)
    
    # Test 4: Get specific airport
    print("\n4️⃣ Testing specific airport...")
    response = requests.get(f"{BASE_URL}/api/v1/airports/JFK")
    print_response("Get JFK Airport", response)
    
    sleep(1)
    
    # Test 5: Get aircraft
    print("\n5️⃣ Testing aircraft endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/flights/aircraft")
    print_response("Get Aircraft", response)
    
    sleep(1)
    
    # Test 6: Calculate emissions
    print("\n6️⃣ Testing emission calculation...")
    payload = {
        "origin": "JFK",
        "destination": "LAX",
        "aircraft_model": "Airbus A320neo"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/flights/calculate-emissions",
        json=payload
    )
    print_response("Calculate Emissions (JFK → LAX)", response)
    
    sleep(1)
    
    # Test 7: Optimize route (ECO mode)
    print("\n7️⃣ Testing route optimization (ECO)...")
    payload = {
        "origin": "JFK",
        "destination": "LAX",
        "aircraft_model": "Airbus A320neo",
        "preference": "eco"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/optimize/route",
        json=payload
    )
    print_response("Optimize Route (ECO)", response)
    
    sleep(1)
    
    # Test 8: Find alternative routes
    print("\n8️⃣ Testing alternative routes...")
    payload = {
        "origin": "JFK",
        "destination": "SFO",
        "aircraft_model": "Boeing 737-800",
        "preference": "balanced"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/optimize/alternatives",
        json=payload
    )
    print_response("Find Alternatives (JFK → SFO)", response)
    
    sleep(1)
    
    # Test 9: Get optimization history
    print("\n9️⃣ Testing optimization history...")
    response = requests.get(f"{BASE_URL}/api/v1/optimize/history")
    print_response("Optimization History", response)
    
    print("\n" + "="*60)
    print("✅ API Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the server is running:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")