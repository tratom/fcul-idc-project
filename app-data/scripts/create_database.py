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
        height FLOAT
    )
    """)

cursor.execute(
    """
    INSERT INTO users (age, is_male, weight, height) 
    VALUES (30, true, 75.0, 1.80)
    """)
