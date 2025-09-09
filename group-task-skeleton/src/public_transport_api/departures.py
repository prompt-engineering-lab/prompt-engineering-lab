from flask import Blueprint, jsonify
import sqlite3
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
    # TODO handle request parameters and add the metadata. Include error handling.
    return jsonify(get_closest_departures())

def get_closest_departures():
    """
    FIXME this is a mock version. You need to implement the correct logic
    """
    conn = None
    try:
        conn = sqlite3.connect("trips.sqlite")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops LIMIT 1;"
        cursor.execute(query)
        first_stop_row = cursor.fetchone()

        mock_departures = []

        if first_stop_row:
            mock_departure = {
                "trip_id": "mock_trip_001",
                "route_id": "mock_route_A",
                "trip_headsign": first_stop_row['stop_name'],
                "stop": {
                    "id": first_stop_row['stop_id'],
                    "name": first_stop_row['stop_name'],
                    "coordinates": {
                        "latitude": float(first_stop_row['stop_lat']),
                        "longitude": float(first_stop_row['stop_lon'])
                    },
                    "arrival_time": "10:00:00",
                    "departure_time": "10:00:30"
                },
                "distance_start_to_stop": 123.45,
                "debug_dist_stop_to_end": 543.21
            }
            mock_departures.append(mock_departure)

        return mock_departures

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()
