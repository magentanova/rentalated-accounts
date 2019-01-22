from flask import Blueprint, jsonify, request

registration_api = Blueprint("registration_api", __name__)

@registration_api.route('/api/register')
def register():
    data = request.get_json()
    return jsonify({
        "msg": "user data schnogged!",
        "user data": data
    })