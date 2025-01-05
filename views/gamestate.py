from flask import Blueprint, render_template, jsonify, current_app # Import current_app

from models import GameState, db
from datetime import timedelta


from controllers.gamestate import advance_time, hello_world

import rq  # Make sure to import rq


from rq.registry import (
    FailedJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
)

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


'''
@gamestate_bp.route('/schedule_hello', methods=['POST'])
def schedule_hello():
    try:
        q = current_app.config['RQ_QUEUE'] # Access the app's queue
        print(f"Config value: {current_app.get('SECRET_KEY')}") # Access config
      
        job = q.enqueue_in(timedelta(seconds=10), hello_world)
        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500
'''

''' 2 Versuch
@gamestate_bp.route('/schedule_hello', methods=['POST'])
def schedule_hello():
    try:
        q = current_app.config['RQ_QUEUE']
        with current_app.app_context(): # Keep this, create the context
            print(f"Config value: {current_app.config.get('SECRET_KEY')}") # Access config HERE (inside context)
            job = q.enqueue_in(timedelta(seconds=10), hello_world) # Pass current_app to the worker
        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})  # This is outside the context, but that's OK for this return
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500
'''

@gamestate_bp.route('/schedule_hello', methods=['POST'])
def schedule_hello():
    from 
    try:
        my_variable = "this is my variable"
        q = current_app.config['RQ_QUEUE']  # Accessing current_app here is OK
        print(current_app.config.get('SECRET_KEY')) # To verify app context
        job = q.enqueue_in(timedelta(seconds=10), hello_world, my_variable) # No need to pass current_app yet

        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500

        


        
@gamestate_bp.route('/clear_redis', methods=['POST'])
def clear_redis_route():
    try:
        redis_conn = current_app.config['RQ_CONNECTION']
        queues = rq.Queue.all(connection=redis_conn)
        queue_names = [q.name for q in queues]

        for queue in queues:
            queue.empty()
            failed_registry = FailedJobRegistry(queue=queue, connection=redis_conn)
            
            # This is how to remove a job from a registry
            for job_id in failed_registry.get_job_ids():
                failed_registry.remove(job_id)


            finished_registry = FinishedJobRegistry(queue=queue, connection=redis_conn)
            # This is how to remove a job from a registry
            for job_id in finished_registry.get_job_ids():
                finished_registry.remove(job_id)
            
            scheduled_registry = ScheduledJobRegistry(queue=queue, connection=redis_conn)
            # This is how to remove a job from a registry
            for job_id in scheduled_registry.get_job_ids():
                scheduled_registry.remove(job_id)
            
            
            

        return jsonify({'message': 'All queues and registries cleared', 'queues': queue_names}), 200

    except Exception as e:
        print(f"Error clearing queues: {e}")
        return jsonify({'error': 'Failed to clear queues'}), 500



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