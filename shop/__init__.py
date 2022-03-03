from flask import Flask

app = Flask(__name__)

from shop import routes
