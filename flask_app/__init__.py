import os

from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "stargaze_secret_key_local"
)

bcrypt = Bcrypt(app)