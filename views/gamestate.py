import rq  # Make sure to import rq
from flask import Blueprint, jsonify, current_app # Import current_app

from datetime import timedelta

from tasks.gamestate import update_game_state
from config import Config  # Import your config


from rq.registry import (
    FailedJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
)

from controllers.gamelog import add_log_entry # Import add_log_entry

from models import db, GameState

gamestate_bp = Blueprint('gamestate', __name__, url_prefix='/gamestate', template_folder='../templates/gamestate')




@gamestate_bp.route('/start_game_cyclce', methods=['POST'])
def start_game_cyclce():
     
    #Check if game is already running
    gamestate = GameState.query.first()
    if gamestate.is_running:
        return jsonify({'error': 'Game is already running'}), 400  # Bad Request

    gamestate.is_running = True
    db.session.commit()

    #Only if running procced
    try:
        q = current_app.config['RQ_QUEUE']  

        #redis_conn = current_app.config.get('RQ_REDIS_CONN')      
        job = q.enqueue_in(timedelta(seconds=Config.REDIS_TIME_SCHEDULE), update_game_state) # No need to pass current_app yet
        add_log_entry(f"In Game Started") # Add log entry

        return jsonify({'message': f'Hello scheduled! Job ID: {job.id}'})
    except Exception as e:
        print(f"Error scheduling hello: {e}")
        return jsonify({'error': 'Failed to schedule hello'}), 500

        


        
@gamestate_bp.route('/clear_redis', methods=['POST'])
def clear_redis_route():
    gamestate = GameState.query.first()
    gamestate.is_running = False
    db.session.commit()
    
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
        add_log_entry(f"In Game Stopped") # Add log entry
    
            
            

        return jsonify({'message': 'All queues and registries cleared', 'queues': queue_names}), 200

    except Exception as e:
        print(f"Error clearing queues: {e}")
        return jsonify({'error': 'Failed to clear queues'}), 500

