from flask import Blueprint, jsonify # Import current_app
from models import GameState


from controllers.gametime import update_rate, reset_rate



gametime_bp = Blueprint('gametime', __name__, url_prefix='/gametime')

@gametime_bp.route('/get_time_info')
def get_time_info():
    gamestate = GameState.query.first() 

    if gamestate:
        return jsonify({
            'game_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'time_rate': gamestate.time_rate
        })
    else:
        return jsonify({'error': 'Game state not found'}), 404


@gametime_bp.route('/update_rate', methods=['POST'])
def update_rate_route():
    return update_rate()


@gametime_bp.route('/reset_rate', methods=['POST'])
def reset_rate_route():
    return reset_rate()


