from models import db, GameLog, GameState

from flask_socketio import SocketIO
import os


from config import Config  # Import your config



sio = SocketIO(message_queue=os.getenv('REDIS_URL'))  # Recreate socketio


def get_last_n_logs():
    try:
        logs = GameLog.query.order_by(GameLog.timestamp.desc()).limit(Config.GAME_LAST_N_LOGS).all()
        return logs
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return [] # Return an empty list on error
    

def add_log_entry(message):
    try:
        gamestate = GameState.query.first()
        if gamestate:
            log_entry = GameLog(message=message, timestamp=gamestate.game_time)  
            db.session.add(log_entry)
            db.session.commit()

            sio.emit('game_log_update', {
                'timestamp': log_entry.timestamp.isoformat(),  # ISO 8601 format for timestamps
                'message': log_entry.message}, namespace='/')  

        else:
            print("Error: GameState not found. Log entry not created.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding log entry: {e}")
