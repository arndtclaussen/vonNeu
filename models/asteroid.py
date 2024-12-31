from . import db

class Asteroid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Example: "Asteroid X42"
    composition = db.Column(db.String(50))       # Example: "Iron-rich"
    size = db.Column(db.Integer)                # Example: 125 (diameter in km)
    discovered_at = db.Column(db.DateTime)
    x_coordinate = db.Column(db.Float)           # X-coordinate in 2D plane
    y_coordinate = db.Column(db.Float)           # Y-coordinate in 2D plane
    delta_v_x = db.Column(db.Float)           # delta v of x
    delta_v_y = db.Column(db.Float)           # delta v of y



    def to_dict(self):  # Add this
        return {
            'id': self.id,
            'name': self.name,
            'composition': self.composition,
            'size': self.size,
            'discovered_at': self.discovered_at,
            'x_coordinate': self.x_coordinate,
            'y_coordinate': self.y_coordinate,
            'delta_v_x': self.delta_v_x,
            'delta_v_y': self.delta_v_y,
        }


    def __repr__(self):
        return f"<Asteroid {self.id}: {self.name}>"