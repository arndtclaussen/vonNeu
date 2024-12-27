from flask import Blueprint, render_template
from models import Probe  # Import the Probe model

probes_bp = Blueprint('probes', __name__, template_folder='../templates/probes')

@probes_bp.route('/')
def list_probes():
    probes = Probe.query.all()
    return render_template('list.html', probes=probes)

@probes_bp.route('/<int:probe_id>')
def details(probe_id):
    probe = Probe.query.get_or_404(probe_id)
    all_probes = Probe.query.all()  # Query all probes for the sidebar
    return render_template('details.html', probe=probe, all_probes=all_probes) # Pass both probe and all_probes