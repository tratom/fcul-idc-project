import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from config import load_config 

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.subscribe("idc/fcxx")
    else:
        print("could not connect, return code:", return_code)


def on_message(client, userdata, message):
    # Decode the message to a string
    msg_str = message.payload.decode("utf-8")
    
    # Convert string into dictionnary and extract values
    try:
        msg_dict = json.loads(msg_str)
        now = datetime.now()

        # TODO UPDATE THIS VALUE WITH MACHINE LEARNING PROGRAM
        activity = True 

        config = load_config()
        conn = connect(config)
        conn.autocommit = True
        cursor = conn.cursor()

        records = [
            (
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                bool(activity),
                msg_dict.get("acceleration_x"),
                msg_dict.get("acceleration_y"),
                msg_dict.get("acceleration_z"),
                msg_dict.get("gyro_x"),
                msg_dict.get("gyro_y"),
                msg_dict.get("gyro_z"),
            )
        ]
        
        # Insertion request
        query = """
            INSERT INTO activity (date, time, activity, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
            VALUES %s
        """

        # Execution of the insertion request
        execute_values(cursor, query, records)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print('New value added')


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
