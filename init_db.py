import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="vonneu_db",
        user="myuser",
        password="mysecretpassword")


cur = conn.cursor()

# Create Probes table
cur.execute('DROP TABLE IF EXISTS Probes;')
cur.execute('''CREATE TABLE Probes (
                id integer PRIMARY KEY,
                Type varchar(50) NOT NULL,
                Build_Time timestamp,
                Status varchar(50)
                );''')

# Insert data into Probes table
cur.execute('''INSERT INTO Probes (id, Type, Build_Time, Status)
            VALUES (%s, %s, %s, %s);''',
            (12, 'Mk1', '2024-12-27 06:04:00', 'Docked'))

cur.execute('''INSERT INTO Probes (id, Type, Build_Time, Status)
            VALUES (%s, %s, %s, %s);''',
            (13, 'Mk1', '2024-12-27 08:04:00', 'Exploring'))

cur.execute('''INSERT INTO Probes (id, Type, Build_Time, Status)
            VALUES (%s, %s, %s, %s);''',
            (23, 'Mk2', None, 'In Production')) # Using None for NULL timestamp


# Create Asteroids table
cur.execute('DROP TABLE IF EXISTS Asteroids;')
cur.execute('''CREATE TABLE Asteroids (
                id integer PRIMARY KEY,
                "Size (in kg)" bigint,  -- Use double quotes for column names with spaces
                "Delta V" integer
                );''')


# Insert data into Asteroids table
cur.execute('''INSERT INTO Asteroids (id, "Size (in kg)", "Delta V")
            VALUES (%s, %s, %s);''',
            (1, 1242, 100))

cur.execute('''INSERT INTO Asteroids (id, "Size (in kg)", "Delta V")
            VALUES (%s, %s, %s);''',
            (2, 12423342234, 1002))


conn.commit()

cur.close()
conn.close()
