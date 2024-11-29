import psycopg2
from config import load_config

def mesure_burned_calories(body_weight,velocity,height):
    c1 = 0.035*body_weight + velocity*velocity/height *0.029*body_weight
    return c1

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Load database configuration
config = load_config()

# Connect to the database
conn = connect(config)
if conn:
    conn.autocommit = True
    cursor = conn.cursor()

    # Fetch data from users table
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()

    # Fetch data from activity table
    cursor.execute("SELECT * FROM activity")
    activity_data = cursor.fetchall()

    # Print and store data in variables
    print("Users Data:", users_data)
    print("Activity Data:", activity_data)

    # Store data in variables
    users = users_data
    activity = activity_data

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Print final variables
    print("Users:", users)
    print("Activity:", activity)

