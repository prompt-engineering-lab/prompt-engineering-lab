import sqlite3
from typing import List, Optional

from ..models import TripDetails, TripResponse, Stop, Coordinates, Metadata, QueryParameters
from ..db_models import TripBasicInfo, StopInfo
from ..exceptions import TripNotFoundError


def _get_trip_basic_info(trip_id: str) -> Optional[TripBasicInfo]:
    conn = sqlite3.connect('trips.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT route_id, trip_headsign
        FROM trips
        WHERE trip_id = ?
    """, (trip_id,))
    trip_row = cursor.fetchone()
    
    conn.close()
    return TripBasicInfo(*trip_row) if trip_row else None


def _get_trip_stops(trip_id: str) -> List[StopInfo]:
    conn = sqlite3.connect('trips.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.stop_name, s.stop_lat, s.stop_lon, 
               st.arrival_time, st.departure_time
        FROM stop_times st
        JOIN stops s ON st.stop_id = s.stop_id
        WHERE st.trip_id = ?
        ORDER BY st.stop_sequence
    """, (trip_id,))
    stop_rows = cursor.fetchall()
    
    conn.close()
    return [StopInfo(*row) for row in stop_rows]


def get_trip_details_from_db(trip_id: str) -> TripDetails:
    trip_info = _get_trip_basic_info(trip_id)
    
    if not trip_info:
        raise TripNotFoundError(f"Trip with ID '{trip_id}' not found")

    stop_infos = _get_trip_stops(trip_id)

    stops: List[Stop] = []
    for stop_info in stop_infos:
        coordinates: Coordinates = {
            "latitude": stop_info.stop_lat,
            "longitude": stop_info.stop_lon
        }
        stop: Stop = {
            "name": stop_info.stop_name,
            "coordinates": coordinates,
            "arrival_time": stop_info.arrival_time,
            "departure_time": stop_info.departure_time
        }
        stops.append(stop)

    trip_details: TripDetails = {
        "trip_id": trip_id,
        "route_id": trip_info.route_id,
        "trip_headsign": trip_info.trip_headsign,
        "stops": stops
    }
    return trip_details


def get_trip_details(trip_id: str, city: str) -> TripResponse:
    query_params: QueryParameters = {"trip_id": trip_id, "city": city}
    metadata: Metadata = {
        "self": f"https://example.com/city/{city}/trips/{trip_id}",
        "city": "Wrocław",
        "query_parameters": query_params
    }
    
    try:
        trip_details = get_trip_details_from_db(trip_id)
        response: TripResponse = {
            "metadata": metadata,
            "trip_details": trip_details
        }
        return response
    except TripNotFoundError:
        response: TripResponse = {
            "metadata": metadata,
            "trip_details": None
        }
        return response
