from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
import random

db = SQLAlchemy()


# Import your models (to be defined below)
from .probe import Probe
from .asteroid import Asteroid
from .gamestate import GameState
from .game_log import GameLog


def init_db(app):
    with app.app_context():
        #db.drop_all()  # Remove this unless you REALLY want to reset every time
        db.create_all()

        # Ensure only one GameState row exists
        if GameState.query.count() == 0:
            initial_game_state = GameState() # Uses default datetime and time_rate
            db.session.add(initial_game_state)
            db.session.commit()


        # Check if probes already exist to prevent duplicate initial data
        if Probe.query.count() == 0:
            probes_data = [
                {"type": "Mk1", "status": "Docked", "fuel": 100},
                {"type": "Mk2", "status": "Exploring", "fuel": 65},
                {"type": "Mk1", "status": "Exploring", "fuel": 12},
                {"type": "Mk3", "status": "Maintenance", "fuel": 88},
                {"type": "Mk2", "status": "In Transit", "fuel": None},
                {"type": "Mk1", "status": "Docked", "fuel": 5},
                {"type": "Mk4", "status": "Construction", "fuel": 23},
            ]

            for data in probes_data:
                probe = Probe(**data)  # More concise way to create the object
                db.session.add(probe)

            db.session.commit()


        # Adding example Asteroids with more data and using the same logic as for Probes:
        if Asteroid.query.count() == 0:
            now = datetime.now(timezone.utc)
            asteroids_data = [
                {"name": "Asteroid Alpha", "composition": "Iron-rich", "size": 250, "discovered_at": now - timedelta(days=50)},
                {"name": "Asteroid Beta", "composition": "Silicate", "size": 55, "discovered_at": now - timedelta(days=15)},
                {"name": "Asteroid Gamma", "composition": "Carbon-rich", "size": 1500, "discovered_at": now - timedelta(days=365*2)},
                {"name": "Asteroid Delta", "composition": "Nickel-Iron", "size": 100, "discovered_at": now - timedelta(days=10)},
                {"name": "Asteroid Epsilon", "composition": "Stony", "size": 75, "discovered_at": None}, # Unknown discovery date
            ]
            for data in asteroids_data:
                # Generate random coordinates and delta-v values
                data["x_coordinate"] = random.uniform(-1000, 1000)  # Example range
                data["y_coordinate"] = random.uniform(-1000, 1000)
                data["delta_v_x"] = random.uniform(-10, 10)      # Example delta-v range
                data["delta_v_y"] = random.uniform(-10, 10)

                asteroid = Asteroid(**data)
                db.session.add(asteroid)

        # Adding example Game Logs:
        if GameLog.query.count() == 0:
            now = datetime.now(timezone.utc)
            game_logs_data = [
                {"timestamp": now - timedelta(minutes=5), "message": "Probe Mk1 launched from Earth."},
                {"timestamp": now - timedelta(minutes=2), "message": "Asteroid Alpha detected near Mars."},
                {"timestamp": now, "message": "Probe Mk2 low on fuel."},  # Current time log
            ]
            for data in game_logs_data:
                log_entry = GameLog(**data)
                db.session.add(log_entry)
        
        db.session.commit()