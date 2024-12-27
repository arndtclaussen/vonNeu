import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect


### Loading Environment Variables
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.



app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST"),
        database=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    return conn



@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Probes;')
    probes = cur.fetchall()  # lowercase variable names for consistency
    cur.close()
    conn.close()
    return render_template('index.html', probes=probes) # lowercase variable name here too

@app.route('/probe/<int:probe_id>')
def probe_details(probe_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Probes WHERE id = %s;', (probe_id,))
    current_probe = cur.fetchone()

    if not current_probe:  # Handle the case where the probe is not found
        return "Probe not found", 404  # Or redirect to an error page


    cur.execute('SELECT * FROM Probes;') # Fetch all probes for sidebar
    probes = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('probe_details.html', current_probe=current_probe, probes=probes)  # Pass both variables