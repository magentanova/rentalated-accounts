from flask import request
from flask_mail import Message

import app.config as config
from app import app, mail
from app.models.user import UserModel

def auth_guard(func):
    def protectedFunc(*args,**kwargs):
        authHeader = request.headers.get('Authorization')
        authToken = None
        accepted = False

        # check for present & valid auth token 
        if authHeader:
            authToken = authHeader.split()[1]
            if authToken: 
                decoded = UserModel.decodeAuthToken(authToken)
                if decoded["valid"]:
                    accepted = True

        # if passed check, invoke wrapped function
        if accepted: 
            return func(*args,**kwargs)
        # otherwise reject request
        else: 
            return "Unauthorized request", 401
    return protectedFunc

def send_email(recipient, subject, htmlTemplate):
    msg = Message(
        subject,
        recipients=[recipient],
        html=htmlTemplate,
        sender=config.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)
