from time import localtime, strftime

from flask import Flask, jsonify, render_template
from flask_static_compress import FlaskStaticCompress

from .db import get_data

app = Flask(__name__)
compress = FlaskStaticCompress(app)


@app.route("/")
def index():
    data, options = get_data()
    return render_template(
        "index.html", data=data, options=options, time=strftime("%H:%M", localtime())
    )


@app.route("/api")
def api():
    return jsonify(get_data()[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
