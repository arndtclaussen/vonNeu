from . import db

class Asteroid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Example: "Asteroid X42"
    composition = db.Column(db.String(50))       # Example: "Iron-rich"
    size = db.Column(db.Integer)                # Example: 125 (diameter in km)
    discovered_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Asteroid {self.id}: {self.name}>"