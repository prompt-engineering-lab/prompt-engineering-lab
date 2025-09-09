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

# Przykładowy endpoint API
@app.route('/api/closest_departures', methods=['POST'])
def api_closest_departures():
    # Przykładowe dane, docelowo pobierane z bazy
    data = request.get_json() or {}
    # Możesz tu wykorzystać np. data['lat'], data['lng']
    example = {
        "departures": [
            {"line": "105", "direction": "Dworzec Główny", "departure_time": "12:34"},
            {"line": "132", "direction": "Plac Grunwaldzki", "departure_time": "12:40"}
        ],
        "query": data
    }
    return jsonify(example)

if __name__ == "__main__":
    app.run(debug=True, port=5001)