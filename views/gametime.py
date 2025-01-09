

import rq  # Make sure to import rq

from flask import Blueprint, render_template, jsonify, current_app # Import current_app

from models import GameState
from datetime import timedelta



gametime_bp = Blueprint('gametime', __name__, url_prefix='/gametime')

@gametime_bp.route('/get_time_info')
def get_time_info():
    gamestate = GameState.query.first()  # Assuming you have a GameState model

    if gamestate:
        return jsonify({
            'game_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'time_rate': gamestate.time_rate
        })
    else:
        return jsonify({'error': 'Game state not found'}), 404
