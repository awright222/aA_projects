from flask import Flask
import os
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    app.register_blueprint(bp)
    return app