from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

# Import your models (to be defined below)
from .probe import Probe
from .asteroid import Asteroid
from .gamestate import GameState


