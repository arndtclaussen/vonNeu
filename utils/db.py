# utils/db.py
from models import db  # Import the db instance from models/__init__.py


def init_db(app): # app needs to be passed 
    with app.app_context():
        db.drop_all()   # In development/testing ONLY.  Use db.create_all() for production
        db.create_all()

        # Example of adding initial data (optional):
        from models.probe import Probe  # Import within function to avoid circular imports
        probe1 = Probe(type="Mk1", status="Docked")
        db.session.add(probe1)
        db.session.commit()