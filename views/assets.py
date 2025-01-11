from flask import Blueprint, render_template


assets_bp = Blueprint('assets', __name__, url_prefix='/assets', template_folder='../templates/assets')

@assets_bp.route('/') 
def probes():
    return render_template('assets/probes.html')

@assets_bp.route('/miners') 
def miners():
    return render_template('assets/miners.html')

@assets_bp.route('/tugs') 
def tugs():
    return render_template('assets/tugs.html')
