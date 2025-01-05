from flask import Blueprint, render_template, jsonify, request, current_app
from datetime import timedelta

from app.models import GameState
from app.extensions import db  # Import db here


main = Blueprint('main', __name__)  # Blueprint name 'main'

@main.route('/', methods=['GET', 'POST'])
def index():
    gamestate = GameState.query.first()
    
    if request.method == 'POST':
        try:
            gamestate.game_time += timedelta(seconds=5)
            db.session.commit()
            return jsonify({'message': 'Time advanced!', 'new_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S')}), 200
        except Exception as e:
            db.session.rollback()  # Important to rollback on error
            return jsonify({'error': str(e)}), 500

    return render_template('index.html', game_time=gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S'))


@main.route('/schedule_advance')
def schedule_advance():
    try:

        from ..tasks import hello_world_rq
        my_variable = "Greetings from redis"
        q = current_app.config['RQ_QUEUE']  
        job = q.enqueue_in(timedelta(seconds=10), hello_world_rq, my_variable) # No need to pass current_app to Scheduler anymore
        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})
            
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500
