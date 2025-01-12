import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")  # Set a proper secret key for production
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}/{os.environ.get('POSTGRES_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Improves Performance

    RQ_DASHBOARD_REDIS_URL = "redis://localhost:6379/0"
    REDIS_URL = "redis://localhost:6379/0"
    
    REDIS_HOST_4_SCHEDULE = "127.0.0.1"
    REDIS_PORT_4_SCHEDULE = "6379"
    REDIS_TIME_SCHEDULE = 1

    