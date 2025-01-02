### How to do redis
# Start the docker: 
# docker run -d --name redis-vonneu -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
#
# Then, we need a module sourced from another file
# --> We are using ZZ_redis_module.py where we have a simple hello world definition
#
# Then we start the worker:
# rq worker --with-scheduler
#
# Then we run this script
# --> Here we test first the connection and then we FINALLY queue a task





### Load 
import os
from dotenv import load_dotenv


from ZZ_redis_module import hello_world

from redis import Redis
from rq import Queue

from datetime import datetime, timedelta

### Load Environment
load_dotenv()


### Test Connection to Docker Redis

redis_connect = Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    charset="utf-8",
    decode_responses=True
    )
connection = redis_connect.ping()

print(connection)

### Test 1: Queue a Simple Task
#q = Queue(connection=redis_connect)
#result=q.enqueue(hello_world)

### Test 2: Queue a simple task with a name
#q = Queue("foo", connection=redis_connect)
#result=q.enqueue(hello_world)
#--> This will not work with the default worker. If we use however:
#--> rq worker "foo" --with-scheduler
#it works


### Test 3: Run a Task in 5 seconds:
now = datetime.now()
print(f"Current time: {now}")

q = Queue(connection=redis_connect)
job = q.enqueue_in(timedelta(seconds=10), hello_world)


## Test 3: Time a que: Schedule the job
# Print the current time
# q = Queue(connection=redis_connect)
# now = datetime.now()
# print(f"Current time: {now}")

# target = datetime(2025, 1, 2, 16, 4)
# print(f"Target time is: {target}")

# job = q.enqueue_at(target, hello_world)  # Updated year to 2024 or later
# print(f"Job enqueued: {job.id}")
