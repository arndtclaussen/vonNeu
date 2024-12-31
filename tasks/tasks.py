import redis
from rq import Queue
from datetime import datetime, timedelta, timezone


#REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')  # Or from environment variables
REDIS_HOST = "localhost"  # For local testing 
redis_connection = redis.Redis(host=REDIS_HOST, port=6379, db=0)
queue = Queue(connection=redis_connection)  # No need to recreate the queue each time


def update_game_state(current_time):
    # with app.app_context():  # IMPORTANT: Add app context for db access if needed
    print(f"Updating game state at {current_time}")

    # Your game logic here (e.g., update asteroid positions, check probe status, etc.)
    # ...

    now = datetime.now(timezone.utc)


    # Schedule the *next* run
    next_run_time = now + timedelta(seconds=5)  # Use 'now' for the next run
    queue.enqueue_in(timedelta(seconds=5), update_game_state, next_run_time)  # Enqueue from here
    print(f"Next update scheduled for {next_run_time}")


def initialize_game_state(): # Initial kick-off function for the task
    current_time = datetime.now(timezone.utc)
    queue.enqueue(update_game_state, current_time)






