from flask import Blueprint, jsonify, request

from models.user import UserModel
from models.revokedToken import RevokedToken

login_api = Blueprint("login_api", __name__)

@login_api.route("/api/login", methods=["POST"])
def login():
    user_data = request.get_json()

    validLogin = True # CURTIS: does this work in terms of timing attacks?
    if not UserModel.count(user_data["email"]):
        # no such user exists
        validLogin = False

    else: 
        user_instance = UserModel.get(user_data["email"])
        if not user_instance.checkPassword(user_data['password']):
            # bad password
            validLogin = False
    
    if validLogin: 
        user_instance = UserModel.get(user_data["email"])
        return user_instance.encodeAuthToken()

    else: 
        return "Error logging in", 400

@login_api.route("/api/logout", methods=["POST"])
def logout():
    token = request.headers.get('Authorization').split()[1]
    print(len(RevokedToken.Meta.table_name))
    print(len("rentalated-accounts-db-RevokedTokensTable-11S1XIOZAKB2Y"))
    revoked_token = RevokedToken(token)
    revoked_token.save()
    return "User logged out."

