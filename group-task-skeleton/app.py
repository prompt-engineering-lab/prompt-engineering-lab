from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='frontend')


# Serwuj index.html z folderu frontend
@app.route('/')
def root():
    return send_from_directory('frontend', 'index.html')


# Serwuj pliki statyczne (JS, CSS, itp.) z folderu frontend
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(debug=True)
