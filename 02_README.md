# README
This documents describes how to setup the development and testing environment on a local machine.


## Initial Python setup (SOP)
Create a new environment. 
```
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip3 install -r requirements.txt
```

## Short Cut Learning for VS Code
* Listing all Short Cuts: Strg + K and Strg + S
* Fold all: Strg + K amd Strg + 0
* Unfold All: Strg + K and Strg + J
* Format HTML: 
    * Format Document command Ctrl+Shift+I to format the entire file 
    * Format Selection Ctrl+K Ctrl+F to just format the selected text.

## Using Docker Locally to run the stuff in a postgres or something.
* Start the docker container with a simple postgres SQL.
```
docker run --name game-vonneu -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=myuser -e POSTGRES_DB=vonneu_db -d -p 5432:5432 postgres
```
* For testing purposes: Connect with something like dbeaver into it.



## Setup Flask
export FLASK_APP=app
export FLASK_ENV=development

export POSTGRES_HOST="localhost"
export POSTGRES_DB="vonneu_db"
export POSTGRES_USER="myuser"
export POSTGRES_PASSWORD="mysecretpassword"



## Bringin in Tailwind
npx tailwindcss init

 npm install -D tailwindcss
 --> This installs node_modules folder and package-lock.json as well as package.json

 bash npx tailwindcss -i ./templates/**/*.html -o static/tailwind.css


## Redis que
See here for details: https://redis.io/learn/howtos/quick-start

``` 
docker run --name redis-vonneu -d -p 6379:6379 redis
docker run -d --name redis-vonneu -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
Then to start
```
rq worker -with-scheduler
rq worker teste_me -with-scheduler
```

There is a dashboard


From the webpage we have:
```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

Just note: redis/redis-stack contains both Redis Stack server and RedisInsight. 
This container is best for local development because you can use RedisInsight to visualize your data. 
redis/redis-stack-server provides Redis Stack but excludes RedisInsight. 
This container is best for production deployment.


We add in environment:
REDIS_HOST=127.0.0.1
REDIS_PORT=6379




## References
* Library Flask Example, see [here](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application).



## Honcho
Using a Procfile to start different tasks
* To identify, if still running lsof -i :5005