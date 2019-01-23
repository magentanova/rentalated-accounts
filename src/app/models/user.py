import os
import jwt
import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.revokedToken import RevokedToken
from app.config import USER_TABLE

JWT_SECRET = os.environ["JWT_SECRET"]

class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = USER_TABLE
        region = "us-east-2"
    Email = UnicodeAttribute(hash_key=True)
    FirstName = UnicodeAttribute()
    LastName = UnicodeAttribute()
    PasswordHash = UnicodeAttribute()
    CreatedAt = UTCDateTimeAttribute()

    def checkPassword(self,password):
        return check_password_hash(self.PasswordHash, password)

    @staticmethod
    def decodeAuthToken(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        # CURTIS: for security purposes, i purposely am not telling them whether 
            # they had a nonsense, expired, or revoked tokens
        errorResponse = {
            "valid": False,
            "payload": None,
            "error_message": "Bad auth token."
        }
        successResponse = {
                    "valid": True,
                    "payload": None,
                    "error_message": None
                }
        try:
            payload = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
            if RevokedToken.check(auth_token):
                return errorResponse
            else:
                successResponse["payload"] = payload["sub"]
                return successResponse
        except (jwt.ExpiredSignatureError,  jwt.InvalidTokenError):
            return errorResponse
        

    def encodeAuthToken(self):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            "exp": int((datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp()),
            "iat": int(datetime.datetime.utcnow().timestamp()),
            "sub": self.Email
        }
        encoded = jwt.encode(
            payload,
            JWT_SECRET,
            algorithm="HS256"
        )
        print(encoded)
        return encoded
        
    def serialize(self):
        d = {}
        for name, attr in self._get_attributes().items():
            if name != "Password":
                d[name] = attr.serialize(getattr(self, name))
            if isinstance(attr, datetime.datetime):
                d[name] = attr.strftime("%Y-%m-%d %H:%M:%S")
        return d

    def setPasswordHash(self,pw):
        self.PasswordHash = generate_password_hash(pw,method="pbkdf2:sha256")
