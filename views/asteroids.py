# views/asteroids.py
from flask import Blueprint, render_template
from models import Asteroid

asteroids_bp = Blueprint('asteroids', __name__, url_prefix='/asteroids', template_folder='../templates/asteroids')

@asteroids_bp.route('/')
def index():
    asteroids = Asteroid.query.all()
    return render_template('index.html', asteroids=asteroids)

@asteroids_bp.route('/<int:asteroid_id>')

def details(asteroid_id):
    asteroid = Asteroid.query.get_or_404(asteroid_id)
    all_asteroids = Asteroid.query.all() # This line was missing or not working
    return render_template('details.html', asteroid=asteroid, all_asteroids=all_asteroids)
		