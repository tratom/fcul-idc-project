import paho.mqtt.client as mqtt 
import time
import csv
import json
from datetime import datetime

broker_hostname = "127.0.0.1"
port = 1883 

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client("Client1")
# client.username_pw_set(username="user_name", password="password") # uncomment if you use password auth
client.on_connect=on_connect

# TLS - added later
# path = './certs/'
# client.tls_set(ca_certs=f'{path}ca.crt',
# certfile=f'{path}client.crt',
# keyfile=f'{path}client.key')
# client.tls_insecure_set(True)

client.connect(broker_hostname, port)
client.loop_start()

topic = "idc/FC64699"

# File dei dati
file_path = "online.data"

# Legge i dati dal file CSV e invia le richieste
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        row['date'] = now.strftime("%Y-%m-%d")
        row['time'] = now.strftime("%H:%M:%S.%f")
        client.publish(topic, json.dumps(row))
        time.sleep(1)  # Pausa tra le richieste per evitare sovraccarico del server

client.loop_stop()