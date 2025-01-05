import os
import redis
import time
from datetime import timedelta, datetime

from flask import Flask, render_template, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from rq import Queue
from rq_scheduler import Scheduler

from rq import Queue, get_current_job  # Import get_current_job if using inside job function


import rq_dashboard 

# Configuration and Models (Keeping config.py)
from config import Config # Your existing config.py

# Load environment variables (if using .env)
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)  # Use your Config class
db = SQLAlchemy(app)

# RQ Dashboard setup *before* registering blueprints (if any in the future)
app.config.from_object(rq_dashboard.default_settings)
rq_dashboard.web.setup_rq_connection(app)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


# Redis connection and RQ queue

redis_conn = redis.from_url('redis://localhost:6379/0')
q = Queue(connection=redis_conn)
scheduler = Scheduler(connection=redis_conn) # Create a scheduler instance




class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_time = db.Column(db.DateTime, nullable=False, default=datetime(2325, 12, 31, 14, 4, 5))  # Using DateTime

with app.app_context():
    db.drop_all() # clears the db at startup - use with care!
    db.create_all()

    # Ensure only one GameState exists - good practice for single-row game state
    if not GameState.query.first():
        initial_game_state = GameState()
        db.session.add(initial_game_state)
        db.session.commit()



@app.route('/', methods=['GET', 'POST'])
def index():
    gamestate = GameState.query.first()
    
    if request.method == 'POST':
        try:
            gamestate.game_time += timedelta(seconds=5)
            db.session.commit()
            return jsonify({'message': 'Time advanced!', 'new_time': gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S')}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return render_template('index_mvp.html', game_time=gamestate.game_time.strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/schedule_advance')
def schedule_advance():
    try:
        my_variable = "this is my variable"
        out = hello_world(my_variable)
        return jsonify({'message': f'Hello scheduled! Job ID: {out}'})


        # Schedule using RQ-Scheduler
        #job = scheduler.enqueue_in(timedelta(seconds=10), hello_world, my_variable)
        #return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})

    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500


def hello_world(passed_variable):
    print(f"Hello, World! {passed_variable}") # This will print on the worker console.
    #job = get_current_job()  # Get information about the currently executing job
    return "Hello World Complete!" # Return value, if you need it (not used here).



def advance_time_rq():
    with app.app_context():
        gamestate = GameState.query.first()
        if gamestate:
            gamestate.game_time += timedelta(seconds=5)
            db.session.commit()
            print(f"Time advanced by RQ Worker to: {gamestate.game_time}")
            return True
        return False



if __name__ == '__main__':
    app.run(debug=True, port=5006)


