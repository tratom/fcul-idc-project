import psycopg2
from config import load_config 

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

config = load_config()
conn = connect(config)
conn.autocommit = True
cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        _id SERIAL PRIMARY KEY,
        age INTEGER,
        is_male BOOL,
        weight FLOAT,
        height FLOAT,
        threshold_running INTEGER,
        threshold_walking INTEGER
    )
    """)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS activity (
        _id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        time TIME NOT NULL,
        activity BOOL,
        acceleration_x FLOAT NOT NULL,
        acceleration_y FLOAT NOT NULL,
        acceleration_z FLOAT NOT NULL,
        gyro_x FLOAT NOT NULL,
        gyro_y FLOAT NOT NULL,
        gyro_z FLOAT NOT NULL
    )
    """)

cursor.execute(
    """
    INSERT INTO users (age, is_male, weight, height, threshold_running, threshold_walking) 
    VALUES (30, true, 75.0, 1.80, 30, 30)
    """)
