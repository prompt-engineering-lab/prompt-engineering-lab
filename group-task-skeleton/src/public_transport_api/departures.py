from flask import Blueprint, jsonify, request
import sqlite3
from typing import List, Optional
import datetime
from scipy import spatial

from models import Coordinates, Metadata
from db_models import StopInfo

departures_bp = Blueprint('departures', __name__, url_prefix='/public_transport/city/<string:city>/closest_departures')


@departures_bp.route("/", methods=["GET"])
def closest_departures(city: str):
    start_coordinates = request.args.get('start_coordinates')
    end_coordinates = request.args.get('end_coordinates')
    start_time = request.args.get('start_time')
    limit = int(request.args.get('limit', 5))
    
    return jsonify(get_closest_departures(city, start_coordinates, end_coordinates, start_time, limit))


def _get_all_stops() -> List[StopInfo]:
    conn = sqlite3.connect('trips.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT stop_id, stop_code, stop_name, stop_lat, stop_lon
                   FROM stops 
                   """)
    stop_rows = cursor.fetchall()
    
    conn.close()
    return [StopInfo(*row) for row in stop_rows]


def _get_all_routes() -> List[tuple]:
    conn = sqlite3.connect('trips.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT route_id, agency_id, route_short_name, route_long_name, 
                          route_desc, route_type, route_type2_id, valid_from, valid_until
                   FROM routes
                   """)
    route_rows = cursor.fetchall()
    
    conn.close()
    return route_rows


def find_closest_stops(coordinates: str, n: int = 2) -> List[StopInfo]:
    lat, lon = map(float, coordinates.split(','))
    all_stops = _get_all_stops()
    
    stop_coords = [[stop.stop_lat, stop.stop_lon] for stop in all_stops]
    tree = spatial.KDTree(stop_coords)
    
    _, indices = tree.query([lat, lon], k=n)
    return [all_stops[i] for i in indices]


def get_closest_departures_from_db(start_coordinates: str, end_coordinates: str, start_time: str, limit: int) -> List[dict]:
    closest_start_stops = find_closest_stops(start_coordinates, 2)
    closest_end_stops = find_closest_stops(end_coordinates, 2)

    #TODO logic below
    departures = []
    for i, stop_info in enumerate(closest_start_stops):
        coordinates: Coordinates = {
            "latitude": stop_info.stop_lat,
            "longitude": stop_info.stop_lon
        }
        
        departure = {
            "trip_id": f"mock_trip_{i+1:03d}",
            "route_id": f"mock_route_{chr(65+i)}",
            "trip_headsign": stop_info.stop_name,
            "stop": {
                "id": f"mock_stop_{i+1:03d}",
                "name": stop_info.stop_name,
                "coordinates": coordinates,
                "arrival_time": stop_info.arrival_time,
                "departure_time": stop_info.departure_time
            },
            "distance_start_to_stop": 123.45 + i * 50,
            "debug_dist_stop_to_end": 543.21 - i * 100
        }
        departures.append(departure)
    
    return departures


def get_closest_departures(city: str, start_coordinates: str, end_coordinates: str, 
                          start_time: Optional[str], limit: int) -> dict:
    metadata: Metadata = {
        "self": f"https://example.com/city/{city}/closest_departures",
        "city": "Wrocław",
        "query_parameters": {
            "city": city,
            "start_coordinates": start_coordinates,
            "end_coordinates": end_coordinates,
            "start_time": start_time,
            "limit": limit
        }
    }
    start_time = start_time or datetime.datetime.now().isoformat()
    departures = get_closest_departures_from_db(start_coordinates, end_coordinates, start_time, limit)
    
    return {
        "metadata": metadata,
        "departures": departures
    }