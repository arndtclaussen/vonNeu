from . import db  # Import your SQLAlchemy instance
from datetime import datetime, timezone

class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc)) # Use UTC
    message = db.Column(db.String(255), nullable=False)  # Adjust length as needed

    def __repr__(self):
        return f"<GameLog {self.id}: {self.message} at {self.timestamp}>"