from flask import request
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

import app.config as config
from app import app, mail
from app.models.user import UserModel

def auth_guard(func):
    # should be replaced with a call to a token validation service, 
        # which performs the below
    def protectedFunc(*args,**kwargs):
        authHeader = request.headers.get('Authorization')
        authToken = None
        accepted = False
        active = False

        # check for present & valid auth token 
        if authHeader:
            authToken = authHeader.split()[1]
            if authToken: 
                decoded = UserModel.decodeAuthToken(authToken)
                if decoded["valid"]:
                    accepted = True
                    email = decoded["payload"]
                    user_instance = UserModel.get(email)
                    if user_instance.active:
                        active = True

        # if passed check, invoke wrapped function
        if accepted: 
            if active: 
                return func(*args,**kwargs)
            else: 
                return "Unathorized request: User account not active", 401
        # otherwise reject request
        else: 
            return "Unauthorized request: Missing or invalid auth token", 401
    return protectedFunc

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
