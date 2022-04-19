import os
from flask import Flask

app = Flask(__name__)

app = Flask(__name__, static_folder="static")

app.config['SECRET_KEY'] = '<7e5a36d7d8a56464191621dd38c0a35d6da35e3c088a3ce5>'

from shop import routes
