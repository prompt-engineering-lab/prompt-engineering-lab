from flask import Flask
from flask_cors import CORS


from departures import departures_bp
from trips import trips_bp


app = Flask(__name__)

CORS(app)


app.register_blueprint(departures_bp)
app.register_blueprint(trips_bp)


@app.route("/")
def index():
    return "Welcome to the Public Transport API for Wrocław!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)