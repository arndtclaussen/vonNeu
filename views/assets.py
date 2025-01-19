from flask import Blueprint, render_template


from models import GameState


from controllers.gamelog import get_last_n_logs # Import add_log_entry



assets_bp = Blueprint('assets', __name__, url_prefix='/assets', template_folder='../templates/assets')


@assets_bp.route('/heaven') 
def heaven():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('assets/heaven.html',gamestate=gamestate, logs=logs)


@assets_bp.route('/probes') 
def probes():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('assets/probes.html',gamestate=gamestate, logs=logs)

@assets_bp.route('/miners') 
def miners():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('assets/miners.html',gamestate=gamestate, logs=logs)

@assets_bp.route('/tugs') 
def tugs():
    gamestate = GameState.query.first()
    logs = get_last_n_logs()
    return render_template('assets/tugs.html',gamestate=gamestate, logs=logs)

