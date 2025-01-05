from app import create_app  # Import your app factory
from app.extensions import db
from sqlalchemy import inspect

def hello_world_rq(my_variable):
    # Create the app instance and push the app context
    app = create_app()
    with app.app_context():
        try:
            # Use the db session provided by Flask-SQLAlchemy
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Existing tables: {tables}")
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}")
        finally:
            db.session.close()

    return f"Hello {my_variable} from the worker!"


