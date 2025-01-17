from flask import Blueprint, jsonify # Import current_app
from models import GameState

from controllers.gamelog import get_last_10_logs, add_log_entry # Import add_log_entry



gamelog_bp = Blueprint('gamelog', __name__, url_prefix='/gamelog')


@gamelog_bp.route('/get_logs')
def get_logs():
    logs = get_last_10_logs()
    # Convert log objects to dictionaries for JSON serialization
    log_list = [{'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'), 'message': log.message} for log in logs]
    return jsonify(log_list)