import os
from flask import Flask
from dotenv import load_dotenv

from config import Config
from models import db, init_db  # Import init_db directly from models
from views import probes_bp, asteroids_bp

load_dotenv()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    init_db(app)  # Call init_db here

    app.register_blueprint(probes_bp)

    app.register_blueprint(asteroids_bp)


    return app



if __name__ == "__main__":
    app = create_app()

    print("Jinja2 Loader:", app.jinja_loader)
    for template_path in app.jinja_loader.searchpath:
        print("Search Path:", template_path)

    app.run(debug=True, port=5005)
