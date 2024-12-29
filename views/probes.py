from flask import Blueprint, render_template, request, current_app
from models import Probe  # Import the Probe model


probes_bp = Blueprint('probes', __name__, url_prefix='/probes', template_folder='../templates/probes')


@probes_bp.route('/')
def index():
    #print(request.path)  # or print(request) for ALL request info
    #print("Probes index route called")
    #print(current_app.jinja_loader.list_templates()) 
    probes = Probe.query.all()
    #print(probes)  # Print the result of the query
    return render_template('probes/index.html', probes=probes)

@probes_bp.route('/<int:probe_id>')

def details(probe_id):
    probe = Probe.query.get_or_404(probe_id)
    all_probes = Probe.query.all()  # Query all probes for the sidebar
    return render_template('probes/details.html', probe=probe, all_probes=all_probes) # Pass both probe and all_probes