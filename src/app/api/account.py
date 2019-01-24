from flask import Blueprint, jsonify, request

import app.config as config
from app.utils import auth_guard
from app.models.user import UserModel

account_api = Blueprint("account_api", __name__)

@account_api.route("/api/account/deactivate", methods=["PUT"])
@auth_guard
def deactivate_account():
    user_data = request.get_json()
    user_instance = UserModel.get(user_data.get("email"))
    user_instance.update(attributes={
        "active": {
            "value": False,
            "action": "PUT"
            }
    })
    return jsonify(user_instance.serialize())


@account_api.route("/api/account", methods=["PUT"])
@auth_guard
def update_account():
    user_data = request.get_json()
    user_instance = UserModel.get(user_data.get("email"))
    new_email = user_data.get("new_email")
    if new_email: 
        # create new user

        # delete old user 

        # PUBLISH to SNS feed
        pass
    else: 
        user_instance.update(attributes={
            "first_name": {
                "value": user_data.get("first_name") or user_instance.get("first_name"),
                "action": "PUT"
                },
            "last_name": {
                "value": user_data.get("last_name") or user_instance.get("last_name"),
                "action": "PUT"
                },
            "password_hash": {
                "value": user_instance.setPasswordHash(user_data.get("password")) if user_data.get("password") else user_instance.password_hash,
                "action": "PUT"
                }
        })
    # PUBLISH TO SNS FEED
    # ??
    return jsonify(user_instance.serialize())

