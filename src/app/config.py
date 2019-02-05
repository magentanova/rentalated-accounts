import os 

# CURTIS: we could be a little more clever here and write the json output of 
    # `describe-stacks` to a file, then parse it here to get table names
    # instead of hardcoding them in. just creates more setup scripts. 

    # ^^ actually this is now a todo

# db stuff
USER_TABLE = "rentalated-accounts-db-UserTable-1U4BFK8R9EE8B"
REVOKED_TOKENS_TABLE = "rentalated-accounts-db-RevokedTokensTable-1VIEA9RVNWJKG"

# encoding secrets
SECRET_KEY=os.environ["SECRET_KEY"]

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

# domains for other services
if os.environ["ENVIRONMENT"] == "production": 
    WEBSITE_URL = "???"
    TOKEN_SERVICE_URL = "https://fo82pqxd3j.execute-api.us-east-2.amazonaws.com/Prod/"

else:
    WEBSITE_URL = "http://localhost:5000" 
    TOKEN_SERVICE_URL = "https://fo82pqxd3j.execute-api.us-east-2.amazonaws.com/Prod/"


