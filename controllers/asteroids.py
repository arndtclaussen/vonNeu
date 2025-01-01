# controllers/asteroids.py
from models import db, Asteroid



def update_asteroid_positions(time_elapsed_seconds):  # Now in asteroids.py
    try:

        asteroids = Asteroid.query.all()
        for asteroid in asteroids:
            asteroid.x_coordinate += asteroid.delta_v_x * time_elapsed_seconds
            asteroid.y_coordinate += asteroid.delta_v_y * time_elapsed_seconds

        pass
    except Exception as e:
        print(f"An error occurred: {e}")
