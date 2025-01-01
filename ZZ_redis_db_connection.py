import redis
import os

from dotenv import load_dotenv
load_dotenv()


def test_redis_connection():
    """Tests the connection to the Redis server."""
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")  # Default to localhost if REDIS_HOST isn't set
        redis_port = int(os.getenv("REDIS_PORT", 6379))    # Default to 6379 if REDIS_PORT isn't set

        # If you're using Redis Stack and have set a password:
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True) # No password

        r.ping()  # Test basic connectivity
        print("Successfully connected to Redis!")

        # Optional: Further testing
        r.set("test_key", "test_value")
        value = r.get("test_key")
        print(f"Retrieved value: {value}")

    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




if __name__ == "__main__":
    test_redis_connection()
