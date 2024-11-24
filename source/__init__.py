import os
from flask import Flask
from mongoengine import *
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)

    CORS(app)

    connect(host=os.environ.get('MONGO_URL'), alias='STORE')

    from .routes.route_admin import admin_routes
    app.register_blueprint(admin_routes)
    
    from .routes.route_cart import cart_routes
    app.register_blueprint(cart_routes)

    from .routes.route_orders import orders_routes
    app.register_blueprint(orders_routes)

    from .routes.route_dashboard import dashboard_routes
    app.register_blueprint(dashboard_routes)

    return app