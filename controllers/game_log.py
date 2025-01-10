from models import db, GameLog, GameState

def add_log_entry(message):
    try:
        gamestate = GameState.query.first()
        if gamestate:
            log_entry = GameLog(message=message, timestamp=gamestate.game_time)  # Set timestamp here
            db.session.add(log_entry)
            db.session.commit()
            print(f"Log entry added: {message} at {gamestate.game_time}") # Log includes gametime
        else:
            print("Error: GameState not found. Log entry not created.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding log entry: {e}")

# controllers/game_log.py
def get_last_10_logs():
    try:
        logs = GameLog.query.order_by(GameLog.timestamp.desc()).limit(10).all()
        return logs
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return [] # Return an empty list on error