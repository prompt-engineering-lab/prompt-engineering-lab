from flask import Blueprint, jsonify
import sqlite3
from typing import List, Optional

from models import TripDetails, TripResponse, Stop, Coordinates, Metadata, QueryParameters
from db_models import TripBasicInfo, StopInfo
from exceptions import TripNotFoundError

trips_bp = Blueprint('trips', __name__, url_prefix='/public_transport/city/<string:city>/trip')

@trips_bp.route("/<string:trip_id>", methods=["GET"])
def handle_trip_details(trip_id: str, city: str = "Wroclaw"):
    """
    Retrieves details about a specific trip, including its route, headsign, and stop details.

    Endpoint:
        GET /public_transport/city/<city>/trip/<trip_id>

    Parameters:
        Path Parameters:
        - city (str): Specifies the city for which trip details are requested. Currently, only "wroclaw" is supported.
        - trip_id (str): The unique identifier of the trip whose details need to be retrieved.

    Returns:
        JSON response containing:
        - metadata: Information about the request, including the URL and query parameters.
        - trip_details: Details of the trip, including trip_id, route_id, trip_headsign, and a list of stops with their names, coordinates, arrival times, and departure times.

    Errors:
        - 400 Bad Request: If the city is not "wroclaw".
        - 404 Not Found: If the trip with the specified trip_id is not found.

    Example Response:
    {
        "metadata": {
            "self": "/public_transport/city/wroclaw/trip/3_14613060",
            "city": "wroclaw",
            "trip_id": "3_14613060"
        },
        "trip_details": {
            "trip_id": "3_14613060",
            "route_id": "A",
            "trip_headsign": "KRZYKI",
            "stops": [
                {
                    "name": "Plac Grunwaldzki",
                    "coordinates": {
                        "latitude": 51.1092,
                        "longitude": 17.0415
                    },
                    "arrival_time": "2025-04-02T08:34:00Z",
                    "departure_time": "2025-04-02T08:35:00Z"
                },
                {
                    "name": "Renoma",
                    "coordinates": {
                        "latitude": 51.1040,
                        "longitude": 17.0280
                    },
                    "arrival_time": "2025-04-02T08:39:00Z",
                    "departure_time": "2025-04-02T08:40:00Z"
                },
                {
                    "name": "Dominikański",
                    "coordinates": {
                        "latitude": 51.1099,
                        "longitude": 17.0335
                    },
                    "arrival_time": "2025-04-02T08:44:00Z",
                    "departure_time": "2025-04-02T08:45:00Z"
                }
            ]
        }
    """
    # TODO handle the city and the metadata. Add also error handling (i.e.: 404)
    return jsonify(get_trip_details(trip_id=trip_id, city=city))


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
                   SELECT s.stop_name,
                          s.stop_lat,
                          s.stop_lon,
                          st.arrival_time,
                          st.departure_time
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
