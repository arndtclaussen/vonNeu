# controllers/gamestate.py
from flask import jsonify
from datetime import timedelta




def advance_time():
    from models import GameState, db, Asteroid

    gamestate = GameState.query.first()
    if gamestate:
       
        # Figure out time
        time_elapsed = timedelta(seconds=5)  # Get the time step
        time_elapsed_seconds = time_elapsed.total_seconds() 
        
        # Store in db
        gamestate.game_time += time_elapsed
       
        # Move Asteroids
        Asteroid.update_positions(time_elapsed_seconds=time_elapsed_seconds)  # Call from Asteroid

        
        db.session.commit()
        return jsonify({'new_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S UTC')}), 200 # Explicit 200 OK status
    else:
        return jsonify({'error': 'Game state not found'}), 404
    
def hello_world(passed_variable):
    print(f"Hello, World! {passed_variable}")
    print("hi")


def update_rate():
    from flask import jsonify, request
    from models import GameState, db
    from controllers.game_log import add_log_entry # Import add_log_entry


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
    from flask import jsonify, request
    from models import GameState, db
    
    try:
        gamestate = GameState.query.first()
        if gamestate:
            gamestate.time_rate = 1.0  # Reset to 1
            db.session.commit()
            return jsonify({'new_rate': gamestate.time_rate}), 200
        else:
            return jsonify({'error': 'Game state not found'}), 404
    except Exception as e:
        db.session.rollback()
        print("Error resetting rate:", e)
        return jsonify({'error': str(e)}), 500