from flask import Blueprint, render_template

from models import Asteroid # Import Asteroid Model

asteroids_bp = Blueprint('asteroids', __name__, url_prefix='/asteroids', template_folder='../templates/asteroids')

@asteroids_bp.route('/')
def index():
     asteroids = Asteroid.query.all()
     return render_template('index.html', asteroids=asteroids) #pass asteroids to template

# ... (other asteroid routes)
