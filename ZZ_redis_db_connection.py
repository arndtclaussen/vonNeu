import redis
import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_redis_connection():
    """Tests the connection to the Redis server, including time synchronization, and cleans up after itself."""
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        try:
            redis_port = int(os.getenv("REDIS_PORT", 6379))
        except ValueError:
            print("Error: REDIS_PORT environment variable must be an integer.")
            return False

        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        try:
            r.ping()
            print("Successfully connected to Redis!")

            # Time Synchronization Check
            try:
                server_time = r.time()
                local_time = time.time()
                time_diff = abs(server_time[0] - local_time)

                print(f"Redis Server Time: {server_time[0]}")
                print(f"Local System Time: {local_time}")
                print(f"Time Difference: {time_diff} seconds")

                if time_diff > 60:
                    print("WARNING: Large time difference detected. Check NTP settings.")

            except redis.exceptions.ResponseError as e:  # Handle potential errors with the TIME command
                print(f"Error getting Redis server time: {e}")


            test_key = "test_key"
            r.set(test_key, "test_value")
            value = r.get(test_key)
            print(f"Retrieved value: {value}")

            r.delete(test_key)
            print("Cleaned up test key.")

        except redis.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return False
        except redis.exceptions.TimeoutError as e:
            print(f"Timeout Error: {e}")
            return False
        except Exception as e:  # Catch any other errors related to Redis commands
            print(f"An error occurred during Redis operations: {e}")
            return False

    except Exception as e:
        print(f"An unexpected error occurred during connection setup: {e}")
        return False

    return True



if __name__ == "__main__":
    if test_redis_connection():
        print("Redis connection test passed.")
    else:
        print("Redis connection test failed.")
