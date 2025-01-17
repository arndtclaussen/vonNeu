import os
import redis

from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from rq import Queue
import rq_dashboard

# Configuration and Models
from config import Config
from models import db, init_db


# Blueprints (Views)
from views import gamestate_bp, gamerate_bp, general_bp, space_bp, assets_bp, gamelog_bp

import logging

# Load environment variables
load_dotenv()
from flask_socketio import SocketIO

# Create a global Redis connection and RQ queue
redis_conn = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)
q = Queue(connection=redis_conn)  # Use default queue or specify a name like 'low', 'medium', 'high'


def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # RQ Dashboard Configuration (Important: before registering blueprints)
    app.config.from_object(rq_dashboard.default_settings)  # Apply default settings
    rq_dashboard.web.setup_rq_connection(app) # Connects the dashboard to your Redis instance
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")



    db.init_app(app)  # Initialize db with the app
    # Database initialization
    with app.app_context():  # Use app context for DB operations
        from models import init_db  # Import inside app context
        init_db(app)

        

    # Make 'q' (RQ queue) accessible to blueprints
    app.config['RQ_QUEUE'] = q # Store it like this
    app.config['RQ_CONNECTION'] = redis_conn # Store it like this

 
    app.register_blueprint(gamestate_bp) 
    app.register_blueprint(gamerate_bp)
    app.register_blueprint(gamelog_bp)
    
    app.register_blueprint(general_bp)   

    app.register_blueprint(space_bp)
    app.register_blueprint(assets_bp) 


    socketio = SocketIO(app, message_queue=os.getenv('REDIS_URL'), cors_allowed_origins="*")
    app.socketio = socketio # Correctly assigning app.socketio
    return app # Correctly returning only the Flask app



if __name__ == '__main__':
    app = create_app()  # Fix: Call create_app() to get the app
    
    if os.environ.get('FLASK_ENV') == 'development':
        print("Jinja2 Loader:", app.jinja_loader)  # Accessing app attributes works here
        for template_path in app.jinja_loader.searchpath:
            print("Search Path:", template_path)
        print(app.url_map)  # Now this works as app is a Flask object

    app.socketio.run(app)