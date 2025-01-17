from flask import Blueprint, render_template, jsonify

from models import Asteroid, GameState


from controllers.gamelog import get_last_n_logs # Import add_log_entry


space_bp = Blueprint('space', __name__, url_prefix='/space', template_folder='../templates/space')


## Asteroids
@space_bp.route('/') 
def asteroids():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('space/asteroids.html', gamestate=gamestate, logs=logs)

@space_bp.route('/get_asteroids')
def get_asteroids():
    asteroids = Asteroid.query.all()
    return jsonify([asteroid.to_dict() for asteroid in asteroids])


## Objects
@space_bp.route('/object') 
def objects():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('space/objects.html', gamestate=gamestate, logs=logs)


