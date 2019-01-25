from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from app.config import REVOKED_TOKENS_TABLE

class RevokedToken(Model):
    class Meta:
        table_name = REVOKED_TOKENS_TABLE
        region = "us-east-2"
    accessToken = UnicodeAttribute(hash_key=True)
    @staticmethod ### CURTIS: this is also something that for the moment 
    ### has been moved to the token service.
    def check(token):
        try:
            RevokedToken.get(token)
            return True

        except RevokedToken.DoesNotExist:
            return False