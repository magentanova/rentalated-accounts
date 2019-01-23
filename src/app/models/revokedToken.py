from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from config import REVOKED_TOKENS_TABLE

class RevokedToken(Model):
    class Meta:
        table_name = REVOKED_TOKENS_TABLE
    Access_token = UnicodeAttribute(hash_key=True)
    @staticmethod
    def check(token):
        try:
            RevokedToken.get(token)
            return True

        except RevokedToken.DoesNotExist:
            return False