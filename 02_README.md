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

## Using Docker Locally to run the stuff in a postgres or something.
* Start the docker container with a simple postgres SQL.
```
docker run --name game-vonneu -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=myuser -e POSTGRES_DB=vonneu_db -d -p 5432:5432 postgres
```
* For testing purposes: Connect with something like dbeaver into it.



## Setup Flask
export FLASK_APP=app
export FLASK_ENV=development


## Bringin in Tailwind
npx tailwindcss init


## References
* Library Flask Example, see [here](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application).

