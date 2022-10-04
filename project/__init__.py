from flask import Flask
from project import email

def create_app():
    app = Flask(__name__)
    app.register_blueprint(email.bp)
    return app