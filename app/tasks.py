
'''
def hello_world_rq(my_variable):
    from sqlalchemy import create_engine, inspect
    from sqlalchemy.orm import sessionmaker
    from config import Config  # Import your config

    print(f"Hello {my_variable} from the worker!")

    # Database connection within the task:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        inspector = inspect(engine) # Create an inspector
        tables = inspector.get_table_names() # Get table names
        print(f"Existing tables: {tables}")


    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()

    return "Hello World from RQ Worker"

'''