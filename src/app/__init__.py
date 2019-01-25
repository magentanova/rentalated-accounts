from flask import Flask
from flask_mail import Mail 

app = Flask(__name__)
app.config.from_object('app.config')
mail = Mail(app)
current_user = {
    "email": None
}