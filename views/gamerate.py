from flask import Blueprint

from controllers.gamerate import get_rate, update_rate, reset_rate


gamerate_bp = Blueprint('gamerate', __name__, url_prefix='/gamerate')

@gamerate_bp.route('/get_time_info')
def get_time_info():
    return get_rate()


@gamerate_bp.route('/update_rate', methods=['POST'])
def update_rate_route():
    return update_rate()


@gamerate_bp.route('/reset_rate', methods=['POST'])
def reset_rate_route():
    return reset_rate()


