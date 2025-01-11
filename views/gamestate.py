
import rq  # Make sure to import rq

from flask import Blueprint, render_template, jsonify, current_app # Import current_app

from models import GameState
from datetime import timedelta


from tasks.gamestate import update_game_state

from config import Config  # Import your config


from rq.registry import (
    FailedJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
)

from controllers.game_log import get_last_10_logs, add_log_entry # Import add_log_entry


gamestate_bp = Blueprint('gamestate', __name__, url_prefix='/gamestate', template_folder='../templates/gamestate')

@gamestate_bp.route('/') # Route for overview is now /gamestate/
def overview():
    gamestate = GameState.query.first()
    return render_template('gamestate/overview.html', gamestate=gamestate)


@gamestate_bp.route('/action') # Route is /gamestate/action
def action():
    return render_template('gamestate/action.html')


@gamestate_bp.route('/start_game_cyclce', methods=['POST'])
def start_game_cyclce():
     
    try:
        q = current_app.config['RQ_QUEUE']  
        job = q.enqueue_in(timedelta(seconds=Config.REDIS_TIME_SCHEDULE), update_game_state) # No need to pass current_app yet
        add_log_entry(f"In Game Started") # Add log entry

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
        add_log_entry(f"In Game Stopped") # Add log entry
    
            
            

        return jsonify({'message': 'All queues and registries cleared', 'queues': queue_names}), 200

    except Exception as e:
        print(f"Error clearing queues: {e}")
        return jsonify({'error': 'Failed to clear queues'}), 500



@gamestate_bp.route('/get_logs')
def get_logs():
    logs = get_last_10_logs()
    # Convert log objects to dictionaries for JSON serialization
    log_list = [{'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'), 'message': log.message} for log in logs]
    return jsonify(log_list)