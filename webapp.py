import os

from flask import Flask, Response, request, send_from_directory

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
    
    def generate():
        yield "data: 0\n\n"
        frame_cap(ip, fps, timeout)
        yield "data: 100\n\n"

    return Response(generate(), mimetype='text/event-stream')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('uploads', 'upload')
        f.save(filename)

        def generate():
            yield "data: 0\n\n"
            input_vid(filename)
            yield "data: 100\n\n"

        return Response(generate(), mimetype='text/event-stream')
