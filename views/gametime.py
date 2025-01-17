from flask import Blueprint

from controllers.gametime import get_rate, update_rate, reset_rate


gametime_bp = Blueprint('gametime', __name__, url_prefix='/gametime')

@gametime_bp.route('/get_time_info')
def get_time_info():
    return get_rate()


@gametime_bp.route('/update_rate', methods=['POST'])
def update_rate_route():
    return update_rate()


@gametime_bp.route('/reset_rate', methods=['POST'])
def reset_rate_route():
    return reset_rate()


