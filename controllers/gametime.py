# controllers/gametime.py
from flask import jsonify, request
from models import GameState, db
from controllers.game_log import add_log_entry 


def update_rate():
    try:
        change = int(request.json.get('change', 0))  # Get change from request body. Default to 0.
        gamestate = GameState.query.first()

        if gamestate:
            new_rate = max(0, gamestate.time_rate + change) # Ensure the rate isn't negative
            if new_rate != gamestate.time_rate: # Only update if there's a change
              gamestate.time_rate = new_rate
              db.session.commit()
              add_log_entry(f"Time rate changed to {new_rate}x") # Add log entry
              print(f"New time rate: {gamestate.time_rate}")  # Keep for debugging
            return jsonify({'new_rate': gamestate.time_rate}), 200 
        else:
            return jsonify({'error': 'Game state not found'}), 404
    except Exception as e:
        db.session.rollback()
        print("Error updating rate:", e)
        return jsonify({'error': str(e)}), 500

def reset_rate():
 
    try:
        gamestate = GameState.query.first()
        if gamestate:
            gamestate.time_rate = 1.0  
            db.session.commit()
            return jsonify({'new_rate': gamestate.time_rate}), 200
        else:
            return jsonify({'error': 'Game state not found'}), 404
    except Exception as e:
        db.session.rollback()
        print("Error resetting rate:", e)
        return jsonify({'error': str(e)}), 500