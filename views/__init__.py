from flask import Blueprint

# Import the blueprints (to be defined below)
from .gamestate import gamestate_bp
from .probes import probes_bp
from .gametime import gametime_bp

from .general import general_bp # Import the routes module

from .space import space_bp # Import the routes module
