
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config import Config  # Import your config


from rq import Queue
from redis import Redis
from datetime import timedelta

redis_conn = Redis(host="127.0.0.1", port="6379", decode_responses=True)
q = Queue(connection=redis_conn) # Declare it outside


def hello_world_rq(my_variable):
    print(f"Hello {my_variable} from the worker!")

    # Database connection within the task:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        inspector = inspect(engine) # Create an inspector
        tables = inspector.get_table_names() # Get table names
        print(f"Existing tables: {tables}")
        q.enqueue_in(timedelta(seconds=10), hello_world_rq, my_variable)

    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()

    return "Hello World from RQ Worker"
		