import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
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



# Load CSV file with header
df = pd.read_csv('dati.csv', delimiter=';', header=0)

# Conversion of columns : 

# column date : 
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d')

# column activity : 
df['activity'] = df['activity'].astype(bool)

# Column time :
converted_time = []
for time_value in df['time']:
    try:
        parts = time_value.split(':')
        if len(parts) == 4:
            time_str = f"{parts[0]}:{parts[1]}:{parts[2]}.{parts[3]}"
            converted_time.append(time_str)
        else:
            raise ValueError(f"Format expected : {time_value}")
    except Exception as e:
        print(f"Error while loading the time {time_value}: {e}")
        converted_time.append(None)

df['time'] = converted_time


# Explicit type convertion of column in native python
df = df.astype({
    'activity': int,
    'acceleration_x': float,
    'acceleration_y': float,
    'acceleration_z': float,
    'gyro_x': float,
    'gyro_y': float,
    'gyro_z': float,
})

# Conversion of lines of DataFrame in tuple list (with activity in boolean)
records = [tuple(map(lambda x: x.item() if hasattr(x, 'item') else x, row)) for row in df.to_records(index=False)]

records = [
    (
        row.date,
        row.time,
        bool(row.activity),
        row.acceleration_x,
        row.acceleration_y,
        row.acceleration_z,
        row.gyro_x,
        row.gyro_y,
        row.gyro_z,
    )
    for row in df.itertuples(index=False)
]


# Insertion request
query = """
    INSERT INTO activity (date, time, activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
    VALUES %s
"""

# Execution of the insertion request
execute_values(cursor, query, records)
