from . import db

class Asteroid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.BigInteger)  # Use BigInteger for large numbers
    delta_v = db.Column(db.Integer)

    def __repr__(self):
        return f"<Asteroid {self.id}: Size={self.size} kg>"
