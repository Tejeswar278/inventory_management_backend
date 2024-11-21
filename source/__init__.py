import os
from flask import Flask
from mongoengine import *
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    connect(host=os.environ.get('MONGO_URL'), db=os.environ.get('MONGO_DATABASE'), port=int(os.environ.get('MONGO_PORT')), alias='TICKET')

    from .routes.route import routes
    app.register_blueprint(routes)

    return app