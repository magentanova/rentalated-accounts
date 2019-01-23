import os 

# CURTIS: we could be a little more clever here and write the json output of 
    # `describe-stacks` to a file, then parse it here to get table names
    # instead of hardcoding them in. just creates more setup scripts. 
# db stuff
USER_TABLE = "rentalated-accounts-db-UserTable-W0EC595B54X3"
REVOKED_TOKENS_TABLE = "rentalated-accounts-db-RevokedTokensTable-11S1XIOZAKB2Y"

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = "adrumandawire"
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'adrumandawire@gmail.com'

# misc
WEBSITE_URL = "http://localhost:5000"