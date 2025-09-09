from flask import Flask, send_from_directory
import os

from flask import jsonify, request

app = Flask(__name__, static_folder='frontend')


# Serwuj index.html z folderu frontend
@app.route('/')
def root():
    return send_from_directory('frontend', 'index.html')


# Serwuj pliki statyczne (JS, CSS, itp.) z folderu frontend
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('frontend', path)


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

if __name__ == '__main__':
    app.run(debug=True)
