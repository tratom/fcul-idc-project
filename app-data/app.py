# Local imports
import datetime
import numpy as np

# Third part imports
from flask import Flask
from flask import request
import pandas as pd
import joblib

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
        value = float(value)
        if key in min_values and key in max_values:
            scaled_data[key] = (value - min_values[key]) / (max_values[key] - min_values[key])
        else:
            raise KeyError(f"Key {key} not found in min_values or max_values")
    return scaled_data

def dict_to_np_array(scaled_data):
    """
    Convert a scaled dictionary to a numpy array of floats in the given feature order.
    
    Args:
        scaled_data (dict): The scaled feature dictionary.
        feature_order (list): The list of features in the order expected by the model.
        
    Returns:
        np.ndarray: A numpy array of floats in the specified order.
    """
    feature_order = ['acceleration_x', 'acceleration_y', 'acceleration_z', 'gyro_x', 'gyro_y', 'gyro_z']
    try:
        # Extract features in the correct order
        feature_values = [scaled_data[feature] for feature in feature_order]
        return np.array(feature_values, dtype=float)
    except KeyError as e:
        raise ValueError(f"Missing feature in input data: {e}")


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Return service health"""
    return 'ok'


@app.route('/predict', methods=['POST'])
def predict():
    feature_dict = request.get_json()
    print(feature_dict)
    data = dict(feature_dict)

    if "date" in feature_dict:
        feature_dict.pop("date")
    if "time" in feature_dict:
        feature_dict.pop("time")

    if not feature_dict:
        return {
            'error': 'Body is empty.'
        }, 500

    try:
        # Assuming the model is named "rf-model.dat.gz"
        model_name = 'knn-model'
        model = joblib.load('model/' + model_name + '.dat.gz')
        
        # Scale and convert to numpy array
        scaled_data = scale_values(feature_dict)
        np_array_data = dict_to_np_array(scaled_data)
        
        # Wrap scaled_data into a list before passing to the model
        response = {
            "prediction": get_model_response([np_array_data], model)["prediction"],
            "data": data
        }
        
        
    except ValueError as e:
        print(e)
        return {'error': str(e).split('\n')}, 500

    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
