import paho.mqtt.client as mqtt
import time
import pandas as pd
import json

broker_hostname = "127.0.0.1"
port = 1883

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, return code:", return_code)

client = mqtt.Client("Client1")
client.on_connect = on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic = "idc/fcxx"
msg_count = 0

# load of CSV
df = pd.read_csv('online.data.csv', header=None, delimiter=';')

# Generate JSON messages
messages = []
for _, row in df.iterrows():
    accel_and_gyro = row[-6:].values
    message = {
        "acceleration_x": accel_and_gyro[0],
        "acceleration_y": accel_and_gyro[1],
        "acceleration_z": accel_and_gyro[2],
        "gyro_x": accel_and_gyro[3],
        "gyro_y": accel_and_gyro[4],
        "gyro_z": accel_and_gyro[5],
    }
    messages.append(message)

try:
    while msg_count < len(messages):
        if(msg_count!=0):
            time.sleep(1)
            result = client.publish(topic, json.dumps(messages[msg_count]))
            status = result[0]
            if status == 0:
                print(f"Message {messages[msg_count]} is published to topic {topic}")
            else:
                print("Failed to send message to topic " + topic)
        msg_count += 1
finally:
    client.loop_stop()
