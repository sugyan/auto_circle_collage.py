from flask import Flask, request, jsonify, render_template

import cv2
import base64
import numpy as np
import urllib
from lib.mizutama import Mizutama

app = Flask(__name__)
app.debug = True

@app.route('/api')
def api():
    url = request.args.get('url')
    if url is None:
        return jsonify(error='"url" is required.')
    try:
        data = urllib.urlopen(url).read()
    except Exception:
        return jsonify(error='urlopen failed.')

    buf = np.fromstring(data, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify(error='read image failed.')

    mizutama = Mizutama(img)
    img = mizutama.collage()
    return jsonify(image='data:image/jpeg;base64,' + base64.b64encode(cv2.imencode('.jpg', img)[1]), url=url)

@app.route('/')
def main():
    return render_template('index.html')
