from flask import send_file

from app import app
from app.api.account import account_api
from app.api.registration import registration_api
from app.api.login import login_api

app.register_blueprint(account_api)
app.register_blueprint(login_api)
app.register_blueprint(registration_api)

@app.route("/")
def hello():
    return "Welcome to the rentalated accounts api. Hamberders"

# @app.route("/activate/<user_id>")
# def activate(user_id):
#     return "Some day you'll be able to activate your account!"

@app.route("/test/activate/<user_id>")
def activationPage(user_id):
    return send_file("test_activation.html")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
