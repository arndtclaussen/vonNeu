
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config import Config  # Import your config


from rq import Queue
from redis import Redis
from datetime import timedelta


from models import db, GameState, Asteroid  # Import necessary models



redis_conn = Redis(host=Config.REDIS_HOST_4_SCHEDULE, port=Config.REDIS_PORT_4_SCHEDULE, decode_responses=True)
q = Queue(connection=redis_conn) # Declare it outside




def update_game_state():

    """Updates game state, including time and asteroid positions."""
    # Database connection within the task:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. Update Game Time
        gamestate = session.query(GameState).first() # use session
        if gamestate:
            
            # Figure out time
            time_elapsed = timedelta(seconds=gamestate.time_rate)  # Get the time step
            #time_elapsed_seconds = time_elapsed.total_seconds() 
            
            gamestate.game_time += time_elapsed
            session.commit() # Commit game time update first

            # 2. Update Asteroid Positions
            asteroids = session.query(Asteroid).all()  # Use session, not db
            for asteroid in asteroids:
                asteroid.x_coordinate += asteroid.delta_v_x * time_elapsed.total_seconds()
                asteroid.y_coordinate += asteroid.delta_v_y * time_elapsed.total_seconds()
                session.commit() # Commit game time update first
                
            #print(f"Game state updated at {gamestate.game_time}, rate: {gamestate.time_rate}")

        else:
            print("Error: GameState not found")

        # Reschedule the task (important for the loop)
        q.enqueue_in(timedelta(seconds=Config.REDIS_TIME_SCHEDULE), update_game_state)

    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()

    return "Hello World from RQ Worker"