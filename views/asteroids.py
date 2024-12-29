from flask import Blueprint, render_template, request, current_app
from models import Asteroid  # Import Asteroid model

asteroids_bp = Blueprint('asteroids', __name__, url_prefix='/asteroids', template_folder='../templates/asteroids')

@asteroids_bp.route('/')
def index():
    #print(request.path)  # or print(request) for ALL request info
    #print("Asteroids index route called")
    #print(current_app.jinja_loader.list_templates()) 
    asteroids = Asteroid.query.all()
    #print(asteroids)  # Print the result of the query
    return render_template('asteroids/index.html', asteroids=asteroids)

@asteroids_bp.route('/<int:asteroid_id>')
def details(asteroid_id):
    asteroid = Asteroid.query.get_or_404(asteroid_id)
    all_asteroids = Asteroid.query.all()
    return render_template('asteroids/details.html', asteroid=asteroid, all_asteroids=all_asteroids)

@asteroids_bp.route('/test')
def test():
    return "Hello from Asteroids!"

@asteroids_bp.route('/test_isolated')
def test_isolated():
    asteroids = Asteroid.query.all()
    return render_template('test_isolated.html', asteroids=asteroids)