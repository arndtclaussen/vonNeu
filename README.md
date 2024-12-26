# vonNeu
Lets have some internal fun. Why not.

# Initial Python setup (SOP)

We create a new environment. 
We are using the name *env*, because it is already in the .gitignore.
```
python3 -m venv env
```
Create a requirements.txt file by simply
```
touch requirements.txt
```
And then we activate the environment
```
source env/bin/activate
```
Maybe we need to update pip other wise we can install the requirements.
```
python -m pip install --upgrade pip
pip3 install -r requirements.txt
```

# Short Cut Learning for VS Code
* Listing all Short Cuts: Strg + K and Strg + S
* Fold all: Strg + K amd Strg + 0
* Unfold All: Strg + K and Strg + J

# Using Docker Locally to run the stuff in a postgres or something.
* Start the docker container with a simple postgres SQL.
```
docker run --name idle-clicker-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=myuser -e POSTGRES_DB=idle_clicker_db -d -p 5432:5432 postgres
```
* For testing purposes: Connect with something like dbeaver into it.

# Learn the link between Flask | SQL | Web
We are following this [here](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application).


export FLASK_APP=app
export FLASK_ENV=development


### Bringin in Tailwind
npx tailwindcss init
