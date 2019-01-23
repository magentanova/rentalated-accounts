from app import app
from app.api.registration import registration_api
from app.api.login import login_api

app.register_blueprint(login_api)
app.register_blueprint(registration_api)

@app.route("/")
def hello():
    return "Welcome to the rentalated accounts api. Hamberders"

@app.route("/activate/<user_id>")
def activate(user_id):
    return "Some day you'll be able to activate your account!"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
