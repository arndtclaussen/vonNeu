import os
from dotenv import load_dotenv

import rq
import rq_dashboard

from flask import Flask, render_template, jsonify, request
from redis import Redis

from app.config import Config
from app.extensions import db  

from app.blueprints.main import main

load_dotenv() # load environment variables

def create_app(): 
    app = Flask(__name__)

    app.config.from_object(Config)

    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue(connection=app.redis)

    
    # Make 'q' (RQ queue) accessible to blueprints
    app.config['RQ_QUEUE'] = app.task_queue 
    app.config['RQ_CONNECTION'] = app.redis 

    register_extensions(app)
    register_blueprints(app)
    register_rq_dashboard(app)

    return app



def register_extensions(app: Flask):
    db.init_app(app)

def register_blueprints(app: Flask):
    app.register_blueprint(main)

def register_rq_dashboard(app: Flask):
    app.config.from_object(rq_dashboard.default_settings)
    rq_dashboard.web.setup_rq_connection(app)
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")