from .extensions import db
from datetime import datetime

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_time = db.Column(db.DateTime, nullable=False, default=datetime(2325, 12, 31, 14, 4, 5))
