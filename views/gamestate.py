from flask import Blueprint, render_template, jsonify, current_app # Import current_app

from models import GameState, db
from datetime import timedelta


from controllers.gamestate import advance_time, hello_world



gamestate_bp = Blueprint('gamestate', __name__, url_prefix='/gamestate', template_folder='../templates/gamestate')

@gamestate_bp.route('/') # Route for overview is now /gamestate/
def overview():
    gamestate = GameState.query.first()
    return render_template('gamestate/overview.html', gamestate=gamestate)


@gamestate_bp.route('/action') # Route is /gamestate/action
def action():
    return render_template('gamestate/action.html')



@gamestate_bp.route('/advance_time', methods=['POST'])
def advance_time_route():  # Rename the route handler
    return advance_time()  # Call the controller function



@gamestate_bp.route('/schedule_hello', methods=['POST'])
def schedule_hello():
    try:
        q = current_app.config['RQ_QUEUE'] # Access the app's queue
        job = q.enqueue_in(timedelta(seconds=10), hello_world)
        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500




'''
@gamestate_bp.route('/advance_time', methods=['POST'])
def advance_time():
    gamestate = GameState.query.first()
    if gamestate:
        gamestate.game_time += timedelta(seconds=5)  # Add 5 seconds
        db.session.commit()
        return jsonify({'new_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S UTC')})
    else:
        return jsonify({'error': 'Game state not found'}), 404  # Return 404 if not found
'''