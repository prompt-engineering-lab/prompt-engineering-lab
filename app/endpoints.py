# pylint: disable=missing-function-docstring,missing-module-docstring
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/public_transport/city/<string:city>/closest_departures', methods=['GET'])
def closest_departures(city):
    # Validate the city parameter
    supported_cities = ["Wroclaw"]
    if city not in supported_cities:
        return jsonify({"error": "City not supported"}), 404

    # Get query parameters
    start_coordinates = request.args.get('start_coordinates')
    end_coordinates = request.args.get('end_coordinates')
    start_time = request.args.get('start_time', datetime.utcnow().isoformat() + 'Z')
    limit = request.args.get('limit', default=5, type=int)

    # Validate required parameters
    if not start_coordinates or not end_coordinates:
        return jsonify({"error": "Missing required parameters"}), 400

    # Process the request (mocked data for demonstration purposes)
    departures = [
        {
            "trip_id": "1",
            "route_id": "101",
            "trip_headsign": "City Center",
            "stop": {
                "name": "Main Station",
                "coordinates": {
                    "latitude": 51.1079,
                    "longitude": 17.0385
                }
            },
            "arrival_time": "2025-04-02T08:30:00Z",
            "departure_time": "2025-04-02T08:35:00Z"
        },
        # Add more mocked departure data as needed
    ][:limit]  # Limit the number of departures based on the limit parameter

    # Prepare the response
    response = {
        "metadata": {
            "self": request.url,
            "city": city,
            "query_parameters": {
                "start_coordinates": start_coordinates,
                "end_coordinates": end_coordinates,
                "start_time": start_time,
                "limit": limit
            }
        },
        "departures": departures
    }

    return jsonify(response), 200

@app.route('/public_transport/city/<string:city>/trip/<string:trip_id>', methods=['GET'])
def trip_details(city, trip_id):
    # Validate the city parameter
    supported_cities = ["Wroclaw"]
    if city not in supported_cities:
        return jsonify({"error": "City not supported"}), 404

    # Validate the trip_id parameter (mock validation for demonstration)
    if not trip_id or not isinstance(trip_id, str):
        return jsonify({"error": "Invalid trip ID"}), 400

    # Process the request (mocked data for demonstration purposes)
    trip = {
        "trip_id": trip_id,
        "route_id": "101",
        "trip_headsign": "City Center",
        "stops": [
            {
                "name": "Main Station",
                "coordinates": {
                    "latitude": 51.1079,
                    "longitude": 17.0385
                },
                "arrival_time": "2025-04-02T08:30:00Z",
                "departure_time": "2025-04-02T08:35:00Z"
            },
            {
                "name": "Market Square",
                "coordinates": {
                    "latitude": 51.1109,
                    "longitude": 17.0385
                },
                "arrival_time": "2025-04-02T08:40:00Z",
                "departure_time": "2025-04-02T08:45:00Z"
            }
            # Add more mocked stop data as needed
        ]
    }

    # Prepare the response
    response = {
        "metadata": {
            "self": request.url,
            "city": city,
            "query_parameters": {
                "trip_id": trip_id
            }
        },
        "trip_details": trip
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
