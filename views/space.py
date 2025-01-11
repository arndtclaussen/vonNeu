from flask import Blueprint, render_template

space_bp = Blueprint('space', __name__, url_prefix='/space', template_folder='../templates/space')

@space_bp.route('/') 
def asteroids():
    return render_template('space/asteroids.html')


@space_bp.route('/object') # Route is /gamestate/action
def objects():
    return render_template('space/objects.html')

