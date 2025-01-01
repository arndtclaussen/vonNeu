from flask import Blueprint, render_template
from models import Asteroid  # Import Asteroid model

asteroids_bp = Blueprint('asteroids', __name__, url_prefix='/asteroids', template_folder='../templates/asteroids')

@asteroids_bp.route('/')
def index():
    asteroids = Asteroid.query.all()
    #print(asteroids)  # Print the result of the query
    return render_template('asteroids/index.html', asteroids=asteroids)

@asteroids_bp.route('/<int:asteroid_id>')
def details(asteroid_id):
    asteroid = Asteroid.query.get_or_404(asteroid_id)
    all_asteroids = Asteroid.query.all()
    return render_template('asteroids/details.html', asteroid=asteroid, all_asteroids=all_asteroids)
