from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.settings import settings
from app.signup.router import signup_router

settings = settings()

app = Flask(__name__)
app.secret_key = settings.flask_secret
app.register_blueprint(signup_router)


@app.route("/")
def home():
    return "<p>Hello, World!</p>"
