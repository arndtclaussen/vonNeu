from . import db

class Probe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    build_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    fuel = db.Column(db.Integer)  # Add this line!

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'build_time': self.build_time,
            'status': self.status,
            'fuel': self.fuel
        }

    def __repr__(self):
        return f"&lt;Probe {self.id}: {self.type}>" 