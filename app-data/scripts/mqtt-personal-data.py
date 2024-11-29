import paho.mqtt.client as mqtt
import time
import json
import psycopg2
from config import load_config

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.subscribe("idc/fcdata")
    else:
        print("could not connect, return code:", return_code)

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def on_message(client, userdata, message):
    # Decode the message to a string
    msg_str = message.payload.decode("utf-8")
    
    # Convert string into dictionnary and extract values
    try:
        msg_dict = json.loads(msg_str)
        value = msg_dict.get("value")
        topic = msg_dict.get("topic")

        # Connection to database
        config = load_config()
        conn = connect(config)
        if conn:
            conn.autocommit = True
            cursor = conn.cursor()

            # request updated
            update_query = """
                UPDATE users 
                SET {column} = %s 
                WHERE _id = 1;
            """
            
            # Dynamically insert the column name (topic) in the query
            update_query = update_query.format(column=topic)
            
            # execut request
            cursor.execute(update_query, (value,))
            print(f"Updated {topic} to {value}.")

            # close cursor and connection
            cursor.close()
            conn.close()
            
    except json.JSONDecodeError as e:
        print("Error when decoding of JSON :", e)


broker_hostname ="127.0.0.1"
port = 1883 

client = mqtt.Client("Client2")
client.on_connect=on_connect
client.on_message=on_message

client.connect(broker_hostname, port) 
client.loop_start()

try:
    time.sleep(1000000)
finally:
    client.loop_stop()
