import datetime
import json
from flask import Flask, request
import pandas as pd
import joblib
from paho.mqtt.client import Client

from modules.functions import get_model_response

def scale_values(data):
    min_values = {
        'acceleration_x': -5.3505,
        'acceleration_y': -3.299,
        'acceleration_z': -3.7538,
        'gyro_x': -4.4306,
        'gyro_y': -7.4647,
        'gyro_z': -9.48
    }
    max_values = {
        'acceleration_x': 5.6033,
        'acceleration_y': 2.668,
        'acceleration_z': 1.6403,
        'gyro_x': 4.8742,
        'gyro_y': 8.498,
        'gyro_z': 11.2662
    }

    # Scale the data
    scaled_data = {}
    for key, value in data.items():
        if key in min_values and key in max_values:
            scaled_data[key] = (value - min_values[key]) / (max_values[key] - min_values[key])
        else:
            raise KeyError(f"Key {key} not found in min_values or max_values")
    return scaled_data

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Return service health"""
    return 'ok'

@app.route('/predict', methods=['POST'])
def predict():
    feature_dict = request.get_json()
    print(feature_dict)
    if not feature_dict:
        return {'error': 'Body is empty.'}, 500

    try:
        # Assuming the model is named "rf-model.dat.gz"
        model_name = 'rf-model'
        model = joblib.load('model/' + model_name + '.dat.gz')
        
        # Directly pass feature_dict to scale_values
        scaled_data = scale_values(feature_dict)
        
        # Wrap scaled_data into a list before passing to the model
        response = get_model_response([scaled_data], model)
    except ValueError as e:
        print(e)
        return {'error': str(e).split('\n')}, 500

    return response, 200

"""
# MQTT Configuration
broker_hostname = "127.0.0.1"
port = 1883
topic = "idc/iris"

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode('utf-8'))
        print(f"Received message: {message}")

        # Do prediction here
        scaled_data = scale_values(message)
        model = joblib.load('model/rf-model.dat.gz')
        prediction = get_model_response([scaled_data], model)
        print(f"Prediction: {prediction}")
    except Exception as e:
        print(f"Error processing message: {e}")

mqtt_client = Client("Flask_Server")
mqtt_client.on_message = on_message
mqtt_client.connect(broker_hostname, port)
mqtt_client.subscribe(topic)
mqtt_client.loop_start()
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')
