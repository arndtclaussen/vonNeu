from flask import Blueprint, render_template, jsonify
from models import Asteroid

space_bp = Blueprint('space', __name__, url_prefix='/space', template_folder='../templates/space')

@space_bp.route('/') 
def asteroids():
    return render_template('space/asteroids.html')


@space_bp.route('/object') 
def objects():
    return render_template('space/objects.html')

@space_bp.route('/get_asteroids')
def get_asteroids():
    asteroids = Asteroid.query.all()
    return jsonify([asteroid.to_dict() for asteroid in asteroids])
