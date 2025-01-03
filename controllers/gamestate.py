# controllers/gamestate.py
from flask import jsonify
from models import GameState, db, Asteroid
from datetime import timedelta




def advance_time():
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
    


def hello_world():
    print("hi")
    