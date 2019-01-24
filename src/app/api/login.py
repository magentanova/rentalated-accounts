from flask import Blueprint, jsonify, request

from app.utils import auth_guard
from app.models.user import UserModel
from app.models.revokedToken import RevokedToken

login_api = Blueprint("login_api", __name__)

@login_api.route("/api/login", methods=["POST"])
def login():
    user_data = request.get_json()

    validLogin = False # CURTIS: does this work in terms of timing attacks?
    # switch this to true iff they exist, their password checks out, 
        # and their account is active.
    if UserModel.count(user_data["email"]):
        user_instance = UserModel.get(user_data["email"])
        if user_instance.checkPassword(user_data['password']):
            if user_instance.active: 
                validLogin = True
    
    if validLogin: 
        user_instance = UserModel.get(user_data["email"])
        return user_instance.encodeAuthToken()

    else: 
        return "Error logging in", 400

@login_api.route("/api/logout", methods=["POST"])
@auth_guard
def logout():
    token = request.headers.get('Authorization').split()[1]
    revoked_token = RevokedToken(token)
    revoked_token.save()
    return "User logged out."

