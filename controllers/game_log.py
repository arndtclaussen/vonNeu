from models import db, GameLog

def add_log_entry(message):
    try:
        log_entry = GameLog(message=message)
        db.session.add(log_entry)
        db.session.commit()
        print(f"Log entry added: {message}")
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