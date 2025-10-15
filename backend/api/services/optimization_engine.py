"""
AI-powered flight path optimization engine
Uses A* algorithm and genetic algorithms for multi-objective optimization
"""

import networkx as nx
from geopy.distance import geodesic
from typing import List, Dict, Tuple
import heapq
from dataclasses import dataclass

@dataclass
class FlightPath:
    """Represents an optimized flight path"""
    waypoints: List[str]  # List of IATA codes
    total_distance_km: float
    estimated_fuel_kg: float
    estimated_co2_kg: float
    flight_time_hours: float
    score: float  # Optimization score

class FlightOptimizer:
    """AI-based flight path optimizer"""
    
    def __init__(self, airports_data: List[Dict], routes_data: List[Dict], aircraft_efficiency: float = 2.8):
        """
        Initialize optimizer with airport and route data
        
        Args:
            airports_data: List of airport dictionaries with coordinates
            routes_data: List of available routes
            aircraft_efficiency: kg fuel per km (default: A320neo)
        """
        self.airports = {a['iata']: a for a in airports_data}
        self.aircraft_efficiency = aircraft_efficiency
        self.co2_factor = 3.16  # kg CO2 per kg fuel
        
        # Build route network graph
        self.graph = self._build_graph(routes_data)
    
    def _build_graph(self, routes_data: List[Dict]) -> nx.DiGraph:
        """Build directed graph from route data"""
        G = nx.DiGraph()
        
        for route in routes_data:
            origin = route['origin']
            dest = route['destination']
            distance = route['distance_km']
            
            # Add edge with distance as weight
            G.add_edge(origin, dest, distance=distance)
        
        return G
    
    def _calculate_distance(self, origin: str, destination: str) -> float:
        """Calculate great circle distance between two airports"""
        if origin not in self.airports or destination not in self.airports:
            return float('inf')
        
        origin_coords = (
            self.airports[origin]['latitude'],
            self.airports[origin]['longitude']
        )
        dest_coords = (
            self.airports[destination]['latitude'],
            self.airports[destination]['longitude']
        )
        
        return geodesic(origin_coords, dest_coords).kilometers
    
    def _heuristic(self, current: str, goal: str) -> float:
        """A* heuristic: straight-line distance to goal"""
        return self._calculate_distance(current, goal)
    
    def _calculate_fuel_and_co2(self, distance_km: float) -> Tuple[float, float]:
        """Calculate fuel consumption and CO2 emissions"""
        fuel_kg = distance_km * self.aircraft_efficiency * 1.15  # 15% overhead
        co2_kg = fuel_kg * self.co2_factor
        return fuel_kg, co2_kg
    
    def optimize_path_astar(
        self,
        origin: str,
        destination: str,
        preference: str = 'eco'  # 'eco', 'balanced', 'fast'
    ) -> FlightPath:
        """
        Find optimal path using A* algorithm
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            preference: Optimization preference
        
        Returns:
            FlightPath object with optimized route
        """
        if origin not in self.graph or destination not in self.graph:
            # Direct path if no route exists
            return self._create_direct_path(origin, destination)
        
        # Set weights based on preference
        weights = {
            'eco': {'fuel': 0.7, 'distance': 0.3},
            'balanced': {'fuel': 0.5, 'distance': 0.5},
            'fast': {'fuel': 0.3, 'distance': 0.7}
        }
        w = weights.get(preference, weights['balanced'])
        
        # A* implementation
        frontier = [(0, origin, [origin])]
        explored = set()
        g_score = {origin: 0}
        
        while frontier:
            _, current, path = heapq.heappop(frontier)
            
            if current == destination:
                return self._create_flight_path(path)
            
            if current in explored:
                continue
            
            explored.add(current)
            
            # Explore neighbors
            if current in self.graph:
                for neighbor in self.graph.neighbors(current):
                    edge_data = self.graph[current][neighbor]
                    distance = edge_data['distance']
                    
                    # Calculate cost (weighted combination)
                    fuel, _ = self._calculate_fuel_and_co2(distance)
                    cost = w['fuel'] * fuel + w['distance'] * distance
                    
                    new_g_score = g_score[current] + cost
                    
                    if neighbor not in g_score or new_g_score < g_score[neighbor]:
                        g_score[neighbor] = new_g_score
                        h_score = self._heuristic(neighbor, destination)
                        f_score = new_g_score + h_score
                        
                        new_path = path + [neighbor]
                        heapq.heappush(frontier, (f_score, neighbor, new_path))
        
        # No path found, return direct
        return self._create_direct_path(origin, destination)
    
    def _create_direct_path(self, origin: str, destination: str) -> FlightPath:
        """Create a direct flight path"""
        distance = self._calculate_distance(origin, destination)
        fuel, co2 = self._calculate_fuel_and_co2(distance)
        
        return FlightPath(
            waypoints=[origin, destination],
            total_distance_km=distance,
            estimated_fuel_kg=fuel,
            estimated_co2_kg=co2,
            flight_time_hours=distance / 850,  # Average cruise speed
            score=1.0
        )
    
    def _create_flight_path(self, waypoints: List[str]) -> FlightPath:
        """Create FlightPath object from waypoint list"""
        total_distance = 0
        
        for i in range(len(waypoints) - 1):
            if waypoints[i] in self.graph and waypoints[i+1] in self.graph.neighbors(waypoints[i]):
                total_distance += self.graph[waypoints[i]][waypoints[i+1]]['distance']
            else:
                total_distance += self._calculate_distance(waypoints[i], waypoints[i+1])
        
        fuel, co2 = self._calculate_fuel_and_co2(total_distance)
        
        return FlightPath(
            waypoints=waypoints,
            total_distance_km=total_distance,
            estimated_fuel_kg=fuel,
            estimated_co2_kg=co2,
            flight_time_hours=total_distance / 850,
            score=self._calculate_score(fuel, total_distance)
        )
    
    def _calculate_score(self, fuel: float, distance: float) -> float:
        """Calculate optimization score (lower is better)"""
        # Normalize and combine metrics
        return (fuel * 0.6 + distance * 0.4) / 1000
    
    def find_alternative_routes(
        self,
        origin: str,
        destination: str,
        max_alternatives: int = 3
    ) -> List[FlightPath]:
        """
        Find multiple alternative routes
        
        Returns top N paths sorted by score
        """
        alternatives = []
        
        # Try different optimization preferences
        for pref in ['eco', 'balanced', 'fast']:
            path = self.optimize_path_astar(origin, destination, pref)
            alternatives.append(path)
        
        # Sort by score and return unique paths
        unique_paths = []
        seen_waypoints = set()
        
        for path in sorted(alternatives, key=lambda x: x.score):
            waypoint_key = tuple(path.waypoints)
            if waypoint_key not in seen_waypoints:
                unique_paths.append(path)
                seen_waypoints.add(waypoint_key)
            
            if len(unique_paths) >= max_alternatives:
                break
        
        return unique_paths