import redis
import os
from dotenv import load_dotenv

load_dotenv()

def test_redis_connection():
    """Tests the connection to the Redis server and cleans up after itself."""
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        try:
            redis_port = int(os.getenv("REDIS_PORT", 6379))
        except ValueError:
            print("Error: REDIS_PORT environment variable must be an integer.")
            return False  # Indicate failure

        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        try:
            r.ping()
            print("Successfully connected to Redis!")

            test_key = "test_key" # Use a variable for easier cleanup
            r.set(test_key, "test_value")
            value = r.get(test_key)
            print(f"Retrieved value: {value}")

            r.delete(test_key)  # Clean up the test key
            print("Cleaned up test key.")

        except redis.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return False
        except redis.exceptions.TimeoutError as e:
            print(f"Timeout Error: {e}")
            return False
        # Add other Redis exception handlers as needed...
        except Exception as e: # For any other errors during the test
            print(f"An error occurred during the test: {e}")
            return False


    except Exception as e:  # Catch any unexpected errors during connection setup
        print(f"An unexpected error occurred: {e}")
        return False

    return True # Indicate success


if __name__ == "__main__":
    if test_redis_connection():
        print("Redis connection test passed.")
    else:
        print("Redis connection test failed.")
