from flask import Flask, json, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route("/")
def index():
    return json.dumps({ 'result': 200 })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
