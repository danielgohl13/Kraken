from flask import Flask, send_from_directory, request


app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory("web", "index.html")

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory("web/assets", path)