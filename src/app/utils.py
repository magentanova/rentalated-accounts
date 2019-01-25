import json
import requests
from flask import request, jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

import app.config as config
from app import app, current_user, mail
from app.models.user import UserModel

def auth_guard(func):
    def protected_func(*args,**kwargs):
        auth_header = request.headers.get('Authorization')
        print(json.dumps(auth_header))
        # send the header to the token service for validation
        response = requests.post("{}/token_service".format(config.TOKEN_SERVICE_URL), 
            json={
                "auth_header": auth_header
            })
        if response.status_code != 200: 
            return jsonify(response.text), response.status_code
        else:
            current_user["email"] = response.json()["payload"]
            return func(*args,**kwargs)

    protected_func.__name__ = func.__name__ 
    # ^^ fixes an error caused by wrapping multiple functions with the same decorator
    return protected_func

def encode_activation_token(email):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    return serializer.dumps(email)

def decode_activation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            max_age=expiration
        )
    except Exception as e:
        print(e)
        return False
    return email

def send_email(recipient, subject, htmlTemplate):
    msg = Message(
        subject,
        recipients=[recipient],
        html=htmlTemplate,
        sender=config.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)
