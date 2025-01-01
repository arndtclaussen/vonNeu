# controllers/gamestate.py
from flask import jsonify
from models import GameState, db
from datetime import timedelta


def advance_time():
    gamestate = GameState.query.first()
    if gamestate:
        gamestate.game_time += timedelta(seconds=5)
        db.session.commit()
        return jsonify({'new_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S UTC')}), 200 # Explicit 200 OK status
    else:
        return jsonify({'error': 'Game state not found'}), 404