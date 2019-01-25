import os
import jwt
import datetime
from pynamodb.models import Model
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.revokedToken import RevokedToken
from app.config import USER_TABLE, SECRET_KEY


class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = USER_TABLE
        region = "us-east-2"
    email = UnicodeAttribute(hash_key=True)
    active = BooleanAttribute(default=False)
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    password_hash = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()

    def checkPassword(self,password):
        return check_password_hash(self.password_hash, password)        

    ### vvv CURTIS: maybe this kind of thing should move to the token service. have 
        ### some questions there. 
    def encodeAuthToken(self):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            "exp": int((datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp()),
            "iat": int(datetime.datetime.utcnow().timestamp()),
            "sub": self.email
        }
        encoded = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
        )
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
        self.password_hash = generate_password_hash(pw,method="pbkdf2:sha256")
        return self.password_hash
