from . import db
from datetime import datetime, timezone


class GameState(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    game_time = db.Column(db.DateTime, nullable=False, default=datetime(2325, 12, 31, 14, 4, 5, tzinfo=timezone.utc))
    time_rate = db.Column(db.Float, nullable=False, default=10.0)

# ... other parts of your models/__init__.py and models/ files ...