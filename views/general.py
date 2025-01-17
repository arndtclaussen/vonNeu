# views/general.py
from flask import Blueprint, redirect, url_for

general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def index():
    return redirect(url_for('assets.probes'))