import os
from flask import Flask
from dotenv import load_dotenv

from config import Config
from models import db
from utils.db import init_db # Function to initialize database

from views import probes_bp, asteroids_bp


import json




load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(probes_bp)

    app.register_blueprint(asteroids_bp)

    from utils.db import init_db  # Import here to avoid circular imports
    init_db(app) # Pass the app to init_db()


    return app




if __name__ == "__main__":
    app = create_app()

    print("Jinja2 Loader:", app.jinja_loader)
    for template_path in app.jinja_loader.searchpath:
        print("Search Path:", template_path)

    app.run(debug=True, port=5005)
