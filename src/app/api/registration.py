import datetime
from flask import Blueprint, jsonify, request

import app.config as config
from app.utils import send_email
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
    
    # good to go
    user_instance = UserModel(
        user_data["email"], 
        CreatedAt=datetime.datetime.utcnow(),
        FirstName=user_data["first_name"], 
        LastName=user_data["last_name"],
    )
    user_instance.setPasswordHash(user_data["password"])

    email_template = """
        <h1>Rentalated</h1>
        <a href="{}/activate/hashofemailandtimestamp">
            <p>Click this link to activate your account!</p>
        </a>
    """.format(config.WEBSITE_URL)

    send_email(
        user_data["email"], 
        "The time has come for you to confirm your Rentalated account.",
        email_template
        )
    # user_instance.save()

    # publish to SNS topic
    ## ???
    ## ???
    return jsonify({
        "msg": "user saved && confimrmation email sent",
        "saved_user": user_instance.serialize()
    })