# utils/db.py
from models import db, Probe, Asteroid

def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()  # Remove db.drop_all() unless you REALLY want to reset the db every time

        # Check if probes already exist to prevent duplicate initial data
        if Probe.query.count() == 0:  # Only add if the table is empty
            probes_data = [
                {"type": "Mk1", "status": "Docked", "fuel": 100},
                {"type": "Mk2", "status": "Exploring", "fuel": 65},
                {"type": "Mk1", "status": "Exploring", "fuel": 12},
                {"type": "Mk3", "status": "Maintenance", "fuel": 88},  # Added more variety
                {"type": "Mk2", "status": "In Transit", "fuel": None}, # None represents unknown fuelness
                {"type": "Mk1", "status": "Docked", "fuel": 5},       # Low fuelness example
                {"type": "Mk4", "status": "Construction", "fuel": 23}, # Different Status
            ]

            for data in probes_data:
                probe = Probe(type=data['type'], status=data['status'], fuel=data['fuel'])
                db.session.add(probe)

            db.session.commit()

        if Asteroid.query.count() == 0:
            asteroids_data = [
                {"size": 123456789012345, "delta_v": 3000},  # Example with BigInteger
                {"size": 9876543210987, "delta_v": 1500}
            ]
            for data in asteroids_data:
                asteroid = Asteroid(size=data['size'], delta_v=data['delta_v'])
                db.session.add(asteroid)
            db.session.commit()


