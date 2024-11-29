from configparser import ConfigParser
import psycopg2

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        

def get_users_data():
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

        # Store data in variables
        users = users_data

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return users
    return []


def count_activities_by_filter(date, filter_type='day'):
    """
    Count the number of running activity (1) and walking (0) with the filter : 'day', 'month', or 'week'.
    """
    config = load_config()
    conn = connect(config)
    if conn:
        conn.autocommit = True
        cursor = conn.cursor()

        # Construct request with filter
        if filter_type == 'day':
            query = """
                SELECT 
                    SUM(CASE WHEN activity = TRUE THEN 1 ELSE 0 END) AS running_count,
                    SUM(CASE WHEN activity = FALSE THEN 1 ELSE 0 END) AS walking_count
                FROM activity
                WHERE date = %s
            """
            params = (date,)
        elif filter_type == 'month':
            query = """
                SELECT 
                    SUM(CASE WHEN activity = TRUE THEN 1 ELSE 0 END) AS running_count,
                    SUM(CASE WHEN activity = FALSE THEN 1 ELSE 0 END) AS walking_count
                FROM activity
                WHERE DATE_PART('year', date) = DATE_PART('year', %s)
                AND DATE_PART('month', date) = DATE_PART('month', %s)
            """
            params = (date, date)
        elif filter_type == 'week':
            query = """
                SELECT 
                    SUM(CASE WHEN activity = TRUE THEN 1 ELSE 0 END) AS running_count,
                    SUM(CASE WHEN activity = FALSE THEN 1 ELSE 0 END) AS walking_count
                FROM activity
                WHERE DATE_PART('year', date) = DATE_PART('year', %s)
                AND DATE_PART('week', date) = DATE_PART('week', %s)
            """
            params = (date, date)
        else:
            raise ValueError("Invalid filter type. Use 'day', 'month', or 'week'.")

        # Execute request
        cursor.execute(query, params)
        counts = cursor.fetchone()

        # Close connection
        cursor.close()
        conn.close()
        
        # Convertir les secondes en minutes et arrondir au centième
        running_minutes = round(counts[0] / 60, 2) if counts[0] else 0
        walking_minutes = round(counts[1] / 60, 2) if counts[1] else 0

        # Return the result into a dictionnary
        return {"running": running_minutes, "walking": walking_minutes}
    return {"running": 0, "walking": 0}

