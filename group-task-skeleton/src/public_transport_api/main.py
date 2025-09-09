import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

from departures import departures_bp
from trips import trips_bp


FRONTEND_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
app = Flask(__name__, static_folder=FRONTEND_FOLDER)
CORS(app)

app.register_blueprint(departures_bp)
app.register_blueprint(trips_bp)

# Serwuj index.html z katalogu frontend
@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

# Serwuj pliki statyczne (JS, CSS, itp.) z katalogu frontend
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Endpoint: najbliższy przystanek na podstawie współrzędnych
import sqlite3

@app.route('/api/closest_departures', methods=['POST'])
def api_closest_departures():
    data = request.get_json() or {}
    lat = data.get('lat')
    lng = data.get('lng')
    if lat is None or lng is None:
        return jsonify({'error': 'Brak współrzędnych lat/lng'}), 400

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../trips.sqlite'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = '''
        SELECT stop_id, stop_name, stop_lat, stop_lon,
               ((stop_lat - ?)*(stop_lat - ?) + (stop_lon - ?)*(stop_lon - ?)) AS dist
        FROM stops
        ORDER BY dist ASC
        LIMIT 1;
    '''
    cursor.execute(query, (lat, lat, lng, lng))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Brak przystanków w bazie'}), 404

    result = {
        'closest_stop': {
            'stop_id': row['stop_id'],
            'stop_name': row['stop_name'],
            'stop_lat': row['stop_lat'],
            'stop_lon': row['stop_lon'],
            'distance': row['dist']
        },
        'query': {'lat': lat, 'lng': lng}
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)