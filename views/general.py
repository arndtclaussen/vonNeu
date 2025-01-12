# views/general.py
from flask import Blueprint, redirect, url_for
from models import GameState # Import GameState

general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def index():
    gamestate = GameState.query.first() # Fetch GameState here, and pass it
    if gamestate:
        return redirect(url_for('assets.probes'))