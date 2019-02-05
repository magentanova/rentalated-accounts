from flask import send_file
from flask_cors import CORS

from app import app
from app.api.account import account_api
from app.api.registration import registration_api
from app.api.login import login_api

app.register_blueprint(account_api)
app.register_blueprint(login_api)
app.register_blueprint(registration_api)

CORS(app)

@app.route("/")
def hello():
    return "Welcome to the rentalated accounts api. Hamberders"

@app.route("/test/activate/<user_id>")
def activationPage(user_id):
    return send_file("test_activation.html")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
