import os


from flask import Flask, send_from_directory, request
from frame_cap import frame_cap
from input_cap import input_vid

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory("web", "index.html")


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory("web/assets", path)


@app.route("/cap")
def cap():
    ip = request.args.get("ip", "")
    timeout = request.args.get("timeout", 5.0)
    fps = request.args.get("fps", 24)
    return frame_cap(ip, fps, timeout)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('uploads', 'upload')
        f.save(filename)

        return input_vid(filename)
