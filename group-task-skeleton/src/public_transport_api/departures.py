from flask import Blueprint, jsonify, request
import sqlite3
from datetime import datetime
import math
departures_bp = Blueprint('departures', __name__, url_prefix='/public_transport/city/<string:city>/closest_departures')

@departures_bp.route("/", methods=["GET"])
def closest_departures(city):
    """
    The endpoint returns the closest departures of lines that bring the user closer to the destination.
	Lines that start in the opposite direction shall not be displayed.
	Departures are sorted by distance from start_coordinates in ascend-ing order (the closest first).
	The endpoint does not consider which line brings the user closer to the destination.

    Request Parameters:
        Path Parameters:
        - city (required): The city for the public transport search. Currently, on-ly "wroclaw" is supported.
        Query Parameters:
        - start_coordinates (required): The geolocation coordinates where the user wants to start the trip.
        - end_coordinates (required): The geolocation coordinates where the user wants to finish the trip.
        - start_time (optional, default: current time): The time at which the us-er starts the trip.
        - limit (optional, default: 5): The maximum number of departures to be returned.
    """
    # Validate city
    if city.lower() != "wroclaw":
        return jsonify({"error": "Only 'wroclaw' city is supported"}), 400

    # Get required parameters
    start_coordinates = request.args.get('start_coordinates')
    end_coordinates = request.args.get('end_coordinates')

    if not start_coordinates:
        return jsonify({"error": "start_coordinates parameter is required"}), 400
    if not end_coordinates:
        return jsonify({"error": "end_coordinates parameter is required"}), 400

    # Validate coordinate format (lat,lon)
    try:
        start_lat, start_lon = map(float, start_coordinates.split(','))
        end_lat, end_lon = map(float, end_coordinates.split(','))
    except (ValueError, AttributeError):
        return jsonify({"error": "Coordinates must be in format 'lat,lon'"}), 400

    # Get optional parameters
    start_time = request.args.get('start_time', datetime.now().strftime('%H:%M:%S'))
    try:
        limit = int(request.args.get('limit', 5))
        if limit <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "limit must be a positive integer"}), 400

    departures = get_closest_departures(start_lat, start_lon, end_lat, end_lon, start_time, limit)
    return jsonify(departures)

def get_closest_departures(start_lat, start_lon, end_lat, end_lon, start_time, limit):
    conn = None
    try:
        conn = sqlite3.connect("trips.sqlite")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get stops with departures after start_time
        query = """
        SELECT DISTINCT s.stop_id, s.stop_name, s.stop_lat, s.stop_lon,
               st.trip_id, t.route_id, t.trip_headsign, st.arrival_time, st.departure_time
        FROM stops s
        JOIN stop_times st ON s.stop_id = st.stop_id
        JOIN trips t ON st.trip_id = t.trip_id
        WHERE st.departure_time >= ?
        """
        cursor.execute(query, (start_time,))
        departures = cursor.fetchall()

        results = []
        for dep in departures:
            stop_lat, stop_lon = float(dep['stop_lat']), float(dep['stop_lon'])

            # Calculate distances
            dist_start_to_stop = haversine_distance(start_lat, start_lon, stop_lat, stop_lon)
            dist_stop_to_end = haversine_distance(stop_lat, stop_lon, end_lat, end_lon)
            dist_start_to_end = haversine_distance(start_lat, start_lon, end_lat, end_lon)

            # Filter: only include if stop is closer to end than start is to end
            if dist_stop_to_end < dist_start_to_end:
                results.append({
                    "trip_id": dep['trip_id'],
                    "route_id": dep['route_id'],
                    "trip_headsign": dep['trip_headsign'],
                    "stop": {
                        "id": dep['stop_id'],
                        "name": dep['stop_name'],
                        "coordinates": {
                            "latitude": stop_lat,
                            "longitude": stop_lon
                        },
                        "arrival_time": dep['arrival_time'],
                        "departure_time": dep['departure_time']
                    },
                    "distance_start_to_stop": dist_start_to_stop,
                    "debug_dist_stop_to_end": dist_stop_to_end
                })

        # Sort by distance from start and limit results
        results.sort(key=lambda x: x['distance_start_to_stop'])
        return results[:limit]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
