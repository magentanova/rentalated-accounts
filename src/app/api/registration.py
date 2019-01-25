import datetime
from flask import Blueprint, jsonify, request
from itsdangerous import URLSafeTimedSerializer

import app.config as config
from app.utils import decode_activation_token, encode_activation_token, send_email
from app.models.user import UserModel

registration_api = Blueprint("registration_api", __name__)

@registration_api.route("/api/register", methods=["POST"])
def register():
    user_data = request.get_json()

    # user exists
    if UserModel.count(user_data["email"]):
        return jsonify("Email already registered"), 400

    # incomplete user data
    if not all([
        user_data.get("first_name"), 
        user_data.get("last_name"), 
        user_data.get("password")
        ]):
        return jsonify("You must provide an email, first_name, last_name, and password"), 400
    
    # good to go, let's get them registered
    user_instance = UserModel(
        user_data["email"], 
        created_at=datetime.datetime.utcnow(),
        first_name=user_data["first_name"], 
        last_name=user_data["last_name"],
    )

    # hash the password
    user_instance.setPasswordHash(user_data["password"])

    # compose and send activation email
    email_template = """
        <h1>Rentalated</h1>
        <a href="{url}/test/activate/{encoded_id}">
            <p>Click this link to activate your account!</p>
        </a>
    """.format(url=config.WEBSITE_URL, encoded_id=encode_activation_token(user_data["email"]))

    send_email(
        user_data["email"], 
        "The time has come for you to activate your Rentalated account.",
        email_template
    )

    # save the user with .activated=False
    user_instance.save()

    return jsonify({
        "msg": "user saved && activation email sent",
        "saved_user": user_instance.serialize()
    })

@registration_api.route("/api/activate/<activation_token>", methods=["POST"])
def activate(activation_token):
    email = decode_activation_token(activation_token)
    if email: 
        user_instance = UserModel.get(email)
        if user_instance.active:
            return "account already activated", 400
        user_instance.update(actions=[
            UserModel.active.set(True)
        ])
        # publish to SNS topic
        ## ???
        ## ???
        ## CURTIS: i went ahead and set this up, i think i get it now, should be fine, 
        ### just haven't done it yet. and hard to test it without starting work on the 
        ### other services
        return jsonify(user_instance.serialize())
    else: 
        return "invalid activation token", 400