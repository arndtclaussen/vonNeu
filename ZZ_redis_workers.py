import redis
from rq import Worker

import os
from dotenv import load_dotenv



load_dotenv()


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))


redis_conn = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

worker = Worker.all(connection=redis_conn)[0] # Get the first available worker

print(f"Worker name: {worker.name}")
print(f"Worker state: {worker.get_state()}") # 'idle', 'busy', 'suspended', etc.
print(f"Worker queues: {worker.queues}") # List of queues the worker is listening to

# Check if the worker is currently working on any jobs:
if worker.get_current_job():
   print("Worker is currently processing a job.")
		
