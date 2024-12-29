from flask import Blueprint, render_template
from models import Probe  # Import the Probe model


asteroids_bp = Blueprint('asteroids', __name__, url_prefix='/asteroids', template_folder='../templates/asteroids')  


@asteroids_bp.route('/')
def index():
    # Placeholder: Using Probe data temporarily
    probes = Probe.query.all() # Keep this temporarily
    return render_template('index.html', probes=probes) # Keep this temporarily

@asteroids_bp.route('/<int:asteroid_id>') # Use asteroid_id here
def details(asteroid_id):  # Use asteroid_id here
    # Placeholder: Using Probe data temporarily
    probe = Probe.query.get_or_404(asteroid_id)  # Use asteroid_id for now, but we'll query Asteroid later
    all_probes = Probe.query.all()  # Query all probes for the sidebar (temporary)
    return render_template('details.html', probe=probe, all_probes=all_probes)  # Keep probe and all_probes for now