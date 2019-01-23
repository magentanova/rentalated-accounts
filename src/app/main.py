from flask import Flask

from api.registration import registration_api
from api.login import login_api

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(registration_api)

@app.route("/")
def hello():
    return "Welcome to the rentalated accounts api."

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
