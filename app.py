import os
from flask import Flask
from dotenv import load_dotenv

from config import Config
from models import db, init_db
from views import probes_bp, asteroids_bp, gamestate_bp

load_dotenv()

def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    init_db(app)

    app.register_blueprint(gamestate_bp) 
    app.register_blueprint(probes_bp)
    app.register_blueprint(asteroids_bp)

    return app



if __name__ == "__main__":
    app = create_app()

    # Show Jinja loader info only in development environment
    if os.environ.get('FLASK_ENV') == 'development':  # Access config this way
        print("Jinja2 Loader:", app.jinja_loader)
        for template_path in app.jinja_loader.searchpath:
            print("Search Path:", template_path)

    app.run(debug=True, port=5005)