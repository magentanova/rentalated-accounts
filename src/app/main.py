from flask import Flask
from api.registration import registration_api
import os 

app = Flask(__name__)
app.register_blueprint(registration_api)

@app.route("/")
def hello():
    return "Hello World from flask"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
