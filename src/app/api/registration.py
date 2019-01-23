import datetime
from flask import Blueprint, jsonify, request

from models.user import UserModel

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
        Created_at=datetime.datetime.utcnow(),
        First_name=user_data["first_name"], 
        Last_name=user_data["last_name"],
    )
    user_instance.setPasswordHash(user_data["password"])
    user_instance.save()

    # publish to SNS topic
    ## ???
    ## ???
    return jsonify({
        "msg": "user saved",
        "saved_user": user_instance.serialize()
    })